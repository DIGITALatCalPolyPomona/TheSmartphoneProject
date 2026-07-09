# The Smartphone Project — agent instructions

KiCad hardware repo (DIGITAL @ Cal Poly Pomona). The knowledgebase lives in
`wiki/` (OpenWiki) and is **governed**: documentation is not optional here,
because the team turns over yearly and this project already got abandoned
once for lack of it.

## Binding rules

Full rules: `wiki/governance/agent-governance.md`. Non-negotiables:

1. Before touching any hardware/library file, read `wiki/index.md` and the
   wiki page that documents that file (the page lists it in its `documents`
   frontmatter). No page? Write one first (`openwiki new`).
2. Every change to a governed artifact updates its wiki page in the same
   branch (content + `updated` date).
3. Before declaring any work done:
   `python3 tools/openwiki/openwiki.py graph`   (regenerate knowledge graph)
   `python3 tools/openwiki/openwiki.py check`   (must pass — CI runs it too)
4. Never hand-edit `graph/` or `build/` (generated), never set a page's
   status to `verified` (humans only), never delete wiki pages or decision
   records (archive instead).
5. Irreversible/architectural changes need a decision page under
   `wiki/decisions/` first.

## Layout

- `wiki/` — the knowledgebase; schema in `wiki/governance/documentation-standards.md`
- `graph/` — generated knowledge graph (JSON + Mermaid)
- `tools/openwiki/openwiki.py` — validator / graph builder / coverage
  auditor / Confluence exporter (stdlib-only Python 3.8+)
- `openwiki.config.json` — which artifacts are governed
- `thermometer.*`, `jackboys*`, `Zynq-Carrier-Power/` — the hardware; see
  their wiki pages before opening them in KiCad

## Verifying documentation exists

When asked to verify docs for some work:
`python3 tools/openwiki/openwiki.py verify` — report its output verbatim
(coverage gaps, stale pages, stubs).
