---
id: index
title: The Smartphone Project
type: overview
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-10-01
tags: [kicad, overview, home]
related: [hardware/thermometer, hardware/zynq-carrier-power, libraries/jackboys-symbols, libraries/jackboys2-footprints, libraries/library-tables, guides/getting-started, decisions/2025-08-digitalbot-submodule-removal, governance/documentation-standards]
---

# The Smartphone Project

This is the documentation wiki for **The Smartphone Project**, a hardware effort by the DIGITAL club at Cal Poly Pomona. The repository holds KiCad design files (KiCad is a free, open-source electronics design suite for drawing schematics and laying out printed circuit boards) for the project's first pieces of custom hardware.

## What is in this repository

The long-term goal is a student-built smartphone. What exists so far is early groundwork:

- A **thermometer daughter board** — a small sensor board (temperature via thermocouple, plus barometric pressure) designed in KiCad 9. See [[hardware/thermometer]].
- A **Zynq carrier power** design, pulled in as a git submodule from a separate repository. See [[hardware/zynq-carrier-power]].
- Two small **project-local KiCad libraries** (custom schematic symbols and footprints) that the thermometer board depends on. See [[libraries/jackboys-symbols]] and [[libraries/jackboys2-footprints]].

## Project status: paused since August 2025

Work on this repository ran from **July to August 2025** and then stopped. Key dates from the git history:

| Date | Event |
|------|-------|
| 2025-07-16 | Earliest design activity — five KiCad auto-backup zips in `thermometer-backups/` (a sixth is from 2025-07-27) |
| 2025-07-19 | First git commit (pyson2k, paung@cpp.edu) |
| 2025-08-13 | Zynq-Carrier-Power added as a submodule (pixelatedknight27 commit `0baa108`, with same-day `.gitmodules` fixes by eryn-chen) |
| 2025-08-23 to 2025-08-26 | A DIGITALBot submodule was added, reverted, re-added, and finally removed — see [[decisions/2025-08-digitalbot-submodule-removal]] |
| 2025-08-26 | Last commit of the original design work (`c81e8e5`, "Removed DititalBot Submodule" — typo in the original message) |
| 2026-02-05 | A fingerprint-sensor design zip was uploaded on the `TheFingerprintSensor` branch (never merged to main) |
| 2026-06 | Documentation preservation pass (`0a96fb0`, `b8c614a`, PR #1) |
| 2026-07-09 | OpenWiki knowledgebase added (PR #2) |

Original contributors: pixelatedknight27 (maxgross72@gmail.com, ~9 commits across two author emails), eryn-chen (eryncchen@gmail.com, 4), pyson2k (paung@cpp.edu, 2), Sebastian Graciano (sebgra518@gmail.com, 1), Angelo Duenas (personalangeloduenas@gmail.com, 1), ARussellChung (russellchungatcpp.edu@gmail.com, 1 on the TheFingerprintSensor branch).

The project was left **mid-design, not finished**: the thermometer board has an incomplete layout (no board outline, zero routed copper) and a **half-finished schematic rewiring with active miswiring** (a grounded SCL pin, swapped alert labels, unpowered chips) plus one missing library (the BMP581 sensor's symbol/footprint library was never committed). Each subsystem page below lists exactly what is unfinished.

## Subsystems and pages

| Page | What it covers |
|------|----------------|
| [[hardware/thermometer]] | The thermometer daughter board (`thermometer.kicad_pro`) — design intent, current state, open work |
| [[hardware/zynq-carrier-power]] | The Zynq-Carrier-Power git submodule |
| [[libraries/jackboys-symbols]] | Custom symbol library `jackboys.kicad_sym` (MCP9600 symbol) |
| [[libraries/jackboys2-footprints]] | Custom footprint library `jackboys2.pretty` (MCP9600 QFN footprint) |
| [[libraries/library-tables]] | How `sym-lib-table` and `fp-lib-table` wire the libraries into the project |
| [[guides/getting-started]] | Step-by-step setup for new members |
| [[decisions/2025-08-digitalbot-submodule-removal]] | Decision record: the DIGITALBot submodule saga |

## Where to start

1. **New to the project?** Read [[guides/getting-started]] first. It walks through cloning (including the submodule step), installing KiCad, opening the project, and the one known error you will hit.
2. **Before changing anything**, read the governance pages: [[governance/documentation-standards]] (any change to a design artifact requires a matching wiki update), [[governance/agent-governance]], and [[governance/confluence-sync]].
3. **Wondering why something looks odd in the history?** Check [[decisions/2025-08-digitalbot-submodule-removal]] before re-attempting any DIGITALBot integration.

## Repository housekeeping notes

- `fp-info-cache` (~4 MB) is an auto-generated KiCad footprint cache, not authored content. Do not hand-edit it and do not document it.
- `thermometer-backups/` holds six timestamped KiCad auto-backup zips (historical record only; exempt from documentation governance).
- `jackboys.bak` is a byte-identical KiCad auto-backup of `jackboys.kicad_sym`.
