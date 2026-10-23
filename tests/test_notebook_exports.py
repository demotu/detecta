"""Publishing checks run with the optional docs tools installed."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("marimo", reason="Install the docs dependency group")

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def native_html():
    session = {"cells": [{"outputs": [{"data": {"text/plain": "Saved result"}}]}]}
    return (
        '<html><head></head><body><div id="root"></div><script>\n  "session": '
        + json.dumps(session)
        + ",\n</script></body></html>"
    )


@pytest.fixture
def root(tmp_path):
    (tmp_path / "docs").mkdir()
    for name in ("pilot", "other"):
        (tmp_path / "docs" / f"{name}.py").write_text(
            'import marimo\napp = marimo.App()\n@app.cell\ndef _():\n    print("Result: 4")\n'
        )
    (tmp_path / "pyproject.toml").write_text('[project]\nname="fixture"\n')
    (tmp_path / "uv.lock").write_text("fixture lock")
    return tmp_path


def test_navigation_switches_modes_and_keeps_plain_cloud_launches(root):
    saved = load("export_notebooks")
    static = saved.decorate(native_html(), "docs/detect_peaks.py", editable=False)
    editor = saved.decorate(native_html(), "docs/detect_peaks.py", editable=True)
    assert 'href="../../detect_peaks.html"' in static
    assert 'href="docs/html/detect_peaks.html"' in editor
    assert 'href="index.html"' in editor
    assert 'href="../../index.html"' in saved.catalog(
        root, ["docs/pilot.py"], editable=False
    )
    assert "/master/docs/detect_peaks.py/wasm" not in static
    assert (
        "https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_peaks.py"
        in static
    )
    assert (
        "https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_peaks.py"
        in static
    )


def test_discovery_includes_new_notebooks_but_not_helpers(root):
    saved = load("export_notebooks")
    (root / "docs/helper.py").write_text("def helper(): pass\n")
    assert saved.discover(root) == ["docs/other.py", "docs/pilot.py"]
    (root / "docs/new.py").write_text("import marimo\napp = marimo.App()\n")
    assert "docs/new.py" in saved.discover(root)


def test_freshness_detects_source_shared_inputs_and_output_tampering(root, monkeypatch):
    saved = load("export_notebooks")

    def execute(args, **kwargs):
        assert kwargs["env"]["MPLBACKEND"] == "module://marimo._output.mpl"
        Path(args[args.index("-o") + 1]).write_text(native_html())
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(saved.subprocess, "run", execute)
    assert saved.main([], root=root) == 0
    assert saved.main(["--check"], root=root) == 0
    source = root / "docs/pilot.py"
    source.write_text(source.read_text() + "# Updated explanation\n")
    assert saved.main(["--check"], root=root) == 1
    assert saved.main(["docs/pilot.py"], root=root) == 0
    assert saved.main(["--check"], root=root) == 0
    (root / "uv.lock").write_text("changed lock")
    assert saved.main(["--check"], root=root) == 1
    assert saved.main([], root=root) == 0
    (root / "docs/html/pilot.html").write_text("damaged output")
    assert saved.main(["--check"], root=root) == 1


def test_missing_export_check_is_read_only(root):
    saved = load("export_notebooks")
    assert saved.main(["--check"], root=root) == 1
    assert not (root / "docs/html").exists()


def test_catalog_check_detects_missing_or_tampered_catalog_without_writing(
    root, monkeypatch
):
    saved = load("export_notebooks")

    def execute(args, **kwargs):
        Path(args[args.index("-o") + 1]).write_text(native_html())
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(saved.subprocess, "run", execute)
    assert saved.main([], root=root) == 0
    catalog = root / "docs/html/index.html"
    catalog.write_text("damaged catalog")
    assert saved.main(["--check"], root=root) == 1
    assert catalog.read_text() == "damaged catalog"
    catalog.unlink()
    assert saved.main(["--check"], root=root) == 1
    assert not catalog.exists()
    assert saved.main([], root=root) == 0
    assert 'href="pilot.html"' in catalog.read_text()
    assert saved.main(["--check"], root=root) == 0


def test_failed_export_preserves_saved_page_and_reports_stale_state(root, monkeypatch):
    saved = load("export_notebooks")
    assert saved.main([], root=root) == 0
    page = root / "docs/html/pilot.html"
    previous = page.read_bytes()
    monkeypatch.setattr(
        saved.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            [], 1, stdout="", stderr="Cell failed"
        ),
    )
    assert saved.main(["--force"], root=root) == 1
    assert page.read_bytes() == previous
    assert saved.main(["--check"], root=root) == 1


def test_bad_native_document_does_not_replace_saved_page(root, monkeypatch):
    saved = load("export_notebooks")
    assert saved.main([], root=root) == 0
    page = root / "docs/html/pilot.html"
    previous = page.read_bytes()

    def execute(args, **kwargs):
        Path(args[args.index("-o") + 1]).write_text("Not a notebook document")
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(saved.subprocess, "run", execute)
    assert saved.main(["docs/pilot.py", "--force"], root=root) == 1
    assert page.read_bytes() == previous


def test_native_execution_saves_plot_and_printed_result(root):
    saved = load("export_notebooks")
    (root / "docs/pilot.py").write_text("""import marimo
app = marimo.App()
@app.cell
def _():
    import matplotlib.pyplot as plt
    plt.plot([0, 1], [1, 0])
    plt.show()
    print("Visible result: 4")
""")
    assert saved.main(["docs/pilot.py"], root=root) == 0
    page = (root / "docs/html/pilot.html").read_text()
    assert "image/png" in page or "image/svg+xml" in page
    assert "Visible result: 4" in page


def test_native_export_preserves_existing_source_session_cache(root):
    saved = load("export_notebooks")
    cache = root / "docs/__marimo__/session/pilot.py.json"
    cache.parent.mkdir(parents=True)
    previous = json.dumps(
        {
            "version": "1",
            "metadata": {"marimo_version": "0.25.2", "script_metadata_hash": None},
            "cells": [],
        }
    )
    cache.write_text(previous)
    assert saved.main(["docs/pilot.py"], root=root) == 0
    assert cache.read_text() == previous


@pytest.fixture
def site(root):
    site = root / "_site"
    saved = site / "docs/html"
    saved.mkdir(parents=True)
    (saved / "index.html").write_text("Saved catalog")
    for name in ("pilot", "other"):
        (saved / f"{name}.html").write_text("Saved " + name)
    (site / "index.html").write_text("Cayman home")
    (site / "assets/css").mkdir(parents=True)
    (site / "assets/css/style.css").write_text("Cayman theme")
    return site


def test_real_editable_exports_merge_assets_and_preserve_home_and_saved_pages(
    root, site
):
    editable = load("export_editable")
    result = editable.build(site, root=root)
    assert len(result["notebooks"]) == 2
    assert '"mode": "edit"' in (site / "pilot.html").read_text()
    assert 'href="docs/html/pilot.html"' in (site / "pilot.html").read_text()
    assert (site / "index.html").read_text() == "Cayman home"
    assert (site / "assets/css/style.css").read_text() == "Cayman theme"
    assert (site / "docs/html/pilot.html").read_text() == "Saved pilot"
    assert list((site / "assets").glob("*.js"))


def test_failed_native_editor_export_preserves_previous_editor(root, site, monkeypatch):
    editable = load("export_editable")
    (site / "pilot.html").write_text("Previous editor")
    monkeypatch.setattr(
        editable.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            [], 1, stdout="", stderr="Export failed"
        ),
    )
    with pytest.raises(RuntimeError):
        editable.build(site, root=root)
    assert (site / "pilot.html").read_text() == "Previous editor"
    assert (site / "index.html").read_text() == "Cayman home"


def test_generated_local_catalog_refreshes_and_retired_editors_are_removed(root, site):
    editable = load("export_editable")
    (site / "index.html").unlink()
    editable.build(site, root=root)
    assert 'href="other.html"' in (site / "index.html").read_text()
    (root / "docs/other.py").unlink()
    editable.build(site, root=root)
    assert not (site / "other.html").exists()
    assert 'href="other.html"' not in (site / "index.html").read_text()
    assert (site / "assets/css/style.css").read_text() == "Cayman theme"


def test_index_notebook_and_repository_root_destination_are_rejected(root, site):
    editable = load("export_editable")
    with pytest.raises(ValueError):
        editable.build(root, root=root)
    (root / "docs/index.py").write_text("import marimo\napp = marimo.App()\n")
    with pytest.raises(ValueError, match="index.html"):
        editable.build(site, root=root)
    assert (site / "index.html").read_text() == "Cayman home"
