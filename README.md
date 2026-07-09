# The Smartphone Project

Hardware project by DIGITAL at Cal Poly Pomona. KiCad 9 designs: a
thermocouple + barometric-pressure **sensor daughter board**, a
**Zynq carrier power** submodule, and the custom **jackboys** part
libraries.

## Start here

**Everything you need to know lives in the wiki: [`wiki/index.md`](wiki/index.md).**

New to the project? Read
[`wiki/guides/getting-started.md`](wiki/guides/getting-started.md).

## The knowledgebase is governed

This project was once paused and nearly lost all of its institutional
knowledge. To prevent a repeat, documentation is enforced, not hoped for:

- Every hardware artifact must have a current wiki page
  ([standards](wiki/governance/documentation-standards.md)).
- A knowledge graph ([`graph/`](graph/)) is generated from the wiki and
  kept in sync by CI.
- AI agents working here follow
  [`wiki/governance/agent-governance.md`](wiki/governance/agent-governance.md).
- Gate command (run before every commit; CI runs it too):

```
python3 tools/openwiki/openwiki.py check
```

## Repo map

| Path | What it is |
|---|---|
| `wiki/` | OpenWiki knowledgebase (Markdown + frontmatter) |
| `graph/` | Generated knowledge graph (JSON + Mermaid) — do not hand-edit |
| `tools/openwiki/` | The OpenWiki CLI (stdlib-only Python) |
| `thermometer.*` | Sensor daughter board KiCad project |
| `Zynq-Carrier-Power/` | Power design submodule (`git submodule update --init`) |
| `jackboys.kicad_sym`, `jackboys2.pretty/` | Custom symbol/footprint libraries |
