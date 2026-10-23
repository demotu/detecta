# Maintaining the published notebooks

Run from the repository root. Publishing tools have their own dependency group;
they do not change detecta's Python >=3.9 runtime support or its PyPI dependencies.

```bash
uv sync --python 3.14 --locked --group docs --extra test
uv run --group docs python scripts/export_notebooks.py
```

The updater executes every marimo notebook immediately under `docs/` and writes
saved text/plots into `docs/html/`. Newly added notebooks are discovered
automatically. Reading needs neither molab nor marimo.app; display assets still
need an Internet connection. Every page has links to its editable version and
both alternative execution services.

Update one notebook, check freshness without executing or writing, or force
new outputs:

```bash
uv run --group docs python scripts/export_notebooks.py docs/detect_peaks.py
uv run --group docs python scripts/export_notebooks.py --check
uv run --group docs python scripts/export_notebooks.py --force
```

The manifest records source, shared-input and output hashes. Changes to package
code, the lockfile, project configuration, exporter, Python or marimo invalidate
all saved pages. A source-only change invalidates that notebook. Remote changes
and nondeterministic output cannot be inferred from local hashes; use `--force`
when needed. A failed export preserves the previous HTML and leaves the snapshot
marked stale. Commit sources, saved HTML and `docs/html/manifest.json`
together. The exporter does not commit or push.

Freshness checks also validate the saved catalog and report a missing or damaged
catalog without changing it. Running the normal updater regenerates that catalog.

Native execution uses a temporary cache prefix, so the four existing committed
source-session caches remain unchanged. New marimo caches and site assets are
ignored by Git; saved HTML is the maintained reading collection.

## Editable Pages and local previews

`.github/workflows/pages.yml` runs on pushes to `master` and supports manual
execution. It installs the locked docs environment, runs package/publishing
tests, refreshes saved outputs, builds the Cayman site, exports native editable
WASM pages at the site root, and deploys the complete artifact. It replaces the
two previous competing Pages workflows; the package/release CI is unchanged.
GitHub Pages must use **GitHub Actions** as its publishing source (already set
for this repository).

To preview the notebook collection locally without installing Jekyll:

```bash
uv run --group docs python scripts/export_notebooks.py
uv run --group docs python -c "import shutil; shutil.copytree('docs/html', '_site/docs/html', dirs_exist_ok=True)"
uv run --group docs python scripts/export_editable.py --site _site
uv run --group docs python -m http.server --directory _site 8000
```

Open `http://localhost:8000/detect_peaks.html`. The complete `_site/` directory
must be served over HTTP, including the native frontend assets. The workflow
also builds the full Cayman home page. For this local shortcut, the exporter
creates a simple notebook catalog only when no home page exists; it refreshes
its own catalog on later builds and preserves an authored/Jekyll home page.
Generated editable pages/assets are kept in the deployment artifact, outside Git.

Click **Run all**, then change parameters or edit Python cells. The browser
downloads Python and notebook dependencies from public package sources. Edits
remain in your browser; download the Python file to keep them. Every editor
links to its saved outputs, and every saved page links back to its editor.

Native exports are staged before installation. If a native export fails, existing
pages remain intact and the workflow does not deploy. Installing editors merges
their generated files into the site, retaining the home page, theme assets and
saved outputs. Notebook filename `index.py` is reserved to protect the catalogs.

## Verification

```bash
uv run --group docs --extra test pytest -q
uv run --group docs ruff check scripts/ tests/test_notebook_exports.py
uv run --group docs python scripts/export_notebooks.py --check
```

Publishing tests require the docs group and are skipped when only the package's
test extra is installed, keeping the existing Python 3.9 CI independent. Review
plots and interactive behavior in the actual editor after notebook changes;
successful execution alone does not prove that every figure is displayed.
