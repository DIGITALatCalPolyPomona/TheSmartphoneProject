---
id: governance/agent-governance
title: Agent Governance
type: governance
status: active
owners: [digital-club]
tags: [governance, ai-agents]
created: 2026-07-09
updated: 2026-10-01
related: [governance/documentation-standards, index]
---

# Agent Governance

This project expects much of its future work — documentation upkeep, design
reviews, refactoring — to be done or assisted by AI agents, because the
human team turns over every academic year. These rules keep agent work
safe, reviewable, and knowledge-preserving. They bind any autonomous or
semi-autonomous agent (Claude Code sessions, CI bots, future tools) working
in this repository. `AGENTS.md` at the repo root is the canonical summary
(`CLAUDE.md` imports it) and points agents here.

## Ground rules

1. **Read before write.** An agent must read `wiki/index.md` and the wiki
   page(s) covering any artifact it is about to touch. If no page exists,
   the agent's first deliverable is that page (status `draft`), not the
   change itself.
2. **Docs travel with changes.** Any change to a governed artifact must
   update the corresponding wiki page (`updated` date bumped, content kept
   truthful) in the same branch. `openwiki check` must pass before an agent
   declares work complete.
3. **Verification is human.** Agents may set page status up to `active`.
   Only a human maintainer may set `verified` / `last_verified` — agents
   must never claim human verification.
4. **Decisions get decision records.** Anything irreversible or
   architectural (adding/removing a submodule, changing a part, retiring a
   board) requires a `decision` page under `wiki/decisions/` *before* the
   change lands. The DIGITALBot episode
   ([[decisions/2025-08-digitalbot-submodule-removal]]) is the cautionary
   tale: three days of add/revert/re-add churn with no recorded rationale.
5. **No silent destruction.** Agents must not delete wiki pages, decision
   records, or `thermometer-backups/` contents; archival (`status:
   archived`) is the only allowed retirement path. Hardware files may be
   deleted only with an accompanying decision record.
6. **Generated files stay generated.** `graph/` and `build/` are tool
   output. Agents regenerate them via the CLI; hand-editing them is a
   governance violation that CI will catch.
7. **Stay in scope.** An agent asked to do X does X and its documentation
   duties — it does not opportunistically restructure the repo, rewrite
   history, or push to branches it was not assigned.
8. **Honest handoffs.** An agent ending a work session with unfinished work
   must leave the state written down: update the affected page's "Open
   work" section, or file a `stub`/`draft` page describing what remains.

## Session protocol for agents

1. Orient: read `CLAUDE.md`, `wiki/index.md`, and relevant pages.
2. Plan: identify which governed artifacts and wiki pages the task touches.
3. Work: make changes; keep docs in lockstep (ground rule 2).
4. Sync: `python3 tools/openwiki/openwiki.py graph`.
5. Gate: `python3 tools/openwiki/openwiki.py check` — must pass.
6. Handoff: commit with a descriptive message; summarize doc updates in the
   commit body or PR description.

## Verification duty

When a task says "verify that proper documentation exists" for some work,
the agent runs `python3 tools/openwiki/openwiki.py verify` and reports the
result verbatim: which artifacts are covered, which pages are stale, which
are stubs. Coverage gaps found during unrelated work should be reported
even when fixing them is out of scope.

## Enforcement

- CI (`.github/workflows/openwiki.yml`) enforces rules 2 and 6 mechanically.
- Pull-request review enforces the rest; reviewers should reject agent PRs
  that change artifacts without touching `wiki/`.
- Repeated violations mean the agent's instructions (`CLAUDE.md`, agent
  definitions under `.claude/agents/`) need fixing — file a decision page
  proposing the change.
