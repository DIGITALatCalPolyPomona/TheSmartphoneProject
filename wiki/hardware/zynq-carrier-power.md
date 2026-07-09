---
id: hardware/zynq-carrier-power
title: Zynq Carrier Power (submodule)
type: hardware
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-07-09
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
| Added | 2025-08-13 by eryn-chen (commit message: "added power carrier as submodule") |

These settings live in `.gitmodules` at the repo root.

## What it is

Based on the name and the surrounding project, this is a **power-supply design for a carrier board hosting a Xilinx Zynq SoC** (a Zynq is a chip combining ARM processor cores with FPGA fabric; a "carrier board" is the larger board a compute module mounts onto). **Note: this description is an inference from the repository name** — the original team did not document it here. Whoever picks this up should open the submodule's own contents (and its repo on GitHub) and confirm, then update this page.

## Getting the contents

After a normal `git clone`, the `Zynq-Carrier-Power/` directory is **empty**. That is expected submodule behavior, not a broken checkout. To populate it, run from the repo root:

```bash
git submodule update --init
```

See [[guides/getting-started]] for the full setup flow.

## Current state

- The directory is empty on a fresh clone until the submodule is initialized (see above).
- The submodule pins whatever commit was current when it was last updated in August 2025; the upstream repo (owned by eryn-chen, a former contributor) may have moved on or gone stale since.
- No design review, status notes, or interface documentation for this board exist in this wiki — its actual completeness is unknown until someone inspects it.

## Open work

- [ ] Run `git submodule update --init` and inspect the actual contents; replace the inferred description above with verified facts.
- [ ] Confirm the upstream repository (https://github.com/eryn-chen/Zynq-Carrier-Power) is still accessible; if the original owner is no longer active in the club, consider forking it into a club-owned account and repointing the submodule.
- [ ] Document the design's purpose, status, and how it relates to the smartphone architecture (what does it power, what are its inputs/outputs?).
- [ ] Decide whether a submodule is still the right structure, and record any change as a decision page (compare [[decisions/2025-08-digitalbot-submodule-removal]] for how a past submodule decision was handled).
