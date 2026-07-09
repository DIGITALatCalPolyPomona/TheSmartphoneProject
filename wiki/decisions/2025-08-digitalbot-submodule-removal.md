---
id: decisions/2025-08-digitalbot-submodule-removal
title: DIGITALBot Submodule Added and Removed (Aug 2025)
type: decision
status: active
owners: [digital-club]
created: 2026-07-09
updated: 2026-07-09
tags: [decision-record, submodule]
related: [index, hardware/zynq-carrier-power]
---

# DIGITALBot Submodule Added and Removed (Aug 2025)

**Status of the decision:** DIGITALBot is **not** part of this repository, and that removal was deliberate. This page records the back-and-forth so a future team doesn't unknowingly repeat it.

## Context

In late August 2025 — the final days before the project was paused — the team attempted a cross-project integration by adding **DIGITALBot** (a repository owned by a third party, AngeloDuenas: https://github.com/AngeloDuenas/DIGITALBot.git) as a git submodule. The attempt churned over three days and was abandoned.

## Timeline (from git history)

| Commit | Date | What happened |
|--------|------|---------------|
| `e8460a1` | 2025-08-23 | DIGITALBot added as a submodule (url https://github.com/AngeloDuenas/DIGITALBot.git, branch `master`) |
| `05afeec` | | Revert of the add |
| `2375d2a` | | Re-added |
| `e3bd74e` | | Submodule pointer updated |
| `42953f6` | | "checked out main on DIGITALBot" |
| `3b9bdd7` | | Updated again; tracked branch changed from `master` to `main` |
| `c81e8e5` | 2025-08-26 | Removed ("Removed DititalBot Submodule" — typo in the original message). Last commit in the repository. |

The visible churn (add, revert, re-add, branch confusion between `master` and `main`) suggests the integration was not going smoothly; whatever the final reason, the team removed it and work stopped.

## Decision

The DIGITALBot submodule was removed on 2025-08-26 and the integration attempt abandoned. The repository's only remaining submodule is [[hardware/zynq-carrier-power]].

## Consequences

- DIGITALBot code is **not** in this repo; nothing here depends on it.
- The repo history contains submodule add/remove noise from Aug 23-26, 2025. If old checkouts or tooling complain about a `DIGITALBot` path, this is why.
- **If a future team wants this integration:** the target repo is owned by an external individual (AngeloDuenas), so first coordinate with its owner (access, branch naming — note the earlier `master`/`main` confusion, and long-term availability), and **record a new decision page in this wiki before re-adding the submodule**. Do not silently re-run the same experiment.
