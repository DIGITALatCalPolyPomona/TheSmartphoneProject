# TheSmartphoneProject — Thermometer Sensor Daughter Board

**Organization:** DIGITALatCalPolyPomona (Cal Poly Pomona)
**Status:** Abandoned August 2025. Preserved for future resumption.
**Last commit:** `c81e8e5` — "Removed DIGITALBot Submodule" (2025-08-26)

---

## What This Is

A KiCad 9.0 PCB design for a compact thermometer and environmental sensor daughter board.
Measures temperature via an external thermocouple (using the MCP9600 amplifier IC) and
barometric pressure (using the BMP581 sensor). Both sensors communicate over a shared I2C
bus exposed on a 7-pin 1mm-pitch header (J1) for connection to a host board.

The host board was intended to be the [Zynq-Carrier-Power](https://github.com/eryn-chen/Zynq-Carrier-Power)
(a Zynq-7000 FPGA carrier board by eryn-chen). The Zynq acts as the I2C master.

---

## Hardware Summary

| Ref | Part | Function | Package | I2C Address | Status |
|-----|------|----------|---------|-------------|--------|
| U1 | MCP9600-E_MX | Thermocouple amplifier + cold-junction compensation | QFN-30 (5×5mm) | 0x60 | Schematic + PCB (unrouted) |
| U2 | BMP581 | Barometric pressure + temperature sensor | LGA-10 (2×2mm) | 0x46 (SDO=GND) | Schematic only |
| TC1 | Thermocouple | External temperature probe | External | — | Schematic only, no footprint |
| J1 | 7-pin 1mm header | Interface to host board | 1mm pitch THT | — | PCB placed, all pins unconnected |

Power: 3.3V from host via J1. No local regulation.

---

## What Is Complete

- Schematic: U1 (MCP9600) and U2 (BMP581) both placed and wired with I2C and power signals
- Custom MCP9600 symbol library: `jackboys.kicad_sym`
- Custom MCP9600 QFN-30 footprint: `jackboys2.pretty/`
- U1 and J1 footprints placed on PCB

## What Is Incomplete

- **PCB routing:** No copper traces — board is fully unrouted
- **Board outline:** Edge.Cuts layer is empty; no board dimensions defined
- **U2 BMP581:** Present in schematic but not placed in PCB layout
- **TC1 thermocouple:** No footprint assigned; connector type not chosen
- **J1 pinout:** All 7 pins unconnected; signals not wired to J1 in schematic or PCB
- **U1 I2C wiring:** MCP9600 SCL/SDA pins (19/20) are NOT wired to the SCL/SDA global labels in the schematic — U1 is currently isolated from the I2C bus
- **U1 ALERT wiring:** MCP9600 ALERT_1–4 pins are also not wired in the schematic
- **U1 EXP pad:** MCP9600 exposed thermal pad (pads 21–30) is not connected to GND — forms an isolated net (design issue)
- **Decoupling capacitors:** None placed anywhere on PCB
- **BMP581 library:** Not in project lib tables — must reinstall from SnapEDA (see below)

---

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

---

## Repository Structure

```
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
├── thermometer-backups/          # 6 pre-git KiCad backup archives
├── Zynq-Carrier-Power/           # Submodule (empty — see below)
├── CLAUDE.md                     # Claude Code context
├── README.md                     # This file
└── docs/                         # Design documentation
    ├── architecture.md
    ├── components.md
    ├── connector-pinout.md
    ├── library-notes.md
    └── project-history.md
```

---

## Submodule: Zynq-Carrier-Power

The `Zynq-Carrier-Power` directory is a git submodule referencing
https://github.com/eryn-chen/Zynq-Carrier-Power (branch: master).
It was never populated and the directory is empty.

To initialize it: `git submodule update --init --recursive`

---

## Documentation

| File | Contents |
|------|---------|
| `docs/architecture.md` | System-level block diagram, I2C bus map, PCB design rules |
| `docs/components.md` | Per-component reference, datasheets, library status |
| `docs/connector-pinout.md` | J1 connector current state and intended pinout design |
| `docs/library-notes.md` | Local vs. external libraries, BMP581 reinstall steps |
| `docs/project-history.md` | Git timeline, team, submodule history, design decisions |

---

## Tools Required

- **KiCad 9.0** — https://www.kicad.org/download/
- **Git** (with submodule support)

---

## Team

| Name | Email |
|------|-------|
| pyson2k | paung@cpp.edu |
| Sebastian Graciano | sebgra518@gmail.com |
| pixelatedknight27 | maxgross72@gmail.com |
| eryn-chen | eryncchen@gmail.com |
