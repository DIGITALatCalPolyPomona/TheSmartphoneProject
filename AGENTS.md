# AGENTS.md — TheSmartphoneProject

Canonical instructions for any coding/documentation agent working in this
repository. Tool-specific entry points (e.g. `CLAUDE.md`) import this file —
keep edits here so all agents stay in sync.

## What this repo is

KiCad 9.0 **hardware** project (PCB design), not software. There is no build
system, package manager, or test suite — do not look for `package.json`,
`Makefile`, or source code. The design: a thermometer/pressure daughter board
(MCP9600 thermocouple amp + BMP581 barometric sensor over I2C, J1 to host).

**Status:** paused August 2025, mid-design. Preserved for resumption.

## Working principles

Derived from Andrej Karpathy's observations on LLM coding pitfalls:

- **Think before editing.** Read the actual files before claiming anything
  about the design. The schematic/PCB are the ground truth — docs describe
  them, never the reverse. If docs and files disagree, the files win.
- **Manage confusion explicitly.** If a pin/net/library claim can't be
  verified from repo files, say so — do not guess and write it into docs.
- **Surgical changes.** Change only what the task requires. KiCad files are
  S-expressions; small hand edits are fine, but preserve surrounding
  formatting, UUIDs, and file structure. Do not reformat whole files.
- **Verify before "done".** Success = the checks below pass, not "it looks
  right". Run them and report output verbatim.

## Knowledgebase governance (non-negotiable)

Documentation is enforced because the team turns over yearly and this
project already died once for lack of it. Full rules:
`wiki/governance/agent-governance.md`.

1. Before touching a hardware/library file, read `wiki/index.md` plus the
   wiki page that lists the file in its `documents:` frontmatter. No page?
   Scaffold one first: `python3 tools/openwiki/openwiki.py new TYPE ID`.
2. Every change to a governed artifact updates its wiki page in the same
   branch (content + `updated:` date). CI fails otherwise.
3. Before declaring work done, run:
   ```
   python3 tools/openwiki/openwiki.py graph   # regen knowledge graph
   python3 tools/openwiki/openwiki.py check   # the CI gate — must pass
   python3 tools/ci/kicad_sanity.py           # kicad file sanity
   ```
4. Never hand-edit `graph/` or `build/` (generated). Never set a page's
   `status: verified` (humans only). Never delete wiki pages or decision
   records — archive instead.
5. Irreversible/architectural changes need a `wiki/decisions/` page first.

## Layout

- `wiki/` — governed knowledgebase (Markdown + frontmatter). Schema:
  `wiki/governance/documentation-standards.md`. Start: `wiki/index.md`.
- `docs/` — design documentation (architecture, components, pinout,
  library notes, history). Complements the wiki; keep both accurate.
- `graph/` — generated knowledge graph (JSON + Mermaid), do not hand-edit.
- `tools/openwiki/openwiki.py` — wiki validator/coverage/graph CLI.
- `tools/ci/kicad_sanity.py` — structural checks on KiCad files.
- `openwiki.config.json` — which artifacts require wiki pages.
- `thermometer.*` — the board project (`kicad_pro` is what KiCad opens).
- `jackboys.kicad_sym`, `jackboys2.pretty/` — project-local symbol/footprint
  libraries (MCP9600). `sym-lib-table`/`fp-lib-table` register them.
- `Zynq-Carrier-Power/` — git submodule (host power board).
  `git submodule update --init` to populate.
- `thermometer-backups/`, `fp-info-cache`, `jackboys.bak` — KiCad-generated
  artifacts; exempt from documentation, do not hand-edit.

## Critical gotchas

- **BMP581 library is missing.** `BMP581:BMP581` is referenced but not in
  `sym-lib-table`/`fp-lib-table` and not in this repo — KiCad shows a
  missing-library error for U2 until it is re-sourced (SnapEDA) and
  committed. Details: `docs/library-notes.md`, `wiki/hardware/thermometer.md`.
- **The schematic is mid-rewire and miswired** — not merely "incomplete
  layout". U1's SCL pin is tied to GND, SDA floats, ALERT_2/4 labels are
  swapped on the physical pins; U2's SCL pin is tied to +3.3V, SDO↔INT are
  swapped. J1's 7 pins ARE labeled in the schematic (INT, ALERT_4..1, SDA,
  SCL) but carry no power/ground; the PCB's `unconnected-` nets are a stale
  netlist. Do NOT run "Update PCB from Schematic" until wiring is fixed.
  Authoritative list: `wiki/hardware/thermometer.md` → "Current state" /
  "Open work".
- **KiCad file format:** `.kicad_sch`/`.kicad_pcb` are S-expressions.
  `(symbol ...)` = schematic parts, `(footprint ...)` = placed parts,
  `unconnected-` net prefixes = unrouted pins, `global_label` = named nets.
- **CRLF churn:** repo lives on a Windows mount for some maintainers —
  keep edits LF-only; do not commit line-ending-only diffs.

## Documentation update system

When docs need updating (after any design or process change):

1. `python3 tools/openwiki/openwiki.py verify` — shows coverage gaps and
   pages staler than the artifacts they document. Report output verbatim.
2. Update the affected `wiki/` pages (content + `updated:` date) and the
   matching `docs/` file if one exists.
3. `python3 tools/openwiki/openwiki.py graph` to regenerate `graph/`.
4. `python3 tools/openwiki/openwiki.py check` + `tools/ci/kicad_sanity.py`
   must pass before the change is done. CI (`openwiki.yml`, `docs.yml`)
   enforces the same gates.

Claude Code users also have `/update-docs` and `/review-changes` skills
(`.claude/skills/`) that wrap this workflow.
