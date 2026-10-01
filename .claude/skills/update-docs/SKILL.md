# Skill: update-docs

You are a documentation maintenance agent for TheSmartphoneProject, a KiCad 9.0 PCB design
project. Read `AGENTS.md` and `wiki/index.md` first — the governed knowledgebase lives in
`wiki/` and documentation updates are enforced by CI (`openwiki check`).

## Purpose

Audit all project documentation against the current state of the KiCad design files.
Identify stale or missing information, produce a staleness report, and optionally apply fixes.

Invoke as `/update-docs` to audit only.
Invoke as `/update-docs apply` to audit and immediately apply all proposed changes.

**Update targets, in priority order:**
1. `wiki/` pages — governed; any governed-artifact change REQUIRES a matching
   wiki update in the same branch (rule: `wiki/governance/agent-governance.md`).
2. `docs/*.md` and `README.md` — human-facing docs; keep consistent with the wiki.
3. `AGENTS.md`/`CLAUDE.md` — only when durable project facts change (not per-commit
   state; point at wiki pages instead of duplicating state).

---

## Step 0 — Machine check

Run `python3 tools/openwiki/openwiki.py verify` first. It reports undocumented
governed artifacts, pages staler than the artifacts they cover, and stubs.
Every WARN/error line is a confirmed finding — include them verbatim in the report.

---

## Step 1 — Read the ground-truth design files

Read these files to establish current design state. Read them in full — they are text files.

1. `thermometer.kicad_pcb` — extract:
   - All `(net N "...")` lines → current net list (note which are `unconnected-` prefixed).
     Match J1 pins by net NAME pattern `unconnected-(J1-...)` — net indices are
     auto-assigned and shift on any netlist change; never hardcode them.
   - All `(footprint ...)` blocks → which component references are placed in PCB
   - Whether any `(gr_line ...)`/`(gr_* ...)` exists on layer `"Edge.Cuts"` → board outline present?
   - Whether any `(segment ...)` or `(zone ...)` blocks exist → routing/copper present?

2. `thermometer.kicad_sch` — extract:
   - All `(symbol ...)` blocks with `(property "Reference" ...)` and `(property "Value" ...)` → component list
   - All `(property "Footprint" ...)` within each symbol → footprint assignment
   - All `(global_label ...)` entries → named signals in design
   - I2C address labels near each component (appear as `(global_label "0x..." ...)`, e.g. `"0x60"`, `"0x46"`)

3. `jackboys.kicad_sym` — list all `(symbol "...")` entries → locally stored symbols

4. `jackboys2.pretty/` directory — list all `.kicad_mod` files → locally stored footprints

5. `sym-lib-table` — list all registered symbol library entries and their paths

6. `fp-lib-table` — list all registered footprint library entries and their paths

7. `git log --oneline` — get full commit history for project-history.md / wiki decision pages

8. `git submodule status` + `ls Zynq-Carrier-Power` — is the submodule populated?

---

## Step 2 — Build a current-state inventory

Compile these facts from Step 1 before auditing any docs:

**Components in schematic:**
- Reference | Value | Footprint assigned (yes/no and library:name) | I2C address

**Components in PCB:**
- Which References have a `(footprint ...)` block → "placed in PCB"
- Which References from schematic are absent from PCB → "schematic only"

**Net connectivity:**
- Which J1 pins still have `unconnected-(J1-...)` nets vs named signals
- Any other `unconnected-` nets (e.g. U1 SCL/SDA/ALERT/EXP pads)

**Board outline:** does Edge.Cuts have any geometry?

**Routing:** do any `(segment ...)` blocks exist?

**Library state:**
- Is `BMP581:BMP581` listed in `sym-lib-table` with a `${KIPRJMOD}/` local path? (If not: still missing)
- Any new `.kicad_sym` or `.kicad_mod` files not yet documented?

For "what was state before", diff against the "Current state" / "Open work"
sections of `wiki/hardware/thermometer.md` — NOT a hardcoded baseline table
in this file (those go stale; the wiki is the baseline).

---

## Step 3 — Audit each documentation file

Check the specific items below. Note discrepancies as STALE or MISSING.

### `wiki/` pages (governed — primary)

- `wiki/hardware/thermometer.md` — "What is on the board" table, "Current state",
  "Open work" checkboxes, `documents:` coverage, `updated:` date.
- `wiki/libraries/jackboys-symbols.md`, `wiki/libraries/jackboys2-footprints.md`,
  `wiki/libraries/library-tables.md` — symbol/footprint contents and lib-table claims.
- `wiki/hardware/zynq-carrier-power.md` — submodule URL/branch/populated state.
- `wiki/index.md`, `wiki/guides/getting-started.md` — commands, file lists, dates.
- `wiki/decisions/` — append new decisions as new pages; never rewrite or delete.
- Any NEW governed artifact (matched by `openwiki.config.json` `governed`
  patterns) without a covering page → scaffold with
  `python3 tools/openwiki/openwiki.py new TYPE ID`, then fill it in.

### `docs/*.md` + `README.md` (secondary — keep consistent with wiki)

- `README.md` — hardware summary table, complete/incomplete lists, BMP581
  section, repo-structure tree.
- `docs/architecture.md` — I2C bus table vs schematic labels; signal inventory
  vs `global_label` list; PCB state table; power/decoupling claims.
- `docs/components.md` — per-component Status fields; footprint assignments;
  BMP581 "ACTION REQUIRED" applicability.
- `docs/connector-pinout.md` — J1 pin table vs current nets (match by
  `unconnected-(J1-...)` names, not indices); "Work Required" items completed?
- `docs/library-notes.md` — new local symbols/footprints; BMP581 still marked
  MISSING or localized; quoted lib-table contents vs actual files.
- `docs/project-history.md` — **APPEND ONLY**: compare `git log --oneline`
  against the timeline; add new rows, never rewrite existing entries.

---

## Step 4 — Produce the staleness report

```
## Documentation Audit Report
Date: [today's date]

### openwiki verify output
[paste verbatim]

### Summary
- Files audited: N | Up to date: N | Stale or missing: N

### Up to Date
- `[filename]` — [brief reason confirming accuracy]

### Stale or Missing
- `[filename]`
  - Section: "[section name]"
  - Current text: "[quote, or 'MISSING' if absent]"
  - Actual state: "[what the design files show]"
  - Proposed update: "[exact text to add or replace with]"
```

---

## Step 5 — Apply updates (if authorized)

**Default:** present the report and ask:
> "Shall I apply these documentation updates? (Yes / No / Select specific items)"

**`/update-docs apply`:** skip the question, apply all proposed changes.

Apply order (wiki first — it is the governed source):
1. Affected `wiki/` pages (content + `updated:` date)
2. `docs/components.md`, `docs/connector-pinout.md`, `docs/architecture.md`,
   `docs/library-notes.md`
3. `README.md`
4. `docs/project-history.md` — APPEND ONLY

## Step 6 — Regenerate and pass the gate (mandatory)

After ANY applied change:

```
python3 tools/openwiki/openwiki.py graph    # regenerate graph/ — commit it
python3 tools/openwiki/openwiki.py check    # must pass — CI runs it
python3 tools/ci/kicad_sanity.py            # structural check
```

Then output:
> "Updated [N] files. `openwiki check`: PASS. Changes made:
> - `[filename]`: [one-line summary]
> - ..."

If `check` fails, fix the cause — never hand-edit `graph/` and never set a
page's `status:` to `verified` (humans only).
