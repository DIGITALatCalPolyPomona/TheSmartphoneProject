---
id: guides/getting-started
title: Getting Started for New Members
type: guide
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-10-01
tags: [guide, onboarding, kicad]
related: [index, hardware/thermometer, hardware/zynq-carrier-power, libraries/library-tables, governance/documentation-standards]
---

# Getting Started for New Members

This guide takes you from zero to having the project open in KiCad, and tells you about the one error you *will* hit so it doesn't scare you. No prior experience with this project is assumed — the original team paused work in August 2025 and this wiki is the handover.

## 1. Clone the repository (including the submodule)

This repo contains a **git submodule** — a folder (`Zynq-Carrier-Power/`) that is really a pointer to a separate repository. A plain `git clone` leaves that folder **empty**; you must initialize it explicitly:

```bash
git clone <repo-url> TheSmartphoneProject
cd TheSmartphoneProject
git submodule update --init
```

(Or do it in one step: `git clone --recurse-submodules <repo-url>`.)

If you skip the submodule step, nothing else breaks — the thermometer project is independent — but `Zynq-Carrier-Power/` will just be an empty directory. See [[hardware/zynq-carrier-power]].

## 2. Install KiCad 9.0 or newer

The design files were saved with **KiCad 9.0** (schematic format 20250114, board format 20241229). Older KiCad versions cannot open them. Download from https://www.kicad.org/download/ for your OS. KiCad is free and open source; the parts you will use are:

- **Schematic Editor** (Eeschema) — the circuit diagram.
- **PCB Editor** (Pcbnew) — the physical board layout.

## 3. Open the project

Start KiCad and open **`thermometer.kicad_pro`** at the repo root (File > Open Project). Always open the `.kicad_pro` project file, not the `.kicad_sch` or `.kicad_pcb` directly — the project context pulls in the sibling `sym-lib-table`/`fp-lib-table` files that register the project-local libraries.

## 4. How the libraries resolve (and why it "just works")

The project uses **project-local library tables** (`sym-lib-table` and `fp-lib-table` at the repo root) with paths written as `${KIPRJMOD}/...`. `${KIPRJMOD}` is a KiCad variable meaning "the folder the project file is in", so the custom `jackboys` symbol library and `jackboys2` footprint library resolve on any machine with no setup. Details in [[libraries/library-tables]].

## 5. The one error you WILL see: missing BMP581 library

U2 (the Bosch BMP581 pressure sensor) still **displays** in the schematic — its symbol is embedded in the file's `lib_symbols` cache — but its library link is broken: KiCad warns about the missing `BMP581` library, the symbol can't be updated from a library, and the footprint can't resolve for PCB sync. This is not something you broke. The original author kept the `BMP581` symbol/footprint library only on their own machine — it was never committed to the repo and never added to the library tables.

What to do:

- **Short term:** acknowledge the warning and keep working; U1 (MCP9600), TC1, and J1 all load fine.
- **To actually fix it:** re-source the BMP581 symbol and footprint (e.g. from SnapEDA or Bosch), commit the library files, register them in `sym-lib-table` / `fp-lib-table`, and update [[hardware/thermometer]] and [[libraries/library-tables]]. This is the top item on the project's open-work list.

## 6. Know what state the design is in

Read [[hardware/thermometer]] before assuming anything works. Headline: the PCB has **no board outline and zero routed copper**, and the schematic itself was paused **mid-rewiring with active defects** (a grounded SCL pin, swapped alert labels, unpowered chips). The design was paused mid-flight, not finished — fix the schematic before touching the layout.

## 7. The documentation rule (read before you change anything)

This repo is governed by a documentation-as-code policy: **any change to a design artifact (schematics, PCB, libraries, library tables, submodules) requires a matching update to its wiki page in the same change**, and the wiki must pass the checker:

```bash
python3 tools/openwiki/openwiki.py check
```

(On Windows the interpreter may be `python` or `py` instead of `python3`.)

Run that before committing. The full rules are in [[governance/documentation-standards]]; also see [[governance/agent-governance]] and [[governance/confluence-sync]] for how automation and the Confluence export interact with the wiki. Notable exemptions from the policy: `fp-info-cache` (an auto-generated ~4 MB KiCad cache) and `thermometer-backups/` (historical auto-backup zips) — the full `ignore` list lives in `openwiki.config.json`.

## 8. Suggested first tasks

1. Open the thermometer schematic and PCB and cross-check them against [[hardware/thermometer]].
2. Initialize the submodule and inspect [[hardware/zynq-carrier-power]] — its description needs verification.
3. Pick an item from a page's "Open work" checklist; the BMP581 library fix is the highest-value starter task.
