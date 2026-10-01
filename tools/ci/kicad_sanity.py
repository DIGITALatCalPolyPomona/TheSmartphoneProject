#!/usr/bin/env python3
"""KiCad repository sanity checks — stdlib-only, runs in CI and locally.

Checks (blocking):
  * every KiCad S-expression file has balanced parentheses and the correct
    root node (kicad_sch / kicad_pcb / kicad_symbol_lib / kicad_mod)
  * every project-local URI (${KIPRJMOD}/...) in sym-lib-table and
    fp-lib-table resolves to a path that exists in the repo

Checks (non-blocking warnings):
  * schematic (lib_id "LIB:SYMBOL") references whose LIB is not registered
    in sym-lib-table — e.g. the known-missing BMP581 library. These are
    warnings, not failures, until the library is committed; flip to
    blocking afterwards if desired.

Exit 0 = pass (warnings allowed), 1 = at least one blocking failure.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SEXP_FILES = [
    ("thermometer.kicad_sch", ("kicad_sch",)),
    ("thermometer.kicad_pcb", ("kicad_pcb",)),
    ("jackboys.kicad_sym", ("kicad_symbol_lib",)),
]

# Symbol libraries provided by every KiCad install — never in project tables.
BUILTIN_SYM_LIBS = {"Device", "power", "Connector", "Connector_Generic",
                    "Connector_PinHeader_1.00mm", "Mechanical"}

errors = []
warnings = []


def fail(msg):
    errors.append(msg)
    print(f"::error::{msg}")


def warn(msg):
    warnings.append(msg)
    print(f"::warning::{msg}")


def strip_strings_and_comments(text):
    """Remove double-quoted strings (with escapes) and ;-comments so parens
    inside them can't skew the balance check."""
    out = []
    i = 0
    in_str = False
    while i < len(text):
        c = text[i]
        if in_str:
            if c == "\\":
                i += 1
            elif c == '"':
                in_str = False
            out.append(" ")
        elif c == '"':
            in_str = True
            out.append(" ")
        elif c == ";":
            while i < len(text) and text[i] != "\n":
                i += 1
            out.append("\n")
            continue
        else:
            out.append(c)
        i += 1
    return "".join(out)


def check_sexp(path, expected_root):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        fail(f"{path}: file missing")
        return
    try:
        text = open(full, encoding="utf-8").read()
    except UnicodeDecodeError:
        fail(f"{path}: not valid UTF-8")
        return
    stripped = strip_strings_and_comments(text)
    if stripped.count("(") != stripped.count(")"):
        fail(
            f"{path}: unbalanced parentheses "
            f"({stripped.count('(')} open vs {stripped.count(')')} close)"
        )
        return
    m = re.match(r"\s*\(\s*([A-Za-z0-9_]+)", stripped)
    if not m or m.group(1) not in expected_root:
        got = m.group(1) if m else "none"
        fail(f"{path}: expected root node ({'|'.join(expected_root)} ...), found ({got} ...)")
    return text


def check_footprint_lib(dirpath):
    if not os.path.isdir(dirpath):
        fail(f"{dirpath}: footprint library directory missing")
        return
    for name in sorted(os.listdir(dirpath)):
        if name.endswith(".kicad_mod"):
            check_sexp(os.path.join(dirpath, name), ("footprint", "module"))


def parse_lib_table(path):
    """Return list of (name, uri) for each (lib (name X)(type T)(uri U)...)."""
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        fail(f"{path}: file missing")
        return []
    text = open(full, encoding="utf-8").read()
    entries = []
    for m in re.finditer(
        r'\(lib\s+\(name\s+"?([^")\s]+)"?\)\s*\(type\s+"?([^")\s]+)"?\)\s*\(uri\s+"([^"]+)"\)',
        text,
    ):
        entries.append((m.group(1), m.group(2), m.group(3)))
    return entries


def main():
    sch_text = None
    for path, root in SEXP_FILES:
        t = check_sexp(path, root)
        if path.endswith(".kicad_sch"):
            sch_text = t
    check_footprint_lib(os.path.join(ROOT, "jackboys2.pretty"))

    sym_libs = parse_lib_table("sym-lib-table")
    fp_libs = parse_lib_table("fp-lib-table")
    for table, entries in (("sym-lib-table", sym_libs), ("fp-lib-table", fp_libs)):
        for name, _type, uri in entries:
            resolved = uri.replace("${KIPRJMOD}", ROOT).replace(
                "${KICAD9_3RD_PARTY}", os.path.expanduser("~/kicad/9.0/3rdparty")
            )
            if uri.startswith("${KIPRJMOD}") and not os.path.exists(resolved):
                fail(f"{table}: lib '{name}' uri {uri} does not resolve in repo")
            elif not uri.startswith("${KIPRJMOD}"):
                warn(
                    f"{table}: lib '{name}' uses non-project uri {uri} "
                    "(depends on the opening machine's KiCad install)"
                )

    if sch_text:
        for lib in sorted(set(re.findall(r'\(lib_id\s+"([^":\s]+):', sch_text))):
            if lib in BUILTIN_SYM_LIBS:
                continue
            if lib not in [n for n, _, _ in sym_libs]:
                warn(
                    f"thermometer.kicad_sch references symbol library '{lib}' "
                    "which is not registered in sym-lib-table"
                )

    print("-" * 60)
    print(f"kicad-sanity: {len(errors)} error(s), {len(warnings)} warning(s)")
    for e in errors:
        print(f"  ERROR   {e}")
    for w in warnings:
        print(f"  WARNING {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
