---
id: libraries/library-tables
title: KiCad Library Tables
type: library
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-07-09
tags: [kicad, library, configuration]
documents: [fp-lib-table, sym-lib-table]
related: [libraries/jackboys-symbols, libraries/jackboys2-footprints, hardware/thermometer]
---

# KiCad Library Tables

KiCad finds symbol and footprint libraries through **library tables**: small text files that map a short *nickname* to a library's location on disk. There are two kinds — a symbol library table and a footprint library table — and each exists at two levels: a *global* one in your KiCad user settings, and an optional *project-local* one sitting next to the project file. This repository uses **project-local** tables, which is what makes the project portable: everything it needs (except KiCad's built-in libraries) travels with the repo.

## sym-lib-table (symbol libraries)

Registers one library:

| Nickname | Path | Documented at |
|----------|------|---------------|
| `jackboys` | `${KIPRJMOD}/jackboys.kicad_sym` | [[libraries/jackboys-symbols]] |

## fp-lib-table (footprint libraries)

Registers one library:

| Nickname | Path | Documented at |
|----------|------|---------------|
| `jackboys2` | `${KIPRJMOD}/jackboys2.pretty` | [[libraries/jackboys2-footprints]] |

## How ${KIPRJMOD} works

`${KIPRJMOD}` is a KiCad path variable that expands to **the directory containing the open project file**. Because both entries use it, the libraries resolve correctly on any machine where the repo is cloned — no per-user configuration needed. When you open `thermometer.kicad_pro`, a schematic reference like `jackboys:MCP9600-E_MX` or a footprint reference like `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX` is looked up via these tables.

## What is deliberately NOT in the tables

The thermometer schematic also references a **`BMP581` library** (symbol and footprint for U2, the Bosch pressure sensor). That library is **absent from both tables and from the repo** — it existed only on the original author's machine. This is why a fresh clone shows a missing-library error for U2. Fixing it means committing a BMP581 library **and adding it to these tables** — doing only one of the two is not enough. See [[hardware/thermometer]].

## Editing the tables

Prefer editing through KiCad (Preferences > Manage Symbol Libraries / Manage Footprint Libraries, "Project Specific Libraries" tab) rather than hand-editing the s-expression text, and always use `${KIPRJMOD}`-relative paths — an absolute path would break the project for everyone else. Any change to these files requires a matching wiki update (see [[governance/documentation-standards]]).

## Current state

- Both tables are version 7, each with a single working entry.
- The `BMP581` library entry is missing (see above) — this is the only known defect.

## Open work

- [ ] When the BMP581 symbol/footprint is re-sourced, register it in `sym-lib-table` and `fp-lib-table` with `${KIPRJMOD}` paths, and update this page and [[hardware/thermometer]].
