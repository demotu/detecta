"""Maintain saved notebook HTML. See scripts/README.md for usage."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from html import escape
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READ_DIR = "docs/html"
SESSION = re.compile(r'(?m)^\s*"session": (.+),\s*$')
STYLE = """<style id="detecta-navigation-style">
body { display:flex; flex-direction:column; height:100vh; margin:0; }
#root { flex:1; min-height:0; height:0; }
#detecta-navigation { position:relative; z-index:100; flex:none; display:flex;
  align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px 24px;
  padding:12px 24px; background:#f8fafc; color:#172b3a; border-bottom:1px solid #d8e1e8;
  font:14px/1.4 system-ui,sans-serif; }
#detecta-navigation p { margin:0; }
#detecta-navigation .launches { display:flex; align-items:center; flex-wrap:wrap; gap:10px; }
#detecta-navigation .badge { padding:3px 9px; border-radius:4px; color:white;
  background:#334155; font-weight:600; text-decoration:none; }
#detecta-navigation .marimo { background:#235b43; }
#detecta-navigation a:focus-visible { outline:3px solid #2563eb; outline-offset:3px; }
@media(max-width:540px) { #detecta-navigation { padding:10px 14px; } }
@media print { #detecta-navigation { display:none; } }
</style>"""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover(root: Path) -> list[str]:
    return [
        path.relative_to(root).as_posix()
        for path in sorted((root / "docs").glob("*.py"))
        if re.search(r"\bmarimo\.App\s*\(", path.read_text())
    ]


def output_path(source: str) -> str:
    return Path(source).stem + ".html"


def title(path: Path) -> str:
    for node in ast.walk(ast.parse(path.read_text())):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "md"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            match = re.search(r"^\s*# (.+)$", node.args[0].value, re.MULTILINE)
            if match:
                return match[1].strip().removesuffix(".py")
    return path.stem


def atomic_write(path: Path, document: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(document)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def decorate(document: str, source: str, *, editable: bool) -> str:
    if document.count("<body>") != 1 or document.count("</head>") != 1:
        raise ValueError("Unsupported marimo HTML document")
    page = output_path(source)
    alternate = f"{READ_DIR}/{page}" if editable else posixpath.relpath(page, READ_DIR)
    label = "Read saved outputs" if editable else "Edit in browser"
    mode = "Editable notebook" if editable else "Saved outputs"
    hint = (
        "Run all cells, then edit and rerun. Download your Python file to keep edits."
        if editable
        else "Saved text and plots; use an interactive mode to recompute."
    )
    navigation = f'''
<nav id="detecta-navigation" aria-label="Notebook viewing and execution modes">
<p><a href="index.html">All notebooks</a> · <strong>{mode}</strong><br>{hint}</p>
<div class="launches"><a href="{escape(alternate, quote=True)}">{label}</a>
<a class="badge" href="https://molab.marimo.io/github/demotu/detecta/blob/master/{escape(source, quote=True)}" target="_blank" rel="noopener noreferrer">molab</a>
<a class="badge marimo" href="https://marimo.app/github.com/demotu/detecta/blob/master/{escape(source, quote=True)}" target="_blank" rel="noopener noreferrer">marimo.app</a></div></nav>
'''
    style = STYLE + ("<style>#root { position:relative; }</style>" if editable else "")
    document = document.replace("</head>", style + "</head>", 1).replace(
        "<body>", "<body>" + navigation, 1
    )
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def shared_digest(root: Path, sources: list[str]) -> str:
    hasher = hashlib.sha256(
        f"{sys.version}\n{version('marimo')}\n{digest(Path(__file__))}\n".encode()
    )
    hasher.update("\n".join(sources).encode())
    paths = [
        root / "pyproject.toml",
        root / "uv.lock",
        *sorted((root / "detecta").glob("*.py")),
    ]
    for path in paths:
        if path.is_file():
            hasher.update(path.relative_to(root).as_posix().encode())
            hasher.update(digest(path).encode())
    return hasher.hexdigest()


def export_one(root: Path, source: str, shared: str) -> dict:
    source_sha = digest(root / source)
    with tempfile.TemporaryDirectory(prefix="detecta-html-") as directory:
        native = Path(directory) / "notebook.html"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "marimo",
                "export",
                "html",
                str(root / source),
                "-o",
                str(native),
                "--force",
            ],
            cwd=root,
            env=os.environ
            | {
                "MPLBACKEND": "module://marimo._output.mpl",
                # marimo mirrors output caches under Python's cache prefix.
                # Keep notebook locations intact without rewriting source caches.
                "PYTHONPYCACHEPREFIX": str(Path(directory) / "cache"),
            },
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-5000:])
        document = native.read_text()
        match = SESSION.search(document)
        if match is None or not isinstance(session := json.loads(match[1]), dict):
            raise ValueError("Native export has no saved notebook session")
        document = decorate(document, source, editable=False)
    if digest(root / source) != source_sha:
        raise RuntimeError("Source changed during export; rerun the updater")
    destination = root / READ_DIR / output_path(source)
    atomic_write(destination, document)
    return {
        "source": source,
        "source_sha256": source_sha,
        "shared_inputs_sha256": shared,
        "html": output_path(source),
        "html_sha256": digest(destination),
        "cells": len(session.get("cells", [])),
        "cells_with_saved_figures": sum(
            "image/png" in json.dumps(cell) or "image/svg+xml" in json.dumps(cell)
            for cell in session.get("cells", [])
        ),
    }


def is_current(root: Path, source: str, entry: dict, shared: str) -> bool:
    page = root / READ_DIR / output_path(source)
    return bool(
        not entry.get("last_error")
        and page.is_file()
        and entry.get("source_sha256") == digest(root / source)
        and entry.get("shared_inputs_sha256") == shared
        and entry.get("html_sha256") == digest(page)
    )


def catalog(root: Path, sources: list[str], *, editable: bool) -> str:
    links = "\n".join(
        f'<li><a href="{escape(output_path(source), quote=True)}">{escape(title(root / source))}</a></li>'
        for source in sources
    )
    alternate = (
        f"{READ_DIR}/index.html"
        if editable
        else posixpath.relpath("index.html", READ_DIR)
    )
    mode = "Editable notebooks" if editable else "Saved notebook outputs"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="detecta-generated-catalog" content="true"><title>detecta · {mode}</title>
<style>body{{max-width:60rem;margin:3rem auto;padding:0 1.2rem;font:17px/1.6 system-ui,sans-serif;color:#172b3a}}a{{color:#176d52}}li{{margin:.5rem 0}}</style></head>
<body><h1>detecta · {mode}</h1><p>Event detection examples. Each notebook links to its other viewing and execution modes.</p>
<ul>{links}</ul><p><a href="{alternate}">Switch collection mode</a></p></body></html>\n'''


def main(argv=None, *, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="Source paths; default: all marimo notebooks in docs/",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check freshness without executing or writing",
    )
    parser.add_argument(
        "--force", action="store_true", help="Execute even if the saved page is current"
    )
    args = parser.parse_args(argv)
    sources = discover(root)
    selected = args.notebooks or sources
    if not selected or any(source not in sources for source in selected):
        parser.error("Select existing marimo notebooks in docs/")
    if any(output_path(source) == "index.html" for source in sources):
        parser.error("index.html is reserved for the notebook catalog")
    path = root / READ_DIR / "manifest.json"
    manifest = json.loads(path.read_text()) if path.is_file() else {}
    entries = {entry["source"]: entry for entry in manifest.get("notebooks", [])}
    shared = shared_digest(root, sources)
    stale = [
        source
        for source in selected
        if not is_current(root, source, entries.get(source, {}), shared)
    ]
    if args.check:
        catalog_path = root / READ_DIR / "index.html"
        available = [
            source
            for source in sources
            if (root / READ_DIR / output_path(source)).is_file()
        ]
        catalog_current = (
            catalog_path.is_file()
            and catalog_path.read_text() == catalog(root, available, editable=False)
        )
        print(
            f"{len(selected) - len(stale)}/{len(selected)} selected exports are current"
        )
        if not catalog_current:
            print("Saved catalog is missing or stale")
        return int(bool(stale) or not catalog_current)
    failures = 0
    for source in selected:
        if not args.force and source not in stale:
            continue
        try:
            entries[source] = export_one(root, source, shared)
            print("EXPORTED", source, flush=True)
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            entries[source] = entries.get(source, {"source": source}) | {
                "last_error": str(error)
            }
            print(f"FAILED {source}: {error}", file=sys.stderr, flush=True)
            failures += 1
    manifest = {
        "exporter": "marimo export html",
        "notebooks": [entries[source] for source in sources if source in entries],
    }
    atomic_write(path, json.dumps(manifest, indent=2) + "\n")
    available = [
        source
        for source in sources
        if (root / READ_DIR / output_path(source)).is_file()
    ]
    atomic_write(
        root / READ_DIR / "index.html", catalog(root, available, editable=False)
    )
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
