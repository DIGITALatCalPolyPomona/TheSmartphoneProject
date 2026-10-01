---
id: hardware/thermometer
title: Thermometer Daughter Board
type: hardware
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-10-01
tags: [kicad, sensor, daughter-board]
documents: [thermometer.kicad_pro, thermometer.kicad_sch, thermometer.kicad_pcb]
related: [libraries/jackboys-symbols, libraries/jackboys2-footprints, index]
---

# Thermometer Daughter Board

The thermometer board is a small **daughter board** (a secondary board that plugs into a larger main board) that measures temperature and barometric pressure. It is the main design in this repository. The commit message for dfb0be3 sums up the intent: "Added bmp581 Pressure Sensor to temperature sensor daughter board".

## Files

The KiCad project consists of three core files at the repo root:

- `thermometer.kicad_pro` — the project file (open this one in KiCad).
- `thermometer.kicad_sch` — the schematic (the circuit diagram; format 20250114, i.e. KiCad 9.0).
- `thermometer.kicad_pcb` — the board layout (the physical copper design; format 20241229). 2 copper layers, 1.6 mm board thickness (the standard PCB default).

(Also present: `thermometer.kicad_prl`, a per-user local-settings file KiCad regenerates; and the sibling `sym-lib-table`/`fp-lib-table` that wire in the project's own libraries.)

Auto-backup zips of earlier versions live in `thermometer-backups/` (five from 2025-07-16, one from 2025-07-27). They are a historical record only.

## What is on the board

| Ref | Part | Role |
|-----|------|------|
| U1 | Microchip **MCP9600-E/MX** | I2C thermocouple EMF-to-temperature converter — reads the tiny voltage a thermocouple produces and converts it to a digital temperature over I2C (a common two-wire chip-to-chip bus: SCL clock + SDA data). Uses the custom symbol from [[libraries/jackboys-symbols]] and footprint `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX` from [[libraries/jackboys2-footprints]] (5 x 5 mm body, 0.65 mm pin pitch; 30 pad objects implementing 21 unique electrical connections). |
| U2 | Bosch **BMP581** | Barometric pressure sensor. **Its library is missing from the repo — see below.** |
| TC1 | `Device:Thermocouple` | The thermocouple sensing element (from KiCad's built-in libraries). Schematic only — no footprint/connector assigned yet. |
| J1 | 7-pin header, 1.00 mm pitch | Connector to the parent board (`Connector_PinHeader_1.00mm:PinHeader_1x07_P1.00mm_Vertical`). Footprint assigned PCB-side only — the schematic Footprint field is blank. |

Power is +3.3V and GND. The schematic is a single sheet ("Root" — KiCad projects can have a hierarchy of sheets; this one doesn't).

## Known gap: missing BMP581 library

The schematic references a **`BMP581` symbol and footprint library that was never committed** — it is not in `sym-lib-table` or `fp-lib-table` (see [[libraries/library-tables]]) and the library files existed only on the original author's machine. U2 still *displays* in the schematic because the symbol is embedded in the file's `lib_symbols` cache — but the link is broken: the symbol cannot be updated from the library, the footprint cannot be resolved for PCB placement/sync, and KiCad surfaces missing-library warnings. The library must be re-sourced (e.g. downloaded from SnapEDA or the manufacturer) or recreated, then registered in the project library tables.

## Current state (honest assessment — the design is unfinished AND mid-refactor)

The project was paused mid-design in August 2025 — and the schematic was left
**halfway through a rewiring that introduced real defects**. The PCB netlist
predates the rewire: it still shows an older, self-consistent arrangement
(U1 pads 1–18 to GND/VDD, TC1 to VIN±, everything else `unconnected-`) that no
longer matches the schematic. "Update PCB from Schematic" must NOT be run
until the schematic is fixed — it would import the miswiring.

### Schematic wiring defects (verified against `thermometer.kicad_sch` geometry)

- **U1 pin 19 (SCL) is tied to GND** — GND power symbol `#PWR06` sits exactly on the pin. A shorted I2C clock line.
- **U1 pin 16 (ADDR) is wired into the SCL net** — together with **U2 pin 6 (CSB)**. The SCL label attaches to this wire; it does not reach U1's actual SCL pin.
- **U1 pin 20 (SDA) is unconnected** — the SDA labels dangle on empty wire stubs.
- **ALERT_2/ALERT_4 labels are swapped** on U1: pin 12 (physical ALERT_2) carries `ALERT_4`, pin 15 (physical ALERT_4) carries `ALERT_2`. Pin 14→`ALERT_3` is correct; pin 11 (ALERT_1) is bare and its label dangles.
- **U1 power is not wired:** VDD (pin 8) and the 10-pin stacked GND group are unconnected; the nearby `#PWR01` +3.3V and `#PWR02` GND symbols dangle on stubs that touch nothing.
- **TC1 does not reach U1** — its wires dead-end ~15 mm below VIN+/VIN- (pins 2/4).
- **U2 (BMP581) is miswired:** pin 2 (SCK/SCL) → +3.3V, pin 5 (SDO/ADR) → `INT` net, pin 7 (INT) → GND; pin 4 (SDI/SDA), pin 1 (VDDIO), and GND pins 3/8/9 are unconnected. Only pin 10 (VDD) → +3.3V is right.
- **J1 IS wired — a pinout exists** (J1 is horizontally mirrored so its pins land on the label row): pin 1=`INT`, 2=`ALERT_4`, 3=`ALERT_3`, 4=`ALERT_2`, 5=`ALERT_1`, 6=`SDA`, 7=`SCL`. But **no J1 pin carries +3.3V or GND** — the board's power delivery is unresolved, a design defect beyond wiring repair.
- Because the labels land on J1's pins, the miswired nets propagate end-to-end: net `SCL` = J1.7 + U1.**ADDR** + U2.**CSB**; net `INT` = J1.1 + U2.**SDO/ADR**; net `SDA` = J1.6 only.
- **Dangling annotation labels** `0x60`, `0x46`, `IgnorePin` (and a second set of SCL/SDA/ALERT labels) are comments-by-label — they touch no pin and prove nothing electrically (the "0x60 = ADDR grounded" reading in older docs was wrong; ADDR is on the SCL net).
- **U1 EXP pads (21–30) float** on an anonymous net — not tied to GND per datasheet requirement. (The `IgnorePin` label near them attaches to nothing.)

### PCB / layout state

- **No board outline.** The Edge.Cuts layer (KiCad's layer for the physical board edge) has nothing drawn on it.
- **No copper at all** — zero `(segment`/`(via`/`(zone` objects; every net is unrouted.
- **U1 + J1 footprints placed; U2 absent** (its footprint cannot resolve — see library gap below).
- **No schematic title block** (title, revision, date are blank). Single "Root" sheet.

In short: the schematic needs wiring repair before any PCB work is meaningful.

## Open work

- [ ] **Fix the schematic wiring** (the whole defect list above): U1 SCL pin off GND, ADDR wired correctly (default 0x60 needs ADDR=GND per MCP9600 convention), ALERT_2/4 labels un-swapped, SDA connected to U1 pin 20, U1 VDD/GND powered, TC1→VIN± connected, U2 pins corrected (SCL off +3.3V, CSB→+3.3V for I2C mode, SDO→GND for 0x46, INT off GND), EXP pads tied to GND, dangling labels removed.
- [ ] Decide the J1 power question — all 7 pins are assigned to signals; +3.3V/GND need pins or another path from the host.
- [ ] Re-source or recreate the BMP581 symbol and footprint; commit the library and register it in `sym-lib-table` / `fp-lib-table`.
- [ ] Assign J1's footprint in the schematic (currently blank — set PCB-side only), place U2's footprint in the PCB, THEN run "Update PCB from Schematic" to reconcile the stale netlist.
- [ ] Assign a footprint/connector for TC1.
- [ ] Draw the board outline on Edge.Cuts and decide the physical form factor.
- [ ] Fill in the schematic title block (title, revision, date, author).
- [ ] Add decoupling capacitors (none exist in schematic or PCB) per MCP9600/BMP581 datasheets.
- [ ] Run KiCad's ERC (Electrical Rules Check, schematic) and DRC (Design Rules Check, layout) and clear the errors.
- [ ] Update this page (per [[governance/documentation-standards]]) as each item lands.
