#!/usr/bin/env python3
"""OpenWiki — repo-native wiki, knowledge graph, and documentation governance.

Zero-dependency (Python 3.8+ stdlib only) so it runs anywhere KiCad does.

Commands:
  validate            Check every wiki page against the OpenWiki schema.
  graph               Regenerate the knowledge graph from wiki + artifacts.
  graph --check       Fail if the committed graph is out of sync (CI mode).
  verify              Documentation-coverage audit: every governed artifact
                      must be documented by an active/verified page.
  check               validate + verify + graph --check (the CI gate).
  new TYPE ID         Scaffold a new wiki page from the type's template.
  confluence          Export pages to build/confluence/ (storage-format XHTML
                      + sync manifest) for a future Confluence push.

See wiki/governance/documentation-standards.md for the page schema and
wiki/governance/agent-governance.md for the rules agents must follow.
"""

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WIKI_DIR = os.path.join(REPO_ROOT, "wiki")
GRAPH_DIR = os.path.join(REPO_ROOT, "graph")
GRAPH_JSON = os.path.join(GRAPH_DIR, "knowledge-graph.json")
GRAPH_MERMAID = os.path.join(GRAPH_DIR, "knowledge-graph.mmd")
CONFIG_PATH = os.path.join(REPO_ROOT, "openwiki.config.json")
BUILD_DIR = os.path.join(REPO_ROOT, "build", "confluence")

PAGE_TYPES = ("overview", "hardware", "library", "guide", "decision", "governance")
PAGE_STATUSES = ("stub", "draft", "active", "verified", "archived")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK_RE = re.compile(r"\[\[([a-z0-9/_-]+)\]\]")
LIST_FIELDS = ("owners", "tags", "documents", "related")
REQUIRED_FIELDS = ("id", "title", "type", "status", "owners", "created", "updated")
OPTIONAL_FIELDS = (
    "tags",
    "documents",
    "related",
    "last_verified",
    "confluence_space",
    "confluence_page_id",
    "confluence_parent",
)


# ---------------------------------------------------------------------------
# Frontmatter parsing (deliberately strict subset of YAML: flat `key: value`
# pairs; lists only as inline `[a, b]`)
# ---------------------------------------------------------------------------

class PageError(Exception):
    pass


def parse_frontmatter(text, path):
    if not text.startswith("---\n"):
        raise PageError("missing frontmatter block (page must start with '---')")
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        raise PageError("unterminated frontmatter block")
    header, body = text[4:end], text[end + 5:]
    meta = {}
    for lineno, line in enumerate(header.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":
            raise PageError("line %d: nested/indented keys are not supported" % lineno)
        if ":" not in line:
            raise PageError("line %d: expected 'key: value'" % lineno)
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.strip()
        if key in meta:
            raise PageError("line %d: duplicate key '%s'" % (lineno, key))
        if key in LIST_FIELDS:
            if not (raw.startswith("[") and raw.endswith("]")):
                raise PageError("line %d: '%s' must be an inline list: [a, b]" % (lineno, key))
            inner = raw[1:-1].strip()
            meta[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key] = raw.strip("'\"")
    return meta, body


class Page(object):
    def __init__(self, relpath, meta, body):
        self.relpath = relpath          # path relative to wiki/, e.g. hardware/thermometer.md
        self.meta = meta
        self.body = body
        self.id = meta.get("id", "")
        self.errors = []

    @property
    def wikilinks(self):
        # fenced code blocks and inline code spans may show [[...]] as syntax
        # examples; those must not become links/edges
        prose = re.sub(r"```.*?```", "", self.body, flags=re.S)
        prose = re.sub(r"`[^`]*`", "", prose)
        return sorted(set(WIKILINK_RE.findall(prose)))


def discover_pages():
    pages = []
    for dirpath, dirnames, filenames in os.walk(WIKI_DIR):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("_"))
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, WIKI_DIR).replace(os.sep, "/")
            with open(full, "r", encoding="utf-8") as fh:
                # normalize CRLF — a Windows (core.autocrlf) checkout must not
                # break frontmatter parsing
                text = fh.read().replace("\r\n", "\n")
            try:
                meta, body = parse_frontmatter(text, rel)
                pages.append(Page(rel, meta, body))
            except PageError as exc:
                page = Page(rel, {}, "")
                page.errors.append(str(exc))
                pages.append(page)
    return pages


# ---------------------------------------------------------------------------
# Config / artifact discovery
# ---------------------------------------------------------------------------

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _matches_any(rel, patterns):
    # fnmatchcase: fnmatch is case-insensitive on Windows (os.path.normcase),
    # which would make governed/documented sets platform-dependent
    return any(fnmatch.fnmatchcase(rel, p) or fnmatch.fnmatchcase(os.path.basename(rel), p)
               for p in patterns)


def governed_artifacts(config):
    """Return sorted repo-relative paths of artifacts that require documentation.

    Directory artifacts (e.g. *.pretty footprint libraries) are matched as a
    directory path and reported once, not per contained file.
    """
    include = config.get("governed", [])
    ignore = config.get("ignore", [])
    found = set()
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        rel_dir = os.path.relpath(dirpath, REPO_ROOT).replace(os.sep, "/")
        if rel_dir == ".":
            rel_dir = ""
        pruned = []
        for d in sorted(dirnames):
            rel = (rel_dir + "/" + d).lstrip("/")
            if d in (".git", ".claude") or _matches_any(rel, ignore):
                continue
            if _matches_any(rel, include):
                found.add(rel)   # directory-level artifact; don't descend
                continue
            pruned.append(d)
        dirnames[:] = pruned
        for name in sorted(filenames):
            rel = (rel_dir + "/" + name).lstrip("/")
            if _matches_any(rel, ignore):
                continue
            if _matches_any(rel, include):
                found.add(rel)
    return sorted(found)


def git_last_commit_date(relpath):
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", relpath],
            cwd=REPO_ROOT, stderr=subprocess.DEVNULL)
        return out.decode().strip() or None
    except (subprocess.CalledProcessError, OSError):
        return None


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------

def validate(pages, config, report=True):
    errors = []
    ids = {}
    for page in pages:
        prefix = "wiki/%s: " % page.relpath
        for err in page.errors:
            errors.append(prefix + err)
        if page.errors:
            continue
        meta = page.meta
        for field in REQUIRED_FIELDS:
            if field not in meta or meta[field] in ("", []):
                errors.append(prefix + "missing required field '%s'" % field)
        for field in meta:
            if field not in REQUIRED_FIELDS + OPTIONAL_FIELDS:
                errors.append(prefix + "unknown field '%s'" % field)
        expected_id = page.relpath[:-3]
        if meta.get("id") and meta["id"] != expected_id:
            errors.append(prefix + "id '%s' must match file path ('%s')" % (meta["id"], expected_id))
        if meta.get("type") and meta["type"] not in PAGE_TYPES:
            errors.append(prefix + "type '%s' not one of %s" % (meta["type"], "/".join(PAGE_TYPES)))
        if meta.get("status") and meta["status"] not in PAGE_STATUSES:
            errors.append(prefix + "status '%s' not one of %s" % (meta["status"], "/".join(PAGE_STATUSES)))
        for field in ("created", "updated", "last_verified"):
            val = meta.get(field)
            if val and not DATE_RE.match(val):
                errors.append(prefix + "%s '%s' is not an ISO date (YYYY-MM-DD)" % (field, val))
        if meta.get("status") == "verified" and not meta.get("last_verified"):
            errors.append(prefix + "status 'verified' requires a last_verified date")
        if meta.get("id"):
            if meta["id"] in ids:
                errors.append(prefix + "duplicate id (also in wiki/%s)" % ids[meta["id"]])
            ids[meta["id"]] = page.relpath
    # cross-references (second pass, only over structurally valid pages)
    for page in pages:
        if page.errors or not page.meta.get("id"):
            continue
        prefix = "wiki/%s: " % page.relpath
        for target in page.meta.get("related", []) + page.wikilinks:
            if target not in ids:
                errors.append(prefix + "link to unknown page '%s'" % target)
        for doc in page.meta.get("documents", []):
            hits = [p for p in _all_repo_paths() if fnmatch.fnmatchcase(p, doc)] \
                if any(c in doc for c in "*?[") \
                else ([doc] if os.path.exists(os.path.join(REPO_ROOT, doc)) else [])
            if not hits:
                errors.append(prefix + "documents entry '%s' matches nothing in the repo" % doc)
    if report:
        _report("validate", errors)
    return errors


_repo_paths_cache = None


def _all_repo_paths():
    global _repo_paths_cache
    if _repo_paths_cache is None:
        paths = []
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            rel_dir = os.path.relpath(dirpath, REPO_ROOT).replace(os.sep, "/")
            if rel_dir == ".":
                rel_dir = ""
            for d in dirnames:
                paths.append((rel_dir + "/" + d).lstrip("/"))
            for f in filenames:
                paths.append((rel_dir + "/" + f).lstrip("/"))
        _repo_paths_cache = sorted(paths)
    return _repo_paths_cache


# ---------------------------------------------------------------------------
# knowledge graph
# ---------------------------------------------------------------------------

def _covers(page, artifact):
    for doc in page.meta.get("documents", []):
        if doc == artifact or fnmatch.fnmatchcase(artifact, doc):
            return True
    return False


def build_graph(pages, config):
    nodes, edges = [], []
    valid = [p for p in pages if not p.errors and p.meta.get("id")]
    artifacts = governed_artifacts(config)

    for page in valid:
        m = page.meta
        nodes.append({
            "id": "wiki:" + m["id"],
            "kind": "page",
            "title": m.get("title", ""),
            "type": m.get("type", ""),
            "status": m.get("status", ""),
            "updated": m.get("updated", ""),
            "confluence_page_id": m.get("confluence_page_id", ""),
        })
        for owner in m.get("owners", []):
            nodes.append({"id": "owner:" + owner, "kind": "owner", "title": owner})
            edges.append({"from": "owner:" + owner, "to": "wiki:" + m["id"], "rel": "owns"})
        for tag in m.get("tags", []):
            nodes.append({"id": "tag:" + tag, "kind": "tag", "title": tag})
            edges.append({"from": "wiki:" + m["id"], "to": "tag:" + tag, "rel": "tagged"})
        for target in m.get("related", []):
            edges.append({"from": "wiki:" + m["id"], "to": "wiki:" + target, "rel": "related"})
        for target in page.wikilinks:
            edges.append({"from": "wiki:" + m["id"], "to": "wiki:" + target, "rel": "references"})

    for artifact in artifacts:
        documenting = sorted(p.meta["id"] for p in valid if _covers(p, artifact))
        nodes.append({
            "id": "artifact:" + artifact,
            "kind": "artifact",
            "title": artifact,
            "documented": bool(documenting),
        })
        for pid in documenting:
            edges.append({"from": "wiki:" + pid, "to": "artifact:" + artifact, "rel": "documents"})

    # de-duplicate and order deterministically
    nodes = sorted({n["id"]: n for n in nodes}.values(), key=lambda n: n["id"])
    edges = sorted({(e["from"], e["to"], e["rel"]): e for e in edges}.values(),
                   key=lambda e: (e["from"], e["to"], e["rel"]))
    digest = hashlib.sha256(
        json.dumps({"nodes": nodes, "edges": edges}, sort_keys=True).encode()).hexdigest()
    return {
        "version": 1,
        "generated_by": "tools/openwiki/openwiki.py graph",
        "source_digest": digest,
        "counts": {"nodes": len(nodes), "edges": len(edges)},
        "nodes": nodes,
        "edges": edges,
    }


def render_mermaid(graph):
    def mid(node_id):
        return re.sub(r"[^A-Za-z0-9]", "_", node_id)
    lines = ["%% Generated by tools/openwiki/openwiki.py graph — do not edit by hand",
             "graph LR"]
    shapes = {"page": ('["%s"]'), "artifact": ('[("%s")]'), "owner": ('(["%s"])'), "tag": ('{{"%s"}}')}
    for node in graph["nodes"]:
        if node["kind"] == "tag":
            continue  # tags overwhelm the diagram; they stay in the JSON
        shape = shapes[node["kind"]] % node["title"].replace('"', "'")
        lines.append("    %s%s" % (mid(node["id"]), shape))
    for edge in graph["edges"]:
        if edge["rel"] == "tagged":
            continue
        lines.append("    %s -->|%s| %s" % (mid(edge["from"]), edge["rel"], mid(edge["to"])))
    return "\n".join(lines) + "\n"


def write_graph(graph):
    os.makedirs(GRAPH_DIR, exist_ok=True)
    with open(GRAPH_JSON, "w", encoding="utf-8") as fh:
        json.dump(graph, fh, indent=2, sort_keys=False)
        fh.write("\n")
    with open(GRAPH_MERMAID, "w", encoding="utf-8") as fh:
        fh.write(render_mermaid(graph))


def graph_check(graph):
    if not os.path.exists(GRAPH_JSON):
        return ["graph/knowledge-graph.json does not exist — run 'openwiki graph'"]
    with open(GRAPH_JSON, "r", encoding="utf-8") as fh:
        try:
            committed = json.load(fh)
        except ValueError:
            return ["graph/knowledge-graph.json is not valid JSON — regenerate it"]
    if committed.get("source_digest") != graph["source_digest"]:
        return ["knowledge graph is out of sync with the wiki — run "
                "'python3 tools/openwiki/openwiki.py graph' and commit the result"]
    return []


# ---------------------------------------------------------------------------
# verify (documentation coverage + staleness)
# ---------------------------------------------------------------------------

def verify(pages, config, strict=False, report=True):
    errors, warnings = [], []
    valid = [p for p in pages if not p.errors and p.meta.get("id")]
    covering_statuses = ("active", "verified")
    for artifact in governed_artifacts(config):
        documenting = [p for p in valid if _covers(p, artifact)]
        live = [p for p in documenting if p.meta.get("status") in covering_statuses]
        if not documenting:
            errors.append("undocumented artifact: %s (no wiki page lists it in 'documents')"
                          % artifact)
        elif not live:
            errors.append("artifact %s is only documented by non-active pages (%s) — "
                          "promote a page to active/verified"
                          % (artifact, ", ".join(p.meta["id"] + ":" + p.meta.get("status", "?")
                                                 for p in documenting)))
        else:
            changed = git_last_commit_date(artifact)
            for page in live:
                if changed and page.meta.get("updated", "") < changed:
                    warnings.append("stale: %s changed %s but wiki/%s was last updated %s"
                                    % (artifact, changed, page.relpath, page.meta["updated"]))
    for page in valid:
        if page.meta.get("status") == "stub":
            warnings.append("stub page awaiting content: wiki/%s" % page.relpath)
    if strict:
        errors, warnings = errors + warnings, []
    if report:
        for w in warnings:
            print("WARN  " + w)
        _report("verify", errors)
    return errors


# ---------------------------------------------------------------------------
# confluence export
# ---------------------------------------------------------------------------

def md_to_storage(body):
    """Convert the OpenWiki markdown subset to Confluence storage format.

    Handles: headings, paragraphs, bold/italic/code spans, fenced code blocks,
    unordered/ordered lists, tables, links, and [[wikilinks]]. Anything fancier
    should be simplified in the source page.
    """
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def spans(s):
        s = esc(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"\[\[([a-z0-9/_-]+)\]\]", r'<em>[wiki:\1]</em>', s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    out, lines, i = [], body.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            code, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append('<ac:structured-macro ac:name="code"><ac:plain-text-body>'
                       "<![CDATA[%s]]></ac:plain-text-body></ac:structured-macro>"
                       % "\n".join(code))
        elif re.match(r"^#{1,6} ", line):
            level = len(line) - len(line.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (level, spans(line[level + 1:]), level))
        elif re.match(r"^[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                items.append("<li>%s</li>" % spans(lines[i][2:]))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
            continue
        elif re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append("<li>%s</li>" % spans(re.sub(r"^\d+\. ", "", lines[i])))
                i += 1
            out.append("<ol>%s</ol>" % "".join(items))
            continue
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                if not all(re.match(r"^:?-+:?$", c) for c in cells):
                    rows.append(cells)
                i += 1
            html = []
            for r, cells in enumerate(rows):
                tag = "th" if r == 0 else "td"
                html.append("<tr>%s</tr>" % "".join("<%s>%s</%s>" % (tag, spans(c), tag)
                                                    for c in cells))
            out.append("<table><tbody>%s</tbody></table>" % "".join(html))
            continue
        elif line.strip():
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(#{1,6} |[-*] |\d+\. |\||```)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % spans(" ".join(para)))
            continue
        i += 1
    return "\n".join(out) + "\n"


def confluence_export(pages, config):
    os.makedirs(BUILD_DIR, exist_ok=True)
    manifest = {"space_default": config.get("confluence", {}).get("space", ""),
                "generated_by": "tools/openwiki/openwiki.py confluence",
                "pages": []}
    exported = 0
    for page in sorted(pages, key=lambda p: p.meta.get("id", "")):
        if page.errors or not page.meta.get("id"):
            continue
        if page.meta.get("status") not in ("active", "verified"):
            continue
        xhtml = md_to_storage(page.body)
        rel = page.meta["id"].replace("/", "__") + ".xhtml"
        with open(os.path.join(BUILD_DIR, rel), "w", encoding="utf-8") as fh:
            fh.write(xhtml)
        manifest["pages"].append({
            "id": page.meta["id"],
            "title": page.meta.get("title", ""),
            "file": rel,
            "space": page.meta.get("confluence_space")
                     or config.get("confluence", {}).get("space", ""),
            "page_id": page.meta.get("confluence_page_id", ""),
            "parent": page.meta.get("confluence_parent", ""),
            "content_sha256": hashlib.sha256(xhtml.encode()).hexdigest(),
        })
        exported += 1
    with open(os.path.join(BUILD_DIR, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print("exported %d page(s) to %s" % (exported, os.path.relpath(BUILD_DIR, REPO_ROOT)))
    print("push with a Confluence REST client per wiki/governance/confluence-sync.md")


# ---------------------------------------------------------------------------
# new (scaffold a page)
# ---------------------------------------------------------------------------

def new_page(page_type, page_id):
    if page_type not in PAGE_TYPES:
        raise SystemExit("unknown type '%s'; expected one of: %s"
                         % (page_type, ", ".join(PAGE_TYPES)))
    if not re.fullmatch(r"[a-z0-9][a-z0-9/_-]*", page_id):
        raise SystemExit("invalid page id '%s' — use lowercase [a-z0-9/_-] "
                         "(e.g. hardware/my-board)" % page_id)
    template = os.path.join(WIKI_DIR, "_templates", page_type + ".md")
    dest = os.path.normpath(os.path.join(WIKI_DIR, page_id + ".md"))
    if not dest.startswith(os.path.normpath(WIKI_DIR) + os.sep):
        raise SystemExit("page id escapes wiki/")
    if os.path.exists(dest):
        raise SystemExit("wiki/%s.md already exists" % page_id)
    with open(template, "r", encoding="utf-8") as fh:
        text = fh.read()
    today = date.today().isoformat()
    text = (text.replace("{{id}}", page_id)
                .replace("{{title}}", os.path.basename(page_id).replace("-", " ").title())
                .replace("{{date}}", today))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("created wiki/%s.md — fill it in, then run 'openwiki check'" % page_id)


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def _report(name, errors):
    for err in errors:
        print("ERROR " + err)
    print("%s: %s (%d error%s)" % (name, "FAIL" if errors else "OK",
                                   len(errors), "" if len(errors) == 1 else "s"))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="openwiki", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    g = sub.add_parser("graph")
    g.add_argument("--check", action="store_true", help="fail if committed graph is stale")
    v = sub.add_parser("verify")
    v.add_argument("--strict", action="store_true", help="treat warnings as errors")
    sub.add_parser("check")
    n = sub.add_parser("new")
    n.add_argument("type", choices=PAGE_TYPES)
    n.add_argument("id", help="page id, e.g. hardware/my-board")
    sub.add_parser("confluence")
    args = parser.parse_args(argv)

    if args.command == "new":
        new_page(args.type, args.id)
        return 0

    config = load_config()
    pages = discover_pages()

    if args.command == "validate":
        return 1 if validate(pages, config) else 0
    if args.command == "verify":
        return 1 if verify(pages, config, strict=args.strict) else 0
    if args.command == "graph":
        graph = build_graph(pages, config)
        if args.check:
            errors = graph_check(graph)
            _report("graph --check", errors)
            return 1 if errors else 0
        write_graph(graph)
        print("wrote graph/knowledge-graph.json (%d nodes, %d edges) and "
              "graph/knowledge-graph.mmd" % (graph["counts"]["nodes"], graph["counts"]["edges"]))
        return 0
    if args.command == "confluence":
        errors = validate(pages, config, report=False)
        if errors:
            _report("validate", errors)
            return 1
        confluence_export(pages, config)
        return 0
    if args.command == "check":
        failed = bool(validate(pages, config))
        failed |= bool(verify(pages, config))
        errors = graph_check(build_graph(pages, config))
        _report("graph --check", errors)
        failed |= bool(errors)
        return 1 if failed else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
