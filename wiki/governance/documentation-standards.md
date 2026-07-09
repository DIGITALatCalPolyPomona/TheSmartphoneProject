---
id: governance/documentation-standards
title: Documentation Standards (OpenWiki)
type: governance
status: active
owners: [digital-club]
tags: [governance, openwiki]
created: 2026-07-09
updated: 2026-07-09
related: [governance/agent-governance, governance/confluence-sync, index]
---

# Documentation Standards (OpenWiki)

This repository's knowledgebase lives in `wiki/` and is called **OpenWiki**:
plain Markdown pages with machine-readable frontmatter, validated by
`tools/openwiki/openwiki.py`, and mirrored into a knowledge graph in
`graph/`. The project was paused once and nearly lost its institutional
knowledge; these standards exist so that never happens again.

## Rule

1. Every **governed artifact** (see `openwiki.config.json` — KiCad projects,
   symbol/footprint libraries, library tables, submodules) must be documented
   by at least one wiki page with status `active` or `verified` that lists it
   in its `documents` frontmatter field.
2. When you change a governed artifact, update its wiki page in the **same
   commit** and bump the page's `updated` date. `openwiki verify` flags pages
   older than their artifact's last commit as stale.
3. The knowledge graph (`graph/knowledge-graph.json` + `.mmd`) is generated,
   never hand-edited. After any wiki change, run
   `python3 tools/openwiki/openwiki.py graph` and commit the result.
4. Before every commit, run `python3 tools/openwiki/openwiki.py check`.
   CI runs the same command and blocks merges on failure.

## Page schema

Pages start with a `---`-delimited frontmatter block of flat `key: value`
pairs; lists are inline (`[a, b]`). No nested keys — the parser is
deliberately strict so pages stay machine-readable.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Must equal the file path under `wiki/` without `.md` |
| `title` | yes | Human title (also the Confluence page title) |
| `type` | yes | `overview`, `hardware`, `library`, `guide`, `decision`, `governance` |
| `status` | yes | `stub` → `draft` → `active` → `verified`; `archived` when retired |
| `owners` | yes | Who answers for this page (person or team handle) |
| `created` / `updated` | yes | ISO dates; bump `updated` on every edit |
| `tags` | no | Free-form labels; become graph nodes |
| `documents` | no | Repo paths (or globs) of artifacts this page documents |
| `related` | no | Ids of related pages; become graph edges |
| `last_verified` | no | Date a human confirmed the page matches reality; required for status `verified` |
| `confluence_space` / `confluence_page_id` / `confluence_parent` | no | Confluence mapping — see [[governance/confluence-sync]] |

In page bodies, `[[page-id]]` wikilinks create `references` edges in the
knowledge graph and are validated (a link to a nonexistent page fails CI).

## Lifecycle

- **stub** — placeholder created with `openwiki new`; counts as a coverage
  warning, not coverage.
- **draft** — being written; does not satisfy coverage.
- **active** — trusted documentation; satisfies coverage.
- **verified** — a human re-checked the page against the artifact and set
  `last_verified`. Prefer this for anything safety- or hardware-spend-related
  (a wrong footprint costs a board spin).
- **archived** — kept for history (e.g. superseded decisions); excluded from
  Confluence export.

## How to add a page

```
python3 tools/openwiki/openwiki.py new hardware hardware/my-board
# edit wiki/hardware/my-board.md, fill in frontmatter + body
python3 tools/openwiki/openwiki.py check
python3 tools/openwiki/openwiki.py graph
git add wiki graph && git commit
```

## Enforcement

`.github/workflows/openwiki.yml` runs `openwiki check` on every push and
pull request: schema validation, documentation coverage of governed
artifacts, and knowledge-graph freshness. A red check means the
knowledgebase and the repo have drifted — fix the docs, not the gate.
