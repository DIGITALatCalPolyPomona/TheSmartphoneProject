# TheSmartphoneProject — Thermometer Sensor Daughter Board

Hardware project by **DIGITAL at Cal Poly Pomona** (KiCad 9). A sensor
daughter board, the **Zynq-Carrier-Power** submodule, and the custom
**jackboys** part libraries.

**Status:** Paused August 2025 mid-rewire — the schematic has active wiring
defects (see below). Preserved for future resumption; documentation maintained.

## Start here

**Everything you need to know lives in the wiki: [`wiki/index.md`](wiki/index.md).**

New to the project? Read
[`wiki/guides/getting-started.md`](wiki/guides/getting-started.md).

## What This Is

A KiCad 9.0 PCB design for a compact thermometer and environmental sensor daughter board.
Measures temperature via an external thermocouple (using the MCP9600 amplifier IC) and
barometric pressure (using the BMP581 sensor). Both sensors communicate over a shared I2C
bus exposed on a 7-pin 1mm-pitch header (J1) for connection to a host board.

The host board was intended to be the [Zynq-Carrier-Power](https://github.com/eryn-chen/Zynq-Carrier-Power)
(a template carrier for pinguz97's Zynq SoM, by eryn-chen). The Zynq acts as the I2C master.

## Hardware Summary

| Ref | Part | Function | Package | I2C Address (intent) | Status |
|-----|------|----------|---------|-------------|--------|
| U1 | MCP9600-E_MX | Thermocouple amplifier + cold-junction compensation | QFN-20+EP (5×5mm, custom 30-pad footprint) | 0x60 | Schematic (miswired) + PCB footprint (unrouted) |
| U2 | BMP581 | Barometric pressure + temperature sensor | LGA-10 (2×2mm) | 0x46 | Schematic only (miswired), no footprint in PCB |
| TC1 | Thermocouple | External temperature probe | External | — | Schematic (wires stop short of U1), no footprint |
| J1 | 7-pin 1mm header | Interface to host board | 1mm pitch THT | — | Schematic labeled (no power pins); PCB pads unconnected |

Power: intended 3.3V from host via J1 — **but no J1 pin is assigned to +3.3V or
GND**; the board's power path is unresolved. No local regulation.

## Design State (verified 2026-10-01)

- Schematic: U1 (MCP9600) and U2 (BMP581) placed — but the last edit left them
  **miswired**: the wiring was drawn for vertically-mirrored symbol geometry that
  isn't applied, so signals land on wrong pins (details below).
- Custom MCP9600 symbol library: `jackboys.kicad_sym`
- Custom MCP9600 footprint (20 leads + EP + thermal vias): `jackboys2.pretty/`
- U1 and J1 footprints placed on PCB; PCB netlist is **stale** — it predates the
  schematic rewiring and must not be trusted or synced until the schematic is fixed.

## What Is Broken / Incomplete

- **Schematic miswiring (top priority):** U1 SCL pin (19) tied to GND, SDA (20)
  floating, ADDR (16) on the `SCL` net, ALERT_2/ALERT_4 labels swapped on the
  physical pins, VDD unpowered, all GND pins floating; U2 SCL pin (2) tied to
  +3.3V, SDO/ADR (5) on the `INT` net, INT (7) tied to GND, SDA/VDDIO/GNDs
  floating; TC1 wires end before reaching U1.
- **J1 pinout:** all 7 pins carry signal labels (`INT`, `ALERT_4`..`ALERT_1`,
  `SDA`, `SCL`) — leaving **no pin for power or ground**. A power-path decision
  is required.
- **PCB:** no copper routed, no board outline, U2/TC1 not placed; netlist stale.
- **Decoupling capacitors:** none exist (schematic has zero C/R symbols).
- **BMP581 library:** not in project lib tables — must reinstall from SnapEDA (see below).
- **U1 EXP pad:** exposed thermal pad (pads 21–30) floating, not on GND.

## Before Opening in KiCad

The BMP581 symbol and footprint (`BMP581:BMP581`) are **not stored in this repository**.
KiCad will show missing library errors without them.

**Reinstall steps:**

1. Download KiCad package from https://www.snapeda.com/parts/BMP581/Bosch/view-part/
2. Extract `.kicad_sym` and `.kicad_mod` files
3. Copy into repo as `BMP581.kicad_sym` + `BMP581.pretty/BMP581.kicad_mod`
4. Update `sym-lib-table` and `fp-lib-table` to point to local paths
5. Commit to repo so future users don't face the same issue

See `docs/library-notes.md` for detailed instructions.

## Repository Structure

```text
TheSmartphoneProject/
├── thermometer.kicad_sch         # Main schematic
├── thermometer.kicad_pcb         # PCB layout
├── thermometer.kicad_pro         # KiCad project settings
├── jackboys.kicad_sym            # Custom MCP9600 symbol library
├── jackboys.bak                  # Symbol library backup
├── jackboys2.pretty/             # Custom MCP9600 footprint library
│   └── QFN65P500X500X100-21N_MCP9600-E_MX.kicad_mod
├── sym-lib-table                 # Symbol library search paths
├── fp-lib-table                  # Footprint library search paths
├── fp-info-cache                 # KiCad footprint cache (auto-generated)
├── thermometer-backups/          # KiCad backup archives (5 pre-git + 1 post)
├── Zynq-Carrier-Power/           # Submodule (populated here at 7aed9fc — see below)
├── wiki/                         # OpenWiki knowledgebase (Markdown + frontmatter)
├── graph/                        # Generated knowledge graph — do not hand-edit
├── tools/openwiki/               # OpenWiki CLI (stdlib-only Python)
├── tools/ci/kicad_sanity.py      # KiCad file structural sanity checker
├── openwiki.config.json          # Which artifacts require wiki documentation
├── .github/workflows/            # CI: openwiki.yml, docs.yml
├── .claude/                      # Claude skills + agents (update-docs, review-changes)
├── thermometer.kicad_prl         # KiCad per-user project settings
├── AGENTS.md                     # Agent instructions (cross-tool canonical)
├── CLAUDE.md                     # Claude Code entry point (imports AGENTS.md)
├── README.md                     # This file
└── docs/                         # Design documentation
    ├── architecture.md
    ├── components.md
    ├── connector-pinout.md
    ├── library-notes.md
    └── project-history.md
```

## Submodule: Zynq-Carrier-Power

The `Zynq-Carrier-Power` directory is a git submodule referencing
https://github.com/eryn-chen/Zynq-Carrier-Power (branch: master). It is
**populated** on the maintainer's checkout, pinned at `7aed9fc` (upstream
`master` tip as of Oct 2026). On a fresh clone it will be empty until you run:

```bash
git submodule update --init
```

Note: no connector matching J1 (1.00mm, 7-pin) exists in the carrier design —
the mating interface is unresolved. See `docs/connector-pinout.md`.

## The knowledgebase is governed

This project was once paused and nearly lost all of its institutional
knowledge. To prevent a repeat, documentation is enforced, not hoped for:

- Every hardware artifact must have a current wiki page
  ([standards](wiki/governance/documentation-standards.md)).
- A knowledge graph ([`graph/`](graph/)) is generated from the wiki and
  kept in sync by CI.
- AI agents working here follow
  [`wiki/governance/agent-governance.md`](wiki/governance/agent-governance.md).
- Gate command (run before every commit; CI runs it too):

```bash
python3 tools/openwiki/openwiki.py check
```

## Documentation

| File | Contents |
|------|---------|
| `wiki/` | OpenWiki knowledgebase — governed, machine-readable, Confluence-ready |
| `docs/architecture.md` | System-level block diagram, I2C bus map, PCB design rules |
| `docs/components.md` | Per-component reference, datasheets, library status |
| `docs/connector-pinout.md` | J1 connector current state and intended pinout design |
| `docs/library-notes.md` | Local vs. external libraries, BMP581 reinstall steps |
| `docs/project-history.md` | Git timeline, team, submodule history, design decisions |

## Tools Required

- **KiCad 9.0** — https://www.kicad.org/download/
- **Git** (with submodule support)
- **Python 3.8+** — for `tools/openwiki/openwiki.py` (stdlib only)

## Team

| Name | Email |
|------|-------|
| pyson2k | paung@cpp.edu |
| Sebastian Graciano | sebgra518@gmail.com |
| pixelatedknight27 | maxgross72@gmail.com |
| eryn-chen | eryncchen@gmail.com |
