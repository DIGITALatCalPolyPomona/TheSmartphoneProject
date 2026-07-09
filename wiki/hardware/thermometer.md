---
id: hardware/thermometer
title: Thermometer Daughter Board
type: hardware
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-07-09
tags: [kicad, sensor, daughter-board]
documents: [thermometer.kicad_pro]
related: [libraries/jackboys-symbols, libraries/jackboys2-footprints, index]
---

# Thermometer Daughter Board

The thermometer board is a small **daughter board** (a secondary board that plugs into a larger main board) that measures temperature and barometric pressure. It is the main design in this repository. The commit message for dfb0be3 sums up the intent: "Added bmp581 Pressure Sensor to temperature sensor daughter board".

## Files

The KiCad project consists of three files at the repo root:

- `thermometer.kicad_pro` — the project file (open this one in KiCad).
- `thermometer.kicad_sch` — the schematic (the circuit diagram; format 20250114, i.e. KiCad 9.0).
- `thermometer.kicad_pcb` — the board layout (the physical copper design; format 20241229). 2 copper layers, 1.6 mm board thickness (the standard PCB default).

Auto-backup zips of earlier versions live in `thermometer-backups/` (five from 2025-07-16, one from 2025-07-27). They are a historical record only.

## What is on the board

| Ref | Part | Role |
|-----|------|------|
| U1 | Microchip **MCP9600-E/MX** | I2C thermocouple EMF-to-temperature converter — reads the tiny voltage a thermocouple produces and converts it to a digital temperature over I2C (a common two-wire chip-to-chip bus: SCL clock + SDA data). Uses the custom symbol from [[libraries/jackboys-symbols]] and footprint `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX` from [[libraries/jackboys2-footprints]] (5 x 5 mm, 21-pad QFN, 0.65 mm pin pitch). |
| U2 | Bosch **BMP581** | Barometric pressure sensor. **Its library is missing from the repo — see below.** |
| TC1 | `Device:Thermocouple` | The thermocouple sensing element (from KiCad's built-in libraries). |
| J1 | 7-pin header, 1.00 mm pitch | Connector to the parent board (`Connector_PinHeader_1.00mm:PinHeader_1x07_P1.00mm_Vertical`). |

Power is +3.3V and GND. The schematic is a single sheet ("Root" — KiCad projects can have a hierarchy of sheets; this one doesn't).

## Known gap: missing BMP581 library

The schematic references a **`BMP581` symbol and footprint library that was never committed** — it is not in `sym-lib-table` or `fp-lib-table` (see [[libraries/library-tables]]) and the library files existed only on the original author's machine. On a fresh clone, KiCad shows a **missing-library error for U2** when you open the schematic. The library must be re-sourced (e.g. downloaded from SnapEDA or the manufacturer) or recreated, then registered in the project library tables.

## Current state (honest assessment — the design is unfinished)

The project was paused mid-design in August 2025. As of the pause:

- **No board outline.** The Edge.Cuts layer (KiCad's layer for the physical board edge) has nothing drawn on it, so the board has no defined shape or size.
- **Most nets are unrouted.** The MCP9600's I2C lines (SCL/SDA), ADDR, and ALERT_1 through ALERT_4, plus **all 7 pins of J1**, are unrouted/unconnected on the PCB.
- **U2 (BMP581) cannot load** on a fresh machine due to the missing library above.
- **No schematic title block** (title, revision, date are blank).
- Single "Root" sheet; no hierarchy, which is fine at this size but worth knowing.

In short: the schematic captures the design intent, but the PCB layout is at an early stage and the project does not pass a completeness check.

## Open work

- [ ] Re-source or recreate the BMP581 symbol and footprint; commit the library and register it in `sym-lib-table` / `fp-lib-table`.
- [ ] Draw the board outline on Edge.Cuts and decide the physical form factor.
- [ ] Define/verify the J1 pinout against whatever parent board this plugs into, and connect all 7 pins in the schematic and layout.
- [ ] Route SCL, SDA, ADDR, and ALERT_1..4 from the MCP9600.
- [ ] Fill in the schematic title block (title, revision, date, author).
- [ ] Run KiCad's ERC (Electrical Rules Check, schematic) and DRC (Design Rules Check, layout) and clear the errors.
- [ ] Review the MCP9600 and BMP581 datasheets for required decoupling/support passives and confirm the schematic matches.
- [ ] Update this page (per [[governance/documentation-standards]]) as each item lands.
