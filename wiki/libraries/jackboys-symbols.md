---
id: libraries/jackboys-symbols
title: jackboys Symbol Library
type: library
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-07-09
tags: [kicad, library, symbols]
documents: [jackboys.kicad_sym]
related: [libraries/jackboys2-footprints, libraries/library-tables, hardware/thermometer]
---

# jackboys Symbol Library

`jackboys.kicad_sym` is the project's custom **symbol library**. In KiCad, a *symbol* is the logical representation of a part on a schematic — a box with named pins — as opposed to a *footprint*, which is the physical copper pattern on the PCB (footprints live in [[libraries/jackboys2-footprints]]).

The library name "jackboys" is just what the original team called it; it carries no technical meaning.

## Contents

The library contains exactly **one symbol**: `MCP9600-E_MX`, the Microchip I2C thermocouple EMF-to-temperature converter used as U1 on the [[hardware/thermometer]] board.

Pin map (pin numbers refer to the physical QFN package pads):

| Pin(s) | Name | Purpose |
|--------|------|---------|
| 2 | VIN+ | Thermocouple positive input |
| 4 | VIN- | Thermocouple negative input |
| 8 | VDD | Supply (+3.3V on this board) |
| 11, 12, 14, 15 | ALERT_1..ALERT_4 | Programmable temperature alert outputs |
| 16 | ADDR | I2C address select |
| 19 | SCL | I2C clock |
| 20 | SDA | I2C data |
| 21+ | EXP | Exposed thermal pad (multiple pins for the pad) |

## Registration

The library is registered project-locally in `sym-lib-table` under the nickname `jackboys`, with the path `${KIPRJMOD}/jackboys.kicad_sym` (`${KIPRJMOD}` expands to the project directory, so it works on any machine). See [[libraries/library-tables]].

## Related file: jackboys.bak

`jackboys.bak` at the repo root is a **byte-identical KiCad auto-backup** of `jackboys.kicad_sym`. KiCad writes these automatically when saving a symbol library. It carries no extra information.

## Current state

- The library works: the single MCP9600-E_MX symbol loads and is used by the thermometer schematic.
- It contains only the one symbol. The **BMP581 symbol is NOT here** — the schematic expects it from a separate `BMP581` library that was never committed (see [[hardware/thermometer]] for that gap).
- The symbol's pin map has not been independently re-verified against the MCP9600 datasheet by the current team.

## Open work

- [ ] Verify the symbol's pin numbering/names against the Microchip MCP9600-E/MX datasheet before fabricating anything.
- [ ] Decide where the re-sourced BMP581 symbol will live — added into this library, or committed as its own library and registered in `sym-lib-table`.
- [ ] Consider deleting or gitignoring `jackboys.bak` (redundant auto-backup); record the choice.
