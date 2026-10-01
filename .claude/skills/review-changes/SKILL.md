# Skill: review-changes

You are reviewing changes to a KiCad 9.0 hardware EDA project called TheSmartphoneProject.
This is a thermometer sensor daughter board (MCP9600 thermocouple amplifier + BMP581 pressure sensor).
Read `AGENTS.md` and `wiki/index.md` first — documentation is governed by the
OpenWiki system (`wiki/` + `openwiki.config.json` + CI gate `openwiki check`).

## Purpose

After any changes to KiCad design files, invoke this skill to determine which
documentation needs updating and produce a concrete impact report.

**Governance rule:** a change to a governed artifact (`openwiki.config.json`
`governed` list: `*.kicad_pro`, `*.kicad_sch`, `*.kicad_pcb`, `*.kicad_sym`,
`*.pretty`, `Zynq-Carrier-Power`, `*-lib-table`) REQUIRES an update to the wiki
page that lists it in `documents:` — same branch, `updated:` date bumped.
`docs/` and `README.md` are secondary consistency targets.

---

## Step 1 — Identify changed files

Run both:

```bash
git diff --name-only
git diff --cached --name-only
```

Filter to governed artifacts:

- `.kicad_sch` — schematic changes
- `.kicad_pcb` — PCB layout changes
- `.kicad_sym` — symbol library changes
- `.kicad_mod` / `.pretty/` — footprint changes
- `.kicad_pro` — project settings changes
- `fp-lib-table` / `sym-lib-table` — library registration changes
- `.gitmodules` / `Zynq-Carrier-Power` gitlink — submodule changes

If none appear, report:
> "No governed artifact changes detected. No documentation updates required."
Then stop.

---

## Step 2 — Analyze schematic changes (`.kicad_sch`)

Run `git diff thermometer.kicad_sch` and look for:

- **New/removed `(symbol ...)` block** → component added/removed.
  Impact: `wiki/hardware/thermometer.md` parts table + `docs/components.md` + `README.md` summary.
- **New `(global_label ...)`** → new named signal.
  Impact: `wiki/hardware/thermometer.md` connectivity text + `docs/architecture.md` signal inventory.
- **Footprint property changed on a symbol** →
  Impact: `docs/components.md` footprint field.
- **J1 pins wired to named signals** →
  Impact: `wiki/hardware/thermometer.md` open-work item + `docs/connector-pinout.md` pinout table.

---

## Step 3 — Analyze PCB changes (`.kicad_pcb`)

Run `git diff thermometer.kicad_pcb` and look for:

- **New `(footprint ...)` block** → component placed.
  Impact: `wiki/hardware/thermometer.md` current-state + `docs/components.md` status field.
- **`(net ...)` changes** → `unconnected-` names gaining real signals.
  Match J1 pins by net NAME `unconnected-(J1-...)` — net indices are
  auto-assigned and shift on any netlist change; never hardcode them.
  Impact: `wiki/hardware/thermometer.md` + `docs/connector-pinout.md`.
- **`Edge.Cuts` geometry added** → board outline defined.
  Impact: `wiki/hardware/thermometer.md` + `docs/architecture.md` + `README.md` lists.
- **`(segment ...)`/`(via ...)`/`(zone ...)` added** → routing began.
  Impact: `wiki/hardware/thermometer.md` open-work + `README.md` "What Is Incomplete".

---

## Step 4 — Analyze library changes

- `git diff jackboys.kicad_sym` — new `(symbol "...")` blocks →
  `wiki/libraries/jackboys-symbols.md` + `docs/library-notes.md`.
- `git diff` on `jackboys2.pretty/*.kicad_mod` — pad/geometry changes →
  `wiki/libraries/jackboys2-footprints.md` + `docs/components.md`.
- `git diff sym-lib-table fp-lib-table` — registrations →
  `wiki/libraries/library-tables.md` + `docs/library-notes.md`.

## Step 5 — New external library dependencies

If a component was added whose `lib_id` library is not in `sym-lib-table`
with a `${KIPRJMOD}/` path (or footprint lib missing from `fp-lib-table`):
flag as "External dependency — must be localized into the repo" and update
`wiki/libraries/library-tables.md` + `docs/library-notes.md` (the BMP581 gap
is the standing example).

## Step 6 — Impact report

```text
## Documentation Impact Report

### Changed governed artifacts
- [each changed file] → covering wiki page: [wiki page id or NONE — needs `openwiki new`]

### Wiki pages to update (required by governance)
- `wiki/...` — [reason]

### Secondary docs to update
- `docs/...` / `README.md` — [reason]

### Proposed changes (per file)
#### wiki/hardware/thermometer.md
[old text → new text; bump `updated:`]

### External dependency alert (if applicable)
```

**Do NOT apply automatically.** Ask: "Shall I apply these documentation updates?"

## Step 7 — After approval (mandatory gate)

```bash
python3 tools/openwiki/openwiki.py graph    # regenerate graph/ — commit it
python3 tools/openwiki/openwiki.py check    # must pass — CI runs it
python3 tools/ci/kicad_sanity.py
```

If `check` fails, fix the cause — never hand-edit `graph/`.

## Reference

For the "expected prior state", read `wiki/hardware/thermometer.md` "Current
state" / "Open work" — the wiki is the baseline; do not maintain a static
baseline table inside this skill.
