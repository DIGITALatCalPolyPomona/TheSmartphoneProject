---
id: libraries/jackboys2-footprints
title: jackboys2 Footprint Library
type: library
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-07-09
tags: [kicad, library, footprints]
documents: [jackboys2.pretty]
related: [libraries/jackboys-symbols, libraries/library-tables, hardware/thermometer]
---

# jackboys2 Footprint Library

`jackboys2.pretty/` is the project's custom **footprint library**. In KiCad, a *footprint* is the physical land pattern for a part — the copper pads, outlines, and dimensions that get etched onto the PCB. A `.pretty` folder is simply KiCad's format for a footprint library: a directory containing one `.kicad_mod` file per footprint.

The name "jackboys2" is the original team's naming (companion to the `jackboys` symbol library, see [[libraries/jackboys-symbols]]); it has no technical meaning.

## Contents

The library contains exactly **one footprint**:

- `QFN65P500X500X100-21N_MCP9600-E_MX.kicad_mod` — the package for the Microchip MCP9600-E/MX (U1 on the [[hardware/thermometer]] board). Decoding the name: a **QFN** (Quad Flat No-lead, a leadless surface-mount package) with **0.65 mm pin pitch**, **5.0 x 5.0 mm** body, **21 pads** (20 perimeter pads plus the exposed thermal pad). KiCad 9 format.

## Registration

Registered project-locally in `fp-lib-table` under the nickname `jackboys2`, path `${KIPRJMOD}/jackboys2.pretty` (`${KIPRJMOD}` expands to the project directory). The schematic references it as `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX`. See [[libraries/library-tables]].

## Current state

- The library works: the single footprint loads and is assigned to U1.
- Only the MCP9600 footprint exists. The **BMP581 footprint is NOT here** — like its symbol, it was expected from an uncommitted `BMP581` library (see [[hardware/thermometer]]).
- The footprint has not been re-verified against the MCP9600 package drawing by the current team, and the board has never been fabricated, so the footprint is unproven in practice.

## Open work

- [ ] Verify pad sizes, pitch, and the exposed-pad geometry against the MCP9600-E/MX package drawing in the Microchip datasheet before ordering boards.
- [ ] Re-source or recreate the BMP581 footprint and decide whether it goes in this library or its own `.pretty` folder registered in `fp-lib-table`.
- [ ] Check the footprint's 3D model assignment (nice-to-have for visual review; likely absent).
