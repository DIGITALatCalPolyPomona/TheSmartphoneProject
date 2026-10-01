---
name: notion-sync
description: Cross-check the governed wiki/ knowledgebase against the club's Notion workspace via the Notion MCP server. Reports drift both ways. Use when asked to "compare the wiki and Notion", "sync knowledge base", or verify the two sources are on the same page.
---

# Notion ↔ OpenWiki cross-check

Git (`wiki/`) is the **source of truth**; Notion is a human-facing mirror.
This skill detects drift — it does not auto-fix either side without approval.

Prerequisite: the `notion` MCP server must be connected (`.mcp.json` /
`.devin/mcp.json` → `https://mcp.notion.com/mcp`, OAuth on first connect). If
the MCP tools aren't available, stop and tell the user to authorize Notion.

## Step 1 — Inventory the wiki side

```bash
python3 tools/openwiki/openwiki.py validate   # all pages parse
ls wiki/**/*.md                               # or read graph/knowledge-graph.json
```

Build a list: page `id`, `title`, `status`, `updated`. Only `active`/`verified`
pages are in-scope for mirroring (same rule as the Confluence export); note
`draft`/`stub`/`archived` pages separately.

## Step 2 — Inventory the Notion side

Use the Notion MCP `search` tool (empty query or terms like the page titles /
"thermometer" / "DIGITAL") to find the club's knowledge-base pages. Map each
Notion page to a wiki page by title — expected pairs:

- `index` / "The Smartphone Project"
- `hardware/thermometer`, `hardware/zynq-carrier-power`
- `libraries/jackboys-symbols`, `libraries/jackboys2-footprints`, `libraries/library-tables`
- `guides/getting-started`
- `governance/*`, `decisions/*`

Record Notion page id, title, and `last_edited_time` for each match.

## Step 3 — Compare

For each mapped pair, fetch the Notion page content (blocks) and compare
against the wiki page body:

- **Stale in Notion:** Notion claims something the wiki corrected
  (watch for the known traps: "J1 pins unconnected", "SDO tied to GND",
  "open-drain alerts", "submodule empty" — all false per current wiki).
- **Missing in Notion:** wiki page has no counterpart.
- **Orphan in Notion:** Notion page documents this project but has no wiki page.
- **Missing in wiki:** Notion has project info the wiki lacks — flag it;
  git must capture it, not the other way around.

Distinguish *factual conflicts* (different pinouts/dates/status — always
report) from *cosmetic drift* (formatting, ordering — note only).

## Step 4 — Report (do not edit yet)

```text
## Notion ↔ Wiki Sync Report
Date: [today]

### Conflicts (Notion disagrees with wiki — wiki wins)
- [wiki page] vs [Notion page]: [claim in Notion] → [claim in wiki]

### Missing in Notion: [N pages]
### Orphans in Notion: [N pages]
### Info only in Notion (candidate wiki additions): [items]

Recommendation: [push wiki→Notion | pull specific facts | none needed]
```

## Step 5 — Apply (only on approval)

- **Wiki → Notion (normal direction):** update the Notion page's blocks to
  match the wiki. Prefer updating over deleting. Note the sync in the wiki
  page's `related`/body only if the team wants the linkage recorded.
- **Notion → wiki (rare):** if Notion holds real project knowledge, add it to
  the proper wiki page, bump `updated:`, then run `openwiki graph` + `check`.
- Re-run this skill's Step 3 after writing to confirm convergence.
