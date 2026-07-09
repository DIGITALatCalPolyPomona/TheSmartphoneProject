---
id: governance/confluence-sync
title: Confluence Sync Design
type: governance
status: active
owners: [digital-club]
tags: [governance, confluence, openwiki]
created: 2026-07-09
updated: 2026-07-09
related: [governance/documentation-standards, index]
---

# Confluence Sync Design

The wiki is designed so the club can later mirror it into Confluence
without restructuring anything. **Git is the source of truth; Confluence
is a read-mostly mirror.** This page records the design so a future team
can turn it on in an afternoon.

## What already exists

- Every page carries optional `confluence_space`, `confluence_page_id`, and
  `confluence_parent` frontmatter fields; a repo-wide default space lives in
  `openwiki.config.json` under `confluence.space`.
- `python3 tools/openwiki/openwiki.py confluence` renders every `active`/
  `verified` page body to **Confluence storage format** (the XHTML dialect
  Confluence's REST API accepts) in `build/confluence/`, plus a
  `manifest.json` mapping each page id → title, space, `page_id`, parent,
  and a `content_sha256` for change detection. `stub` and `archived` pages
  are excluded.
- Page bodies are restricted to a Markdown subset (see
  [[governance/documentation-standards]]) precisely so this conversion
  stays lossless.

## Turning it on (future work)

1. Create a Confluence space; put its key in `openwiki.config.json`.
2. Write a small push script (or CI job) that, for each manifest entry:
   - `page_id` empty → `POST /wiki/api/v2/pages` (create under `parent`),
     then write the returned id back into the page's `confluence_page_id`
     frontmatter and commit — the id is the durable link between systems.
   - `page_id` set → compare `content_sha256` against the last-pushed hash
     (store it as a Confluence content property); `PUT` an update only on
     change, incrementing the version number Confluence requires.
3. Run it from CI on merges to `main`, authenticated with a Confluence API
   token stored as a repository secret — never committed.

## Sync policy decisions (already made — record changes as decision pages)

- **One-way sync, git → Confluence.** Edits made in Confluence are
  overwritten on the next push. People who want a durable edit change the
  Markdown. This avoids the two-master merge problem that kills most
  wiki mirrors.
- **`[[wikilinks]]` render as literal `[wiki:page-id]` markers** until the
  push script exists; the push script should rewrite them into real
  Confluence page links using the manifest's id → `page_id` mapping.
- **The knowledge graph is not pushed.** Confluence gets the prose;
  `graph/knowledge-graph.json` stays a repo artifact (a future script may
  attach the Mermaid rendering as a page).

## Why not sync now

The club has no Confluence instance today. Everything above is inert until
step 1 happens, and nothing in daily workflow depends on it.
