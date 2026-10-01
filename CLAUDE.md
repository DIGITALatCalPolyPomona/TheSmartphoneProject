# CLAUDE.md — TheSmartphoneProject

## Project Type

KiCad 9.0 hardware EDA project. This is a PCB design, NOT a software project.
Do not look for package.json, CMakeLists.txt, Makefile, or source code files.

## What This Is

A thermometer/environmental sensor daughter board designed for the Cal Poly Pomona
DIGITALatCalPolyPomona organization. Measures temperature via thermocouple + MCP9600
amplifier and barometric pressure via BMP581. Both sensors communicate over I2C.
Intended to plug into the Zynq-Carrier-Power host board via J1 connector.

**Status:** Abandoned August 2025. Preserved for future resumption.

## Knowledgebase & Binding Rules

The knowledgebase lives in `wiki/` (OpenWiki) and is **governed**: documentation is
not optional here, because the team turns over yearly and this project already got
abandoned once for lack of it.

Full rules: `wiki/governance/agent-governance.md`. Non-negotiables:

1. Before touching any hardware/library file, read `wiki/index.md` and the
   wiki page that documents that file (the page lists it in its `documents`
   frontmatter). No page? Write one first (`openwiki new`).
2. Every change to a governed artifact updates its wiki page in the same
   branch (content + `updated` date).
3. Before declaring any work done:
   `python3 tools/openwiki/openwiki.py graph`   (regenerate knowledge graph)
   `python3 tools/openwiki/openwiki.py check`   (must pass — CI runs it too)
4. Never hand-edit `graph/` or `build/` (generated), never set a page's
   status to `verified` (humans only), never delete wiki pages or decision
   records (archive instead).
5. Irreversible/architectural changes need a decision page under
   `wiki/decisions/` first.

When asked to verify docs for some work:
`python3 tools/openwiki/openwiki.py verify` — report its output verbatim
(coverage gaps, stale pages, stubs).

## Key Files

| File | Purpose |
|------|---------|
| `thermometer.kicad_sch` | Schematic (KiCad 9.0 S-expression format) |
| `thermometer.kicad_pcb` | PCB layout (KiCad 9.0 S-expression format) |
| `thermometer.kicad_pro` | Project settings and design rules (JSON) |
| `jackboys.kicad_sym` | Custom symbol library (MCP9600-E_MX only) |
| `jackboys2.pretty/` | Custom footprint library (MCP9600 QFN-30 only) |
| `fp-lib-table` | Footprint library search paths |
| `sym-lib-table` | Symbol library search paths |
| `wiki/` | OpenWiki knowledgebase (Markdown + frontmatter) |
| `graph/` | Generated knowledge graph (JSON + Mermaid) — do not hand-edit |
| `tools/openwiki/openwiki.py` | Validator / graph builder / coverage auditor / Confluence exporter |
| `openwiki.config.json` | Which artifacts are governed |
| `thermometer-backups/` | Timestamped KiCad backup archives |

## CRITICAL: Missing External Library

The BMP581 symbol and footprint are referenced as `BMP581:BMP581` but this library
is **NOT stored in this repository**. The project will show missing library errors
when opened in KiCad until this is reinstalled.

**To restore:** Download KiCad format from SnapEDA, then copy into repo as local libraries:
- `BMP581.kicad_sym` (symbol)
- `BMP581.pretty/BMP581.kicad_mod` (footprint)
- Update `sym-lib-table` and `fp-lib-table` to point to local paths

See `docs/library-notes.md` for detailed instructions.

## KiCad File Format Notes

- `.kicad_sch` and `.kicad_pcb` use S-expression text format (human-readable).
- Components in schematic are `(symbol ...)` blocks with Reference/Value/Footprint properties.
- Placed components in PCB are `(footprint ...)` blocks.
- Net names prefixed with `unconnected-` mean the pin has no connection in the PCB.
- Global labels in the schematic represent named signals (SCL, SDA, ALERT_1, etc.).

## Current Design State

- **Schematic:** U1 (MCP9600) and U2 (BMP581) both placed and wired
- **PCB:** Only U1 and J1 footprints placed — U2 (BMP581) not yet added to PCB
- **Routing:** No copper traces routed anywhere
- **Board outline:** Edge.Cuts layer is empty (no board shape defined)
- **J1 connector:** All 7 pins are unconnected (nets 13–19 all `unconnected-` prefixed)
- **U1 SCL/SDA:** NOT wired to SCL/SDA global labels — U1 pins 19 and 20 are unconnected in both schematic and PCB
- **U1 EXP pad (pads 21–30):** NOT connected to GND — forms isolated net `Net-(U1-EXP-Pad21)` (design issue, must be fixed)
- **IgnorePin label:** An unusual `global_label "IgnorePin"` exists at schematic coordinate (96.52, 67.31) — purpose unclear, connected to a pin near U1

## Known Design Issues (to fix on resumption)

1. MCP9600 EXP thermal pad not connected to GND (pads 21–30 floating)
2. MCP9600 SCL/SDA pins not connected in schematic
3. MCP9600 ALERT_1–4 pins not connected in schematic
4. J1 pinout undefined — all 7 pins unconnected
5. U2 BMP581 not placed in PCB
6. No board outline defined
7. BMP581 library not in project lib tables (relies on global KiCad install)

## Available Skills

- `/review-changes` — Reviews KiCad file changes (git diff) and identifies which docs need updating
- `/update-docs` — Audits all documentation against current KiCad design state and proposes/applies updates

## Submodule Notes

- **Zynq-Carrier-Power:** Still in `.gitmodules`, points to `https://github.com/eryn-chen/Zynq-Carrier-Power`
  (branch: master). Directory is empty — was never initialized. This is the intended host board.
  Run `git submodule update --init` to populate it.
- **DIGITALBot:** Removed in commit `c81e8e5`. Not relevant to this hardware project.

## Documentation Index

| File | Contents |
|------|---------|
| `README.md` | Project overview, hardware summary, getting started |
| `wiki/` | OpenWiki knowledgebase — governed, machine-readable |
| `docs/architecture.md` | System context, block diagram, I2C bus, PCB parameters |
| `docs/components.md` | Per-component reference with datasheets and library status |
| `docs/connector-pinout.md` | J1 connector status and intended pinout design |
| `docs/library-notes.md` | Local and external library tracking, reinstall instructions |
| `docs/project-history.md` | Git timeline, submodule history, design decisions |
