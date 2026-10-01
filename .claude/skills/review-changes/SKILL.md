# Skill: review-changes

You are reviewing changes to a KiCad 9.0 hardware EDA project called TheSmartphoneProject.
This is a thermometer sensor daughter board (MCP9600 thermocouple amplifier + BMP581 pressure sensor).
See `/CLAUDE.md` and `docs/` for full project context before proceeding.

## Purpose

After any changes to KiCad design files, invoke this skill to determine which documentation
files need updating and produce a concrete impact report.

---

## Step 1 — Identify changed KiCad files

Run both of the following:
```
git diff --name-only
git diff --cached --name-only
```

Filter results to files with these extensions:
- `.kicad_sch` — schematic changes
- `.kicad_pcb` — PCB layout changes
- `.kicad_sym` — symbol library changes
- `.kicad_mod` — footprint changes
- `.kicad_pro` — project settings changes
- `fp-lib-table` — footprint library path changes
- `sym-lib-table` — symbol library path changes

If none of these files appear in the diff output, report:
> "No KiCad design file changes detected. No documentation updates required."
Then stop.

---

## Step 2 — Analyze schematic changes (`.kicad_sch`)

Run `git diff thermometer.kicad_sch` and look for:

**New component added** (`(symbol ...)` block with a new Reference):
- Extract: Reference (e.g., U3), Value (part name), Footprint property, any nearby global labels
- Doc impact: Add row to `docs/components.md` table and hardware summary in `README.md`

**Component removed** (`(symbol ...)` block deleted):
- Extract: Which Reference was removed
- Doc impact: Remove or mark as removed in `docs/components.md`, update `README.md` table

**New global label** (`(global_label ...)` added):
- Extract: label name (e.g., a new signal name)
- Doc impact: Add to signal inventory in `docs/architecture.md`, check `docs/connector-pinout.md`

**Footprint property changed on existing symbol**:
- Note which component and what the new footprint is
- Doc impact: Update footprint field in `docs/components.md` for that component

**Net connections to J1 pins added**:
- If any J1 pin now connects to a named signal
- Doc impact: Update `docs/connector-pinout.md` pinout table

---

## Step 3 — Analyze PCB changes (`.kicad_pcb`)

Run `git diff thermometer.kicad_pcb` and look for:

**New `(footprint ...)` block** (component placed on PCB for first time):
- Extract: Reference value (e.g., `(property "Reference" "U2")`)
- Doc impact: Update status field in `docs/components.md` from "Schematic only" to "Placed in PCB (unrouted)"

**Net list changes** (lines starting with `(net N "...")`):
- Look for nets that previously had `unconnected-` prefix now having a real signal name
- Doc impact: If any J1 pin (nets 13–19 historically) gained a signal name, update `docs/connector-pinout.md`

**Edge.Cuts geometry added** (`(gr_line ...)` or `(fp_line ...)` on layer `"Edge.Cuts"`):
- Doc impact: Update `docs/architecture.md` PCB state table (board outline now defined); update `README.md` "What Is Complete" list

**Routing tracks added** (`(segment ...)` blocks):
- Doc impact: Update `README.md` "What Is Incomplete" list if routing has begun or completed

**Zone/copper pour added** (`(zone ...)` blocks):
- Doc impact: Note in `docs/architecture.md` power architecture section

---

## Step 4 — Analyze library changes (`.kicad_sym`, `.kicad_mod`)

Run `git diff jackboys.kicad_sym` (or any other `.kicad_sym` file) and look for:
- New `(symbol "...")` block → new custom symbol added
- Doc impact: Update `docs/library-notes.md` to list the new symbol

Run `git diff` on any `.kicad_mod` file and look for:
- Pad geometry changes
- Doc impact: Update footprint description in `docs/components.md`

---

## Step 5 — Check for new external library dependencies

If a new component was added:
1. Read `sym-lib-table` — is the new component's library listed with a `${KIPRJMOD}/` local path?
2. Read `fp-lib-table` — same check for footprint library
3. If either points to a non-local path (e.g., a global SnapEDA path or missing entry):
   - Flag as: "External dependency detected — should be localized into repo"
   - Doc impact: Add entry to `docs/library-notes.md` "External Libraries" section with reinstall instructions

---

## Step 6 — Produce the documentation impact report

Output this structured report:

```
## Documentation Impact Report

### Changed KiCad Files
- [list each changed file]

### Files That Need Updating
- `docs/components.md` — [specific reason]
- `README.md` — [specific reason]
- [etc. — only list files that actually need changes]

### Files That Do NOT Need Updating
- [file] — [brief reason why it's unaffected]

### Proposed Changes (per file)
#### docs/components.md
[Describe exactly what text to add, change, or remove — quote the old text and new text]

#### README.md
[Same format]

[Continue for each affected file]

### External Dependency Alert (if applicable)
[Flag any new library not stored in repo]
```

**Do NOT apply changes automatically.** Present the report and ask:
> "Shall I apply these documentation updates?"

Apply only if the user confirms.

---

## Context: Current Documentation State

When checking whether docs are stale, here is the baseline state as of initial documentation (2026-06-02):
- U1 MCP9600: Placed in PCB, unrouted
- U2 BMP581: In schematic only (not in PCB)
- TC1: In schematic only, no footprint
- J1: All 7 pins unconnected
- Board outline: Empty
- Routing: None
- BMP581 library: Not in repo (external, SnapEDA)
