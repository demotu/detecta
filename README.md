# [detecta](https://pypi.org/project/detecta/)

[![PyPI version](https://badge.fury.io/py/detecta.svg)](https://badge.fury.io/py/detecta) 
[![DOI](https://zenodo.org/badge/250680438.svg)](https://zenodo.org/badge/latestdoi/250680438)

Python module to detect events in data

The following functions are implemented in detecta:  

- **detect_peaks.py**: detects peaks in data based on their amplitude and other features.  
- **detect_onset.py**: detects onset in data based on amplitude threshold.  
- **detect_cusum.py**: detects abrupt changes in data using cumulative sum algorithm (CUSUM).  
- **detect_seq.py**: detects initial and final indices of sequential data identical to a parameter.

## Installation

```bash
pip install detecta
```

The plots (parameter `show=True`) require matplotlib, which can be installed together with:

```bash
pip install "detecta[plot]"
```

Or

```bash
conda install -c duartexyz detecta
```

## Examples

The examples are [marimo](https://marimo.io) notebooks in [docs/](https://github.com/demotu/detecta/tree/master/docs). Click a notebook name to open its **editable GitHub Pages version**. Click **Run all**, then edit and rerun cells to experiment. Download the Python file to keep your changes; browser edits do not update this repository.

- [detect_peaks](https://demotu.github.io/detecta/detect_peaks.html) [![molab][molab-badge]](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_peaks.py) [![marimo][marimo-badge]](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_peaks.py)
- [detect_onset](https://demotu.github.io/detecta/detect_onset.html) [![molab][molab-badge]](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_onset.py) [![marimo][marimo-badge]](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_onset.py)
- [detect_cusum](https://demotu.github.io/detecta/detect_cusum.html) [![molab][molab-badge]](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_cusum.py) [![marimo][marimo-badge]](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_cusum.py)
- [detect_seq](https://demotu.github.io/detecta/detect_seq.html) [![molab][molab-badge]](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_seq.py) [![marimo][marimo-badge]](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_seq.py)

Every notebook links to its **Read saved outputs** version in [docs/html/](https://demotu.github.io/detecta/docs/html/). Those pages contain saved text and plots and can be read without running Python; their controls cannot recompute results. Both modes are hosted on this repository's GitHub Pages site independently of molab and marimo.app. The compact badges provide alternative interactive services; their molab links use the standard execution mode.

Editable Pages notebooks run Python through [WebAssembly](https://docs.marimo.io/guides/wasm/). They still download their runtime and packages, and saved pages load display assets, so keep an Internet connection. GitHub Actions automatically discovers the notebooks, refreshes saved outputs and publishes the editable collection on every push to `master`. See [scripts/README.md](scripts/README.md) to update or preview the exports locally.

[molab-badge]: https://img.shields.io/badge/molab-334155?style=flat-square
[marimo-badge]: https://img.shields.io/badge/marimo-235b43?style=flat-square

Or run them locally:

```bash
uvx marimo edit --sandbox docs/detect_peaks.py
```

## Other similar modules

 - [Overview of algorithms for peak detection in Python](https://github.com/MonsieurV/py-findpeaks)

## How to cite this work

Here is a suggestion to cite this software, with its concept DOI, which always resolves to the latest version (to cite a specific version, use its DOI listed on [Zenodo](https://doi.org/10.5281/zenodo.4598961)):

> Marcos Duarte. (2021). detecta: A Python module to detect events in data. Zenodo. https://doi.org/10.5281/zenodo.4598961

And a possible BibTeX entry:

```tex
@software{duarte_detecta,
  author       = {Marcos Duarte},
  title        = {{detecta: A Python module to detect events in data}},
  year         = 2021,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.4598961},
  url          = {https://doi.org/10.5281/zenodo.4598961}
}
```

## License

The non-software content of this project is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/), and the software code is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
