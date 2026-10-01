---
id: hardware/zynq-carrier-power
title: Zynq Carrier Power (submodule)
type: hardware
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-10-01
tags: [kicad, power, zynq, submodule]
documents: [Zynq-Carrier-Power]
related: [index, guides/getting-started]
---

# Zynq Carrier Power (submodule)

`Zynq-Carrier-Power/` is not ordinary content of this repository — it is a **git submodule**, meaning it is a pointer to a specific commit of a *separate* repository that git checks out into this folder on request.

## Submodule facts

| Field | Value |
|-------|-------|
| Path | `Zynq-Carrier-Power/` |
| URL | https://github.com/eryn-chen/Zynq-Carrier-Power |
| Branch | `master` |
| Added | 2025-08-13 by pixelatedknight27 (commit `0baa108`, "added power carrier as submodule"; same-day `.gitmodules` fixes by eryn-chen) |
| Pinned commit | `7aed9fc` — still the tip of upstream `master` as of Oct 2026 |

These settings live in `.gitmodules` at the repo root.

## What it is

Now verified from the populated submodule: it is a KiCad 9 project whose own
README describes it as **"Zynq-Carrier-Template — a template Daughterboard for
pinguz97's Zynq-SoM"** (a Zynq is a chip combining ARM processor cores with
FPGA fabric; a "carrier board" is the larger board a compute module mounts
onto). Contents on disk: `Zynq-Carrier-Power.kicad_pro`/`.kicad_sch`/`.kicad_pcb`
(plus a `.kicad_dru` rules file) and an `Imports/` library set — a Zynq SoM
module on a DF40C-100DP mezzanine connector, a BQ25629RYKR battery charger,
a USB4105GFA USB-C connector, JST connectors, and a 1 µH inductor with 3D
models.

In this project it serves as the intended **host/power board** the thermometer
daughter board plugs into via J1.

## Getting the contents

After a normal `git clone`, the `Zynq-Carrier-Power/` directory is **empty** —
expected submodule behavior, not a broken checkout. To populate it:

```bash
git submodule update --init
```

(Some checkouts — including the maintainer's working copy — already have it
populated.) See [[guides/getting-started]] for the full setup flow.

## Current state

- Initialized and populated on the maintainer's checkout; pins `7aed9fc`,
  still upstream `master`'s tip (other upstream branches exist: `colab-2`,
  `collab`, `footprint-update`).
- No design review, status notes, or interface documentation for this board
  exist in this wiki — and no J1-compatible mate (1.00 mm, 7-pin) was found in
  its connectors (it uses USB-C, barrel jack, 2.54 mm headers, JST, and the
  DF40C SoM connector), so the thermometer's host interface is unresolved.
- KiCad lock file `~Zynq-Carrier-Power.kicad_pcb.lck` was observed — the board
  has been opened in KiCad recently; treat its design state as unreviewed.

## Open work

- [x] ~~Run `git submodule update --init` and inspect the actual contents~~ — done Oct 2026 (description above is now verified).
- [x] ~~Confirm the upstream repository is still accessible~~ — cloned fine Oct 2026; pinned commit is still `master`'s tip.
- [ ] Document how the thermometer board's J1 mates to this carrier — no matching connector was found in the submodule; likely a wiring/cable interface or a carrier revision is needed.
- [ ] Decide whether a submodule is still the right structure (upstream is a personal repo of a former contributor — consider forking into a club-owned org), and record any change as a decision page (compare [[decisions/2025-08-digitalbot-submodule-removal]]).
