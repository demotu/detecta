"""Add native editable notebooks to a Pages build. See scripts/README.md."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path

from export_notebooks import (
    READ_DIR,
    ROOT,
    atomic_write,
    catalog,
    decorate,
    digest,
    discover,
    output_path,
)


def build(site: Path, *, root: Path = ROOT) -> dict:
    site = site.resolve()
    if site == root.resolve():
        raise ValueError("Use a separate site build directory, not the repository root")
    sources = discover(root)
    if not sources:
        raise ValueError("No marimo notebooks found in docs/")
    if any(output_path(source) == "index.html" for source in sources):
        raise ValueError("index.html is reserved for the site home page")
    for page in ["index.html", *map(output_path, sources)]:
        if not (site / READ_DIR / page).is_file():
            raise ValueError(f"Build the saved pages first: missing {READ_DIR}/{page}")
    entries = []
    with tempfile.TemporaryDirectory(dir=site, prefix=".detecta-edit-") as directory:
        staging = Path(directory) / "editable"
        staging.mkdir()
        for source in sources:
            before = digest(root / source)
            target = staging / output_path(source)
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "marimo",
                    "export",
                    "html-wasm",
                    str(root / source),
                    "--mode",
                    "edit",
                    "-o",
                    str(target),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            if result.returncode:
                raise RuntimeError((result.stdout + result.stderr)[-5000:])
            if not target.is_file() or not (staging / "assets").is_dir():
                raise ValueError(f"Incomplete native export: {source}")
            if digest(root / source) != before:
                raise RuntimeError(f"{source} changed during export; rerun the builder")
            atomic_write(target, decorate(target.read_text(), source, editable=True))
            entries.append(
                {
                    "source": source,
                    "source_sha256": before,
                    "html": output_path(source),
                    "html_sha256": digest(target),
                }
            )
        home = site / "index.html"
        if not home.exists() or 'name="detecta-generated-catalog"' in home.read_text():
            atomic_write(staging / "index.html", catalog(root, sources, editable=True))
        manifest = {"mode": "edit", "marimo": version("marimo"), "notebooks": entries}
        atomic_write(
            staging / "export-manifest.json", json.dumps(manifest, indent=2) + "\n"
        )
        previous_path = site / "export-manifest.json"
        previous = (
            json.loads(previous_path.read_text()) if previous_path.is_file() else {}
        )
        retired = {
            entry["html"]
            for entry in previous.get("notebooks", [])
            if entry.get("source", "").startswith("docs/")
            and entry.get("html") == output_path(entry["source"])
            and entry["html"] != "index.html"
        } - set(map(output_path, sources))
        # Only generated files are merged; Jekyll, saved outputs and theme assets remain.
        shutil.copytree(staging, site, dirs_exist_ok=True)
        for page in retired:
            (site / page).unlink(missing_ok=True)
    (site / ".nojekyll").touch()
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        default=ROOT / "_site",
        help="Existing site build (default: _site)",
    )
    args = parser.parse_args()
    manifest = build(args.site)
    print(f"Exported {len(manifest['notebooks'])} editable notebooks to {args.site}")


if __name__ == "__main__":
    main()
