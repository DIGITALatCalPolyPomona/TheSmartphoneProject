---
id: governance/notion-sync
title: Notion Sync (MCP cross-check)
type: governance
status: active
owners: [digital-club]
tags: [governance, notion, mcp, openwiki]
created: 2026-10-01
updated: 2026-10-01
related: [governance/confluence-sync, governance/documentation-standards, index]
---

# Notion Sync (MCP cross-check)

The club may keep a human-facing copy of this knowledgebase in **Notion**.
Like the Confluence design ([[governance/confluence-sync]]), **git is the
source of truth** — Notion is a read-mostly mirror. Unlike Confluence, Notion
sync is driven manually by an agent through Notion's official MCP server.

## How it connects

- `.mcp.json` (Claude Code) and `.devin/mcp.json` (Devin) both declare the
  `notion` server pointing at `https://mcp.notion.com/mcp` — Notion's hosted
  Streamable-HTTP MCP endpoint.
- First use triggers an OAuth flow in the agent's client; each maintainer
  authorizes their own workspace access. **No tokens are committed to this
  repo.** A token-based local alternative (`@notionhq/notion-mcp-server` with
  a `NOTION_TOKEN` env var) exists for clients without remote-MCP support.
- There is no CI job for this — Notion access is interactive/user-authorized,
  so the check runs on demand via the agent skill `/notion-sync`
  (`.claude/skills/notion-sync/SKILL.md`).

## Workflow

1. Agent inventories wiki pages (the `graph/knowledge-graph.json` page list is
   authoritative) and searches Notion for counterparts.
2. Content is compared pair-by-pair; factual conflicts and missing/orphan
   pages are reported — never silently edited.
3. On approval, drift is resolved wiki→Notion. If Notion holds knowledge the
   repo lacks, it is pulled into the wiki (with `updated:` bump +
   `openwiki graph` + `openwiki check`), because the repo must survive even
   if the Notion workspace is lost — that is the whole reason OpenWiki exists
   (see [[index]] project history).

## Scope

Only `active` and `verified` wiki pages are expected to exist in Notion —
the same subset the Confluence exporter uses. `draft`/`stub`/`archived`
pages staying git-only is intentional.
