# Notion ↔ OpenWiki Audit — Lead Review Draft

**Status:** DRAFT FOR TECHNICAL LEAD REVIEW — nothing below has been applied.
**Audit date:** 2026-10-02 · Repo branch: `claude/openwiki-knowledge-graph-tbcphx` (head `88ce6ab`)
**Scope:** DIGITAL @ Cal Poly Pomona Notion workspace vs `wiki/` + `docs/` + KiCad files.
**Method:** 53 Notion pages fetched to `/tmp/notion-audit/`; 4 explorer subagents produced findings; 3 adversarial verifier subagents re-checked every claim against primary sources (KiCad S-expression geometry, scratch dumps, governance schema). Every row below carries a verification verdict.

**How to review:** each proposed change has a `Sign-off` column. Leads approve/reject per row; only approved rows are applied. Claims marked `NEEDS VERIFICATION` mean the *Notion* value may itself be wrong — confirm with your team's datasheets, not with this document.

---

## 0. Errata — corrections found during verification

The verifier pass caught four errors in the audit's own claims. These corrections supersede the raw findings:

1. **MCP9600 alert outputs are push-pull ONLY**, not configurable open-drain (DS20005426 §3.4 — polarity/comparator/interrupt configurable, no open-drain option). `docs/connector-pinout.md:44` asserts the opposite — **flagged as a doc bug** to fix in the same pass.
2. **BMP581 range discrepancy:** Notion states 300–1100 hPa; `docs/components.md:70` states 30–125 kPa (=300–1250 hPa). One of them is wrong — lead must pick the datasheet value before anything is written.
3. **Notion MCP9600 ±0.2 °C accuracy** matches no verifiable datasheet figure (typical is ±0.5 °C) — treat as unverified.
4. Additional schematic defects the first pass missed: `#PWR03` GND dangles 2.54 mm above a `+3.3V` stub (near-miss short); **no I2C pull-up resistors anywhere**; PCB J1 footprint UUID doesn't match schematic J1 UUID (stale link); U2 pin 6 CSB is on the SCL net (not floating).

---

## 1. Verified ground truth (re-traced in `thermometer.kicad_sch`)

| Claim | Verdict | Evidence |
|---|---|---|
| J1 7-pin: 1=INT 2=ALERT_4 3=ALERT_3 4=ALERT_2 5=ALERT_1 6=SDA 7=SCL, no power/GND | CONFIRMED | sch symbol `Conn_01x07` @35.56,87.63; labels at pin endpoints |
| U1: SCL pin→GND, SDA floats, ADDR on SCL net, ALERT_2/4 swapped, VDD/GND/TC1/EXP unconnected | CONFIRMED | pin-level geometry trace; `#PWR06` on pin 19; `#PWR01` stub 2.54 mm short of VDD |
| U2: SCK→+3.3V, SDO→INT, INT→GND, CSB→SCL net, SDA/VDDIO/GND float | CONFIRMED | pin-level geometry trace |
| BMP581 library absent; symbol survives only in embedded `lib_symbols` cache | CONFIRMED | `sym-lib-table`/`fp-lib-table` list only `jackboys`/`jackboys2` |
| PCB netlist stale pre-rewire; zero copper; no Edge.Cuts; U2 footprint absent | CONFIRMED | `.kicad_pcb` nets all `unconnected-*`/single-pad named nets |
| Zynq-Carrier-Power populated @ `7aed9fc`; no J1-compatible mate | CONFIRMED | submodule HEAD; its connectors are 2.54 mm/JST/DF40C — no 7-pin 1.00 mm |
| `wiki/hardware/thermometer.md` "Current state" accurately describes files | CONFIRMED | all verifiable statements match |

## 2. Conflicts (Notion claims contradicted by repo)

| # | Notion page | Claim | Repo truth | Verdict | Severity |
|---|---|---|---|---|---|
| C1 | HD Thermometer `21e1…c230` | Example header `1=VCC 2=GND 3=SDA 4=SCL` | J1 = signals only, no power/GND | CONFIRMED | High — teaches wrong pinout |
| C2 | HD Barometer `2381…e486` | "Daughterboard header" table | Table is BMP581 die pinout (VDDIO/SCK/SDI/SDO/CSB), not J1 | CONFIRMED | High — dangerous mislabel |
| C3 | CONOPS `3e41…f6c1` | IMU/Thermometer/ALS on shared **SPI** bus + FIFO/AXI | Board is **I2C** on J1; all HD sensor pages spec I2C | CONFIRMED | High — architecture doc wrong |
| C4 | Write Daughterboard FW `2f71…1285` | `Microcontroller - ESP32 C3` | Repo has no MCU/firmware; Zynq host = I2C master | CONFIRMED | Medium — intent vs artifact gap |
| C5 | Build Logs `2671…f181` | "(9/7/25) Entry 1: Completed ✅" | No outline, zero copper, miswired schematic | CONFIRMED | High — false completion record |
| C6 | Trickle Charge `2601…9e84` | Discrete analog Li-Ion charger ("not using chargers, making one") | `Zynq-Carrier-Power` already contains BQ25629 charger IC | CONFIRMED | Medium — divergent design, unreconciled |
| C7 | Fingerprint `2411…3127` | FPC1030/FPC2530/FPC1020 research | Repo `TheFingerprintSensor` branch = R503/R502 module | CONFIRMED | Medium — parallel work never reconciled |
| C8 | STM32 Systems Controller `24f1…bf21` | STM32G431 power sequencer, 5 rails, USB-C mux | Scope overlaps Zynq-Carrier-Power's power role | CONFIRMED | Low — boundary ambiguity |
| C9 | CONOPS internal | Status `Done` but its Sequence Diagram sub-task is `Not started` | — | CONFIRMED | Low |

## 2.1 Discrepancy details — verbatim Notion text vs repo evidence

Each item quotes the Notion page exactly as fetched (scratch file = `/tmp/notion-audit/<id>.txt`, line numbers cited) against the specific repository artifact. Leads: confirm the "Lead action" per item.

### D-1 — J1 pinout is wrong in Notion (C1)
- **Notion states** (HD Thermometer, `21e1…c230.txt` L43): `"Pin 1 = VCC (3.3V or 5V), Pin 2 = GND, Pin 3 = SDA, Pin 4 = SCL"`
- **Repo shows** (`thermometer.kicad_sch`, `Conn_01x07` @35.56,87.63, labels sch:2053–2425): `1=INT 2=ALERT_4 3=ALERT_3 4=ALERT_2 5=ALERT_1 6=SDA 7=SCL` — **7 pins, zero power/GND pins**
- **Delta:** pin count (4 vs 7), signal set, and connector role are all different; the Notion example would mis-wire the board
- **Lead action:** approve change C1 (rewrite to real pinout) — or confirm the 4-pin example describes a *different planned* connector that should be labeled as such

### D-2 — Barometer "header" table is actually the sensor die pinout (C2)
- **Notion states** (`2381…e486.txt` L292–338, under heading "Define the Daughterboard Header"): rows `VDDIO / SCK / SDI / SDO / CSB / INT / VDD / VSS(3,8-9)`
- **Repo shows:** those are BMP581's own package pins; the daughterboard's actual connector J1 carries `INT/ALERT_4/3/2/1/SDA/SCL`
- **Delta:** die pins presented as the board-to-carrier interface; anyone building a carrier cable from this table connects the wrong thing
- **Lead action:** approve C2 (relabel table as "BMP581 package pinout") + decide whether a real J1 table should be added (C1 pattern)

### D-3 — CONOPS bus architecture: SPI vs actual I2C (C3)
- **Notion states** (`3e41…f6c1.txt`): L110 `"IMU / Thermometer / ALS | Daughterboard | Shared SPI Bus Channels"`; L77 `"Raw serial data streams into the FPGA-based custom SPI master logic… FIFO Buffers"`
- **Repo shows:** J1 pins 6/7 = `SDA`/`SCL`; MCP9600 and BMP581 are both wired as I2C parts; every HD sensor page also specs I2C — CONOPS contradicts both repo AND its own sibling pages
- **Delta:** shared-SPI/FIFO/AXI pipeline described nowhere in the hardware; no SPI pins exist on J1
- **Lead action:** approve C3 — but note this may be *aspirational* architecture for the FPGA fabric rather than an error; confirm intent before rewriting vs annotating

### D-4 — ESP32-C3 daughterboard MCU vs no MCU in repo (C4)
- **Notion states** (`2f71…1285.txt` L8–12): `"Microcontroller - ESP32 C3"` with named owner assignments for Audio, Heat, Light, RTC
- **Repo shows:** schematic contains U1 MCP9600 + U2 BMP581 only; no MCU, no firmware tree, no programming header; `docs/architecture.md` assumes the Zynq host is the I2C master
- **Delta:** Notion architecture puts a microcontroller on each daughterboard; repo implements a host-driven dumb-sensor board
- **Lead action:** D-gate — is ESP32-C3 intent (document as planned architecture, A3) or abandoned? Decide before wiki pull

### D-5 — "Completed ✅" build log vs broken board (C5)
- **Notion states** (`2671…f181.txt` L7): `"(9/7/25) Entry 1: Completed ✅"`
- **Repo shows** (verified pin-by-pin): U1 SCL pin shorted to GND; U1 SDA unconnected; TC1 not wired to VIN±; U2 SCK on +3.3V, SDO on INT, INT on GND, CSB on SCL net; PCB has zero copper segments/vias/zones; no Edge.Cuts outline; U2 footprint unresolved (BMP581 lib absent); no I2C pull-ups; `#PWR03` GND dangling 2.54 mm above a +3.3V stub
- **Delta:** the single "Completed" entry postdates none of the open defects — board cannot function as committed
- **Lead action:** D1 — Status/build-log corrections are lead-owned; recommend annotation rather than silent overwrite (preserve the entry, append reality)

### D-6 — Trickle-charger design vs existing BQ25629 (C6)
- **Notion states** (`2601…9e84.txt` L82): `"-not using chargers, making one"` + 2026-03/04 notes describing a TL431/LM358 discrete analog charger with op-amp comparator phases
- **Repo shows:** `Zynq-Carrier-Power/` submodule @ `7aed9fc` already contains a TI **BQ25629** integrated charger IC
- **Delta:** two parallel charging designs exist and were never reconciled; Notion notes are *newer* than the repo's last activity
- **Lead action:** D3 — engineering decision required; do not treat either side as stale

### D-7 — Fingerprint parts diverge across sources (C7)
- **Notion states** (`2411…3127.txt` + MP `3e41…8006`): research around FPC1030 / FPC2530 / FPC1020 (FPC fingerprint modules)
- **Repo shows:** branch `TheFingerprintSensor` contains an R503/R502 (serial fingerprint module) design
- **Delta:** different vendor families entirely — two unmerged research tracks
- **Lead action:** D4 — which module family is the program using?

### D-8 — Status fields claim Done on broken/absent work
- **Notion states:** `Status: Done` on Thermometer (`21e1` L5), Barometer (`2381` L13), Heat Sensor (`2481` + dup `2f71-802f`), RTC (`2411-80f6`), Microphone (`2421`), Haptic (`2311-8016`)
- **Repo shows:** the only board that exists is mid-rewire/broken (D-5 evidence); RTC, Heat Sensor, Mic, Haptic, Fingerprint, IMU, ToF, Flashlight, Light have **zero repo artifacts** — for Mic/Haptic the schematics exist only as Notion-attached images
- **Delta:** `Done` in Notion conflates "research done" with "hardware done"; wiki truth (`thermometer.md` Current state) says in-progress/defective
- **Lead action:** D1 — decide whether Status means research-phase or shipped-hardware; annotate vs rewrite

### D-9 — "Phase III active" vs repo paused (§3 row 2)
- **Notion states** (`1e11…e386.txt`): `"Current Phase: Phase III — Design Custom PCBs"` live; Phase 3 testing task `In progress`
- **Repo shows:** last design activity ~Aug 2025 (`thermometer-backups/` timeline, decision record `2025-08-digitalbot-submodule-removal`); nothing since
- **Delta:** dashboard implies active work through the pause
- **Lead action:** D1-adjacent — update dashboard to reflect dormant state or confirm new activity exists

### D-10 — Xilinx 7200 typo (§3 row 3)
- **Notion states** (`1e11…0996.txt` L75, Task 1.2): `"physical pins on the Xilinx 7200 package"`
- **Repo shows:** Zynq-7020 SoC (carrier submodule targets Zynq-7000; STM32 page correctly says "Zynq-7000")
- **Delta:** "7200" vs "7020" — one-character transposition, but wrong enough to confuse
- **Lead action:** approve C5 (trivial fix)

### D-11 — Notion pages contradict their own matrices
- **Heat Sensor** (`2481…2d28.txt`): pick = TMP1075DSGR — but its own matrix scored **TMP117AIDRVR 19 > TMP1075 18**
- **Touch Screen**: recommends Capacitive — but Infrared scored **13 > 8**
- **Delta:** internal contradictions, not repo conflicts — but they decide which parts get pulled into `docs/components.md`
- **Lead action:** D6 — confirm intended winner before any pull

### D-12 — Requirements values disagree between sources
- **Notion states:** BMP581 `"300–1100 hPa"`, MCP9600 `"±0.2 °C"` (`2381` L27-30; `21e1` L9-10)
- **Repo shows:** `docs/components.md:70` says BMP581 range `30–125 kPa` (=300–**1250** hPa); MCP9600 datasheet typical accuracy is ±0.5 °C, not 0.2
- **Delta:** both sides may be wrong; must be resolved against the actual datasheet before any "requirements" land in wiki
- **Lead action:** §0.2/§0.3 — assign datasheet owner

### D-13 — CONOPS marked Done while its own sub-task is Not started (C9)
- **Notion states** (`3e41…f6c1.txt` L12): `"Status":"Done"`; its Sequence Diagram sub-task: `"Not started"`
- **Delta:** rolled-up status contradicts child state
- **Lead action:** D1

### D-14 — Empty Notion shells vs documented wiki (reverse drift)
- **Notion states:** Thermometer MP `3e41…0e10`, Barometer MP `…e770`, STM32/LightSensor `…80d2`/`…80f3` = template headers only; Flashlight/Speakers/Barometer/Fingerprint/PowerReg/Touch/Camera/Trickle/SoM = fully blank
- **Repo shows:** `wiki/hardware/thermometer.md` documents real pin-level state; `hardware/zynq-carrier-power.md` documents the carrier
- **Delta:** the human-facing mirror is empty where git has substance — this is the primary wiki→Notion push case
- **Lead action:** approve §7 mapping + push

### D-15 — Barometer page template contamination
- **Notion states** (`2381…e486.txt`): still contains `"MCP9600T-E/MX"` strings and a "Choose a Temperature Sensor" header; options matrix row 8 duplicates LPS33KTR while MS5837 sits unscored — all under `Status: Done`
- **Delta:** page content doesn't match its own title/status
- **Lead action:** bundle with C2 cleanup

---

## 3. Stale/incorrect Notion content

| Notion page | Stale claim | True state | Verdict |
|---|---|---|---|
| Thermometer, Barometer, Heat Sensor(+dup), RTC, Microphone, Haptic (HD) | Status `Done` | Design mid-rewire, broken, paused Aug 2025 | CONFIRMED (all 6) |
| HD dashboard `…e386` | "Current Phase: Phase III — Design Custom PCBs" + Phase 3 testing `In progress` | Paused; also internally inconsistent (III=design vs 3=testing) | CONFIRMED |
| Main DB `…0996` | "Xilinx 7200" package pins | Should read Zynq-7020 | CONFIRMED (typo) |
| Barometer page | "Choose a Temperature Sensor" boilerplate + unscored MS5837 row + dup LPS33KTR row | Template contamination | CONFIRMED |
| Heat Sensor pick | TMP1075DSGR selected | Its own matrix scored TMP117AIDRVR 19 > 18 | CONFIRMED (internal contradiction) |
| Touch Screen | "Capacitive recommended" | Infrared scored 13 > Capacitive 8 | CONFIRMED (internal contradiction) |
| Power Regulation | placeholder gibberish ("jfkdsjlkaf", "liposuction battery") | draft-quality page marked In progress | CONFIRMED |
| PRD `1b21…147a` | Panda Linux, M.2 SSD, LTE, 6.1" display | SIDEKICK scope doc says no full OS / RTOS-or-text-engine | CONFIRMED (superseded) |
| `2f71…` duplicate pages | 5 verbatim component copies re-parented under "Write Daughterboard Firmware" | duplication drift | CONFIRMED |

## 4. Missing in Notion (wiki pages with no counterpart — informational only)

`libraries/jackboys-symbols`, `libraries/jackboys2-footprints`, `libraries/library-tables`, `guides/getting-started`, `governance/agent-governance`, `governance/confluence-sync`, `governance/documentation-standards`, `governance/notion-sync`, `decisions/2025-08-digitalbot-submodule-removal`. `hardware/zynq-carrier-power` has only a blank SoM shell (`3e41…57d7`). **Recommendation: leave unmapped** — governance content is agent-facing; mirror only if the club wants docs surfaced in Notion.

## 5. Orphans / Notion-only facts (pull candidates)

| Fact | Source page | Verdict | Where it could land |
|---|---|---|---|
| Sensor requirements (−25–250 °C, ±0.2 °C; ±1.0 hPa, ±0.5 °C, 300–1100 hPa) | HD Thermometer/Barometer | NEEDS VERIFICATION (see §0.2–0.3) | `wiki/hardware/thermometer.md` Requirements section |
| BMP581 selection matrix (8 candidates, 44 pts) | HD Barometer | CONFIRMED in Notion | `wiki/decisions/` (see P2) |
| Dual-barometer interior/exterior plan | HD Barometer | CONFIRMED in Notion | `wiki/decisions/` (see P2) |
| CONOPS system spec (rails 1.0/1.8/3.3 V, ≤15 ms, <42 °C touch, sensor list) | CONOPS | CONFIRMED in Notion — but SPI claim is wrong | fix in place; spec lives in Notion only |
| Part picks: TMP1075DSGR, RV-3028-C8-1PPM, ICM-20948 (29.25), VL53L1X+rear-ToF, AMM-2742-T-WP-R, DRV2605L, LM3644 | HD + MP pages | CONFIRMED in Notion | `docs/components.md` or decisions |
| ESP32-C3 firmware intent; merged-board rule (ICs back, connectors front) | Write FW / Combine | CONFIRMED in Notion | `docs/architecture.md` (intent-framed) |
| SIDEKICK rename + "legacy project" status | SIDEKICK root | CONFIRMED in Notion | `wiki/index.md` one-line note |
| Trickle charger analog notes (TL431/LM358, dated 2026-03/04 — post-repo-pause) | Trickle Charge | CONFIRMED — newer than repo | none in repo (conflict C6 first) |
| STM32 extras: TPS2121 mux, MKR footprint, 4-layer stackup | STM32 page | CONFIRMED in Notion | none (see C8) |
| 12-section mini-project doc template | MP pages | CONFIRMED | `wiki/_templates` candidate |

## 6. Proposed changes — grouped by what each needs

### A. Wiki edits — safe to apply on your approval (schema-validated)

| ID | Change | Target | Verdict | Sign-off |
|---|---|---|---|---|
| A1 | Add Requirements section (values pending §0 verification) | `wiki/hardware/thermometer.md` | VALID | ☐ |
| A2 | One-line "project renamed SIDEKICK (external)" note | `wiki/index.md` | VALID | ☐ |
| A3 | ESP32-C3 host intent + merged-board mechanical rule (framed as *intent*, not state) | `docs/architecture.md` | VALID | ☐ |
| A4 | Add missing items to thermometer Open work: I2C pull-ups, `#PWR03` near-short, J1 UUID mismatch | `wiki/hardware/thermometer.md` | VALID | ☐ |
| A5 | Fix `connector-pinout.md:44` push-pull/open-drain claim | `docs/connector-pinout.md` | VALID (doc bug) | ☐ |

### B. Require a `wiki/decisions/` page FIRST (architectural)

| ID | Change | Verdict | Sign-off |
|---|---|---|---|
| B1 | BMP581 selection matrix + dual-barometer plan — one decision page covers both; must land before any schematic change | VALID, required | ☐ |
| B2 | Second-barometer architecture decision | VALID, required | ☐ |

### C. Notion body edits — apply on approval (content only, no property fields)

| ID | Change | Verdict | Sign-off |
|---|---|---|---|
| C1 | Fix HD Thermometer example header → real J1 pinout | VALID | ☐ |
| C2 | Relabel HD Barometer "daughterboard header" table as BMP581 die pinout | VALID | ☐ |
| C3 | CONOPS: SPI → I2C (and note only MCP9600+BMP581 exist) | VALID | ☐ |
| C4 | Annotate empty MP shells as templates | VALID | ☐ |
| C5 | Fix "Xilinx 7200" typo | VALID | ☐ |

### D. NEEDS LEAD DECISION — do not apply without named owner

| ID | Change | Why gated | Sign-off |
|---|---|---|---|
| D1 | Set Status fields off `Done` (Thermometer/Barometer/Heat/RTC/Mic/Haptic, Build Log "Completed") | Status = lead-owned workflow metadata; overwriting destroys human state | ☐ owner: ____ |
| D2 | SHADES battery-temp disambiguation note | Scope creep unless a real naming collision is confirmed | ☐ owner: ____ |
| D3 | Reconcile Trickle discrete charger vs BQ25629 in submodule | Real design divergence — engineering call | ☐ owner: ____ |
| D4 | Reconcile Fingerprint FPC picks vs repo R503/R502 | Parallel workstreams never merged | ☐ owner: ____ |
| D5 | STM32 power board vs Zynq-Carrier-Power scope boundary | Ownership question | ☐ owner: ____ |
| D6 | Heat Sensor / Touch internal matrix contradictions | Which pick was actually intended? | ☐ owner: ____ |

## 7. Proposed page-mapping table (mirror)

| Wiki page | Notion page | URL | Status |
|---|---|---|---|
| `index.md` | SIDEKICK (TSP) root `3ab1…26ee` | app.notion.com/p/3ab169473d7780d790c9fe8b69b426ee | proposed |
| `hardware/thermometer.md` | Thermometer MP `3e41…0e10` | app.notion.com/p/3e4169473d77802ea963c2d3552f0e10 | proposed (wiki = source) |
| `hardware/thermometer.md` (legacy) | HD Thermometer `21e1…c230` | app.notion.com/p/21e169473d778007bf46e3cce8d5c230 | proposed |
| `hardware/thermometer.md` (U2) | Barometer MP `3e41…e770` + HD Barometer `2381…e486` | app.notion.com/p/3e4169473d7780908ef9d9e18576e770 | proposed |
| `hardware/zynq-carrier-power.md` | SoM `3e41…57d7` (blank) | app.notion.com/p/3e4169473d77803f8977fbebdcf257d7 | proposed (fill shell) |
| `docs/architecture.md` | CONOPS `3e41…6c1` | app.notion.com/p/3e4169473d7780f296d4ddf50a7af6c1 | proposed (needs C3 fix) |
| all other wiki pages | — | — | unmapped (intentional) |

## 8. Coverage limits (what was NOT exhaustively read)

- Legacy DB = 81 rows; ~25 unfetched rows are lifecycle docs (SDDPD phases), team-member lists, Recorded Meetings, calendar rows — no hardware-state risk identified, but sampling was risk-based, not complete.
- SHADES (~90 pages) and the ET numbered-template tree were inventoried via search, not fetched page-by-page.
- Notion attachments (KiCad zips, PDFs, images) were catalogued but not downloaded — the Mic/Haptic "Done" board images could not be diffed against repo files.

## 9. Process note for the sync skill

Verifier recommendation: amend `.claude/skills/notion-sync/SKILL.md` to split **block/body edits** (approval-flow per SKILL Step 5) from **property/Status edits** (per-field owner sign-off). Not applied — awaiting your call.
