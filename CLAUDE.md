# CLAUDE.md — TheSmartphoneProject

KiCad 9.0 **hardware** repo (PCB design — not software). The canonical agent
instructions for this project live in `AGENTS.md`:

@AGENTS.md

If the import above did not resolve, read `AGENTS.md` now — it is required,
not optional.

## Claude-only notes

- Repo skills (`.claude/skills/`):
  - `/update-docs` — audit `wiki/` + `docs/` against the actual KiCad files,
    then update. Run this whenever a design artifact changed.
  - `/review-changes` — map a git diff of `*.kicad_*`/`lib-table` files onto
    the wiki pages that must be updated.
- Ready-made agents in `.claude/agents/`: `doc-steward` (writes/maintains
  wiki pages), `doc-verifier` (read-only check runner).
- Gate before any "done" claim: `python3 tools/openwiki/openwiki.py check`
  and `python3 tools/ci/kicad_sanity.py` — both must pass.
