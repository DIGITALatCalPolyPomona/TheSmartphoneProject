# Project History

## Timeline

| Date | Commit | Event |
|------|--------|-------|
| 2025-07-16 | (backups) | Initial design iterations — 5 backup snapshots in `thermometer-backups/` before first git commit |
| 2025-07-19 | `18f5047` | First git commit — MCP9600 schematic + initial PCB layout uploaded |
| 2025-07-27 | `dfb0be3` | BMP581 pressure sensor added to schematic ("Added bmp581 Pressure Sensor to temperature sensor daughter board") |
| 2025-07-27 | (backup) | 6th backup snapshot (21:50) — the only post-git backup in `thermometer-backups/` |
| 2025-08-13 | `0baa108` | Zynq-Carrier-Power added as git submodule |
| 2025-08-13 | `4633a5a`–`e697671` | Multiple attempts to configure the Zynq-Carrier-Power submodule |
| 2025-08-23 | `e8460a1`–`3b9bdd7` | DIGITALBot submodule added, re-added, and adjusted (churn continued into Aug 24) |
| 2025-08-26 | `c81e8e5` | DIGITALBot submodule removed — last design commit (all later commits are docs/config only) |
| 2026-06-02 | `0a96fb0` | Preservation documentation added (README, CLAUDE.md, docs/, .claude/skills/) |
| 2026-06-08 | `b8c614a` | Documentation audit corrections (KiCad ground-truth pass) |
| 2026-07-09 | `14322b4` | OpenWiki knowledge base + governance added (PR #2 branch) |
| 2026-10-01 | `4b78c66` | PR #1 merged — docs corrections + CLAUDE.md/AGENTS.md |

Side activity (not on `main`): the `TheFingerprintSensor` branch holds `cc17e00`
(2026-02-05, AngeloDuenas — "The fingerprint sensor sensor.zip", a R503/R502
fingerprint module design uploaded via web UI). The two efforts never merged.

Active design span: ~38 days (July 19 – August 26, 2025).

## Team Members

| Name | Email | GitHub |
|------|-------|--------|
| pyson2k | paung@cpp.edu | pyson2k |
| Sebastian Graciano | sebgra518@gmail.com | sebgra518 |
| pixelatedknight27 | maxgross72@gmail.com | maxgross72 |
| eryn-chen | eryncchen@gmail.com | eryn-chen |
| ARussellChung | — | ARussellChung |
| Angelo Duenas | — | AngeloDuenas |

(ARussellChung authored commit `a06b248`; AngeloDuenas authored the
`TheFingerprintSensor` branch work and owned the DIGITALBot repo briefly
submoduled in Aug 2025.)

## Submodule History

### Zynq-Carrier-Power

- **URL:** `https://github.com/eryn-chen/Zynq-Carrier-Power` (branch: master)
- **Added:** August 13, 2025
- **Status:** Entry present in `.gitmodules`; **populated** on the maintainer's checkout at `7aed9fc` (upstream `master` tip as of Oct 2026). Fresh clones get an empty directory until `git submodule update --init` is run.
- **Purpose:** The intended host/carrier board this daughter board was designed to connect to (upstream README: "Zynq-Carrier-Template — a template Daughterboard for pinguz97's Zynq-SoM"; contents include a BQ25629 charger, USB-C, and SoM mezzanine connector — **no J1-compatible mate was found**, so the interface is unresolved).
- **To initialize (fresh clones):** `git submodule update --init`

### DIGITALBot

- **Added:** ~August 23, 2025
- **Removed:** August 26, 2025 (commit `c81e8e5`)
- **Purpose:** Unclear in context of this hardware project; appeared to be a chatbot submodule
- **Status:** Fully removed from `.gitmodules` and repo

## Design Decisions Recorded

- **BMP581 I2C address: 0x46 (intended)** — the `0x46` annotation label sits next to U2's SDO/ADR pin, but the pin is actually wired to the `INT` net (the INT pin is the one tied to GND — the two appear swapped). If taken literally, the I2C address is indeterminate. Note: BMP581 addresses are 0x46/0x47 (not 0x76/0x77 — those belong to BMP280/BMP388).
- **MCP9600 I2C address: 0x60 (intended)** — annotated with a `0x60` label (a tri_state global label used as a visual note, not a signal connection). However, ADDR (pin 16) is actually wired to the `SCL` net, not floating — so the programmed address is indeterminate until the miswiring is repaired.
- **No I2C pull-up resistors on this board** — the host board (Zynq-Carrier-Power) is expected to provide them.
- **1mm pitch chosen for J1** — compact form factor for daughter board interface.
- **Custom MCP9600 footprint** — standard KiCad QFN-20 was insufficient; team created a 30-pad footprint: 20 peripheral pads (10 signal + 10 GND) + 10 EXP sub-pads (21–30) inside the exposed thermal pad area. The "21N" in the footprint name refers to 21 unique electrical nets.
- **BMP581 library not localized** — sourced from SnapEDA and added to the GLOBAL KiCad library on the developer's machine. The project-level `sym-lib-table` and `fp-lib-table` have no BMP581 entry. This is the project's most critical "must fix before reopening" issue.

## Unresolved Issues at Time of Abandonment

These were open issues in the design when work stopped:

1. **EXP pad floating** — MCP9600 exposed thermal pad (pads 21–30) forms isolated net `Net-(U1-EXP-Pad21)`. Should be connected to GND in the schematic.
2. **U1 I2C miswired** — MCP9600's SCL pin (19) is tied to **GND** by a power symbol sitting on it; SDA (pin 20) is unconnected; ADDR (pin 16) sits on the `SCL` net. The SCL/SDA global labels reach J1 but not U1's I2C pins.
3. **U1 ALERT pins swapped/partially wired** — `ALERT_3` reaches pin 14 correctly, but `ALERT_4` lands on pin 12 (physical ALERT_2) and `ALERT_2` lands on pin 15 (physical ALERT_4); ALERT_1 (pin 11) is bare. Root cause is likely symbols wired for vertically-mirrored geometry that isn't applied to the instances.
4. **U2 similarly miswired** — SCK/SCL pin (2) tied to +3.3V, SDO/ADR (5) on the `INT` net, INT (7) tied to GND, SDI/SDA (4) unconnected, VDDIO/GNDs unconnected.
5. **No power on J1** — all 7 pins carry signals (INT, ALERT_4..1, SDA, SCL); the board's +3.3V/GND entry path is undefined.
6. **J1 footprint set in PCB only** — the schematic J1 symbol has an empty Footprint property; the footprint was placed directly in the PCB editor.
7. **IgnorePin label** — a `global_label "IgnorePin"` floats at (96.52, 67.31) on U1's pin column between VDD and ALERT_1; it touches no pin, so it suppresses nothing. Purpose unknown — likely leftover from editing.

## Why Abandoned

No explicit reason recorded in commit messages. Last activity (August 23–26) was submodule cleanup with no schematic or PCB changes. The PCB remained incomplete:

- No copper traces routed
- No board outline defined
- BMP581 not placed in PCB (schematic only)
- J1 connector pinout exists on paper (labels on all 7 pins) but leaves no room for power and was never synced to the PCB
- Schematic mid-rewire: U1/U2 wiring was changed for a mirrored symbol layout that was never applied, leaving both chips misconnected (see Unresolved Issues)

The project appears to have been paused rather than cancelled — though "schematic substantially complete" overstates it: the last design act left the schematic in a broken mid-refactor state that must be repaired before any layout work.

## Backup Archive Contents

The `thermometer-backups/` directory contains 6 timestamped KiCad ZIP backups: 5 from the day of initial setup (July 16, 2025, before version control) plus 1 post-git snapshot (July 27). They represent pre-/early-git design iterations:

| Archive | Timestamp |
|---------|-----------|
| thermometer-2025-07-16_213626.zip | 2025-07-16 21:36 |
| thermometer-2025-07-16_214447.zip | 2025-07-16 21:44 |
| thermometer-2025-07-16_215526.zip | 2025-07-16 21:55 |
| thermometer-2025-07-16_220757.zip | 2025-07-16 22:07 |
| thermometer-2025-07-16_221732.zip | 2025-07-16 22:17 |
| thermometer-2025-07-27_215053.zip | 2025-07-27 21:50 |
