# OpenWiki tooling

Single-file, stdlib-only CLI (`openwiki.py`, Python 3.8+) behind the
`wiki/` knowledgebase. No pip installs — it must run on any lab machine
that can run KiCad.

```
python3 tools/openwiki/openwiki.py validate      # schema-check every page
python3 tools/openwiki/openwiki.py verify        # doc coverage of governed artifacts
python3 tools/openwiki/openwiki.py graph         # regenerate graph/ (JSON + Mermaid)
python3 tools/openwiki/openwiki.py graph --check # fail if committed graph is stale
python3 tools/openwiki/openwiki.py check         # all of the above — the CI gate
python3 tools/openwiki/openwiki.py new TYPE ID   # scaffold a page from wiki/_templates/
python3 tools/openwiki/openwiki.py confluence    # export build/confluence/ for Confluence
```

- What counts as a governed artifact: `openwiki.config.json`.
- Page schema and lifecycle: `wiki/governance/documentation-standards.md`.
- Rules for AI agents: `wiki/governance/agent-governance.md`.
- Confluence mirroring design: `wiki/governance/confluence-sync.md`.

The knowledge graph (`graph/knowledge-graph.json`) is deterministic —
same wiki in, byte-same graph out — so `graph --check` can enforce
freshness in CI via the embedded `source_digest`. `graph/knowledge-graph.mmd`
is a Mermaid rendering of the same graph (minus tag nodes) that GitHub
displays natively.
