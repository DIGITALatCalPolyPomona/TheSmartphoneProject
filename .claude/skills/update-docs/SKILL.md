# Skill: update-docs

You are a documentation maintenance agent for TheSmartphoneProject, a KiCad 9.0 PCB design
project. See `/CLAUDE.md` and `docs/` for full project context before proceeding.

## Purpose

Audit all project documentation against the current state of the KiCad design files.
Identify stale or missing information, produce a staleness report, and optionally apply fixes.

Invoke as `/update-docs` to audit only.
Invoke as `/update-docs apply` to audit and immediately apply all proposed changes.

---

## Step 1 — Read the ground-truth design files

Read these files to establish current design state. Read them in full — they are text files.

1. `thermometer.kicad_pcb` — extract:
   - All `(net N "...")` lines → current net list (note which are `unconnected-` prefixed)
   - All `(footprint ...)` blocks → which component references are placed in PCB
   - Whether any `(gr_line ...)` exists on layer `"Edge.Cuts"` → board outline present?
   - Whether any `(segment ...)` blocks exist → routing present?

2. `thermometer.kicad_sch` — extract:
   - All `(symbol ...)` blocks with `(property "Reference" ...)` and `(property "Value" ...)` → component list
   - All `(property "Footprint" ...)` within each symbol → footprint assignment
   - All `(global_label ...)` entries → named signals in design
   - I2C address labels near each component (appear as `(label "0x..." ...)` near component pins)

3. `jackboys.kicad_sym` — list all `(symbol "...")` entries → locally stored symbols

4. `jackboys2.pretty/` directory — list all `.kicad_mod` files → locally stored footprints

5. `sym-lib-table` — list all registered symbol library entries and their paths

6. `fp-lib-table` — list all registered footprint library entries and their paths

7. `git log --oneline` — get full commit history for project-history.md audit

---

## Step 2 — Build a current-state inventory

Compile these facts from Step 1 before auditing any docs:

**Components in schematic:**
- Reference | Value | Footprint assigned (yes/no and library:name) | I2C address

**Components in PCB:**
- Which References have a `(footprint ...)` block → "placed in PCB"
- Which References from schematic are absent from PCB → "schematic only"

**Net connectivity:**
- Are any J1 pins (historically nets 13–19) now connected to named signals?
- Are there any nets that are no longer `unconnected-` that were before?

**Board outline:**
- Does Edge.Cuts have any geometry?

**Routing:**
- Do any `(segment ...)` blocks exist?

**Library state:**
- Is `BMP581:BMP581` listed in `sym-lib-table` with a `${KIPRJMOD}/` local path? (If not: still missing)
- Are there any new `.kicad_sym` or `.kicad_mod` files added since initial documentation?

---

## Step 3 — Audit each documentation file

For each file, check the specific items listed below. Note discrepancies as STALE or MISSING.

### `README.md`
- Hardware summary table: Does it list all components currently in the schematic?
- "What Is Complete" list: Does it match actual PCB/schematic state?
- "What Is Incomplete" list: Does it accurately reflect current gaps (routing, board outline, U2 PCB placement, J1 pinout)?
- BMP581 "Before Opening" section: Is the library still missing (check sym-lib-table)?
- Project status line: Still "Abandoned August 2025" unless new commits show resumed work?

### `CLAUDE.md`
- "Current Design State" table: Does it match the current PCB state?
- "CRITICAL: Missing External Library" section: Is BMP581 still missing from repo?
- "Key Files" table: Are all listed files still present? Any new files to add?
- "Available Skills" list: Are the skills still at `.claude/skills/review-changes/` and `.claude/skills/update-docs/`?

### `docs/architecture.md`
- I2C bus table: Do component addresses match the labels in the schematic?
- Signal inventory table: Are all global labels present? Any new ones added?
- PCB state table: Does it reflect current PCB placement, routing, and board outline status?
- Power architecture section: Any new decoupling capacitors or power components added?

### `docs/components.md`
- For each component: Is the "Status" field accurate (Schematic only / Placed in PCB (unrouted) / Routed)?
- Are there any components in the schematic not yet documented here?
- BMP581 "ACTION REQUIRED" note: Still applicable if BMP581:BMP581 not in sym-lib-table locally?
- Footprint assignments: Do the footprint fields match what's in the schematic?

### `docs/connector-pinout.md`
- J1 pin table: Have any pins moved from "unconnected" to a defined signal? (Check net list)
- "Work Required" list: Have any items been completed? (e.g., U2 placed in PCB, traces routed)

### `docs/library-notes.md`
- "Local Custom Libraries" section: Are there new `.kicad_sym` or `.kicad_mod` files not yet documented?
- "External Libraries" section: Is BMP581 still marked MISSING, or has it been localized?
- `sym-lib-table` summary table: Does it match the actual file content?
- `fp-lib-table` summary table: Does it match the actual file content?

### `docs/project-history.md`
- Timeline table: Are there commits in `git log --oneline` output that are not yet in the table?
  (Run `git log --oneline` and compare each hash against the table.)
- If new commits exist: Append them to the timeline table — never rewrite existing history entries.

---

## Step 4 — Produce the staleness report

Output this structured report:

```
## Documentation Audit Report
Date: [today's date]

### Summary
- Files audited: N
- Up to date: N
- Stale or missing content: N

### Up to Date
- `[filename]` — [brief reason confirming accuracy]

### Stale or Missing
- `[filename]`
  - Section: "[section name]"
  - Current text: "[quote the stale text, or 'MISSING' if absent]"
  - Actual state: "[what the design files show]"
  - Proposed update: "[exact text to add or replace with]"

[Repeat for each stale item]
```

---

## Step 5 — Apply updates (if authorized)

**Default behavior:** Present the report from Step 4 and ask:
> "Shall I apply these documentation updates? (Yes / No / Select specific items)"

**If invoked as `/update-docs apply`:** Skip the question and apply all proposed changes immediately.

Apply changes in this order to avoid forward-reference issues:
1. `docs/components.md` (most likely to change; other docs reference it)
2. `README.md` (summarizes components.md)
3. `docs/connector-pinout.md` (depends on PCB net state)
4. `docs/architecture.md`
5. `docs/library-notes.md`
6. `CLAUDE.md`
7. `docs/project-history.md` — **APPEND ONLY**: never rewrite existing entries; only add new rows to the timeline table

After applying all changes, output:
> "Updated [N] files. Changes made:
> - `[filename]`: [one-line summary of what changed]
> - ..."

---

## Context: Baseline State (as of 2026-06-02)

Use this as the reference when determining whether the current state is a change from
what was originally documented:

| Item | Baseline |
|------|---------|
| U1 MCP9600 | Placed in PCB, not routed |
| U2 BMP581 | Schematic only, not in PCB |
| TC1 thermocouple | Schematic only, no footprint |
| J1 pins 1–7 | All unconnected (nets 13–19) |
| Board outline | Empty |
| Copper routing | None |
| Decoupling caps | None |
| BMP581 library | Not in repo (external/SnapEDA) |
| Last git commit | c81e8e5 — "Removed DIGITALBot Submodule" (2025-08-26) |
