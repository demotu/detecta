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

The examples are [marimo](https://marimo.io) notebooks in the [docs](https://github.com/demotu/detecta/tree/master/docs) directory. Run them in your browser, no installation needed:

| Notebook | molab | marimo.app |
|---|---|---|
| [detect_peaks](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_peaks.py) | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_peaks.py/wasm) | [![Open with marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_peaks.py) |
| [detect_onset](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_onset.py) | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_onset.py/wasm) | [![Open with marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_onset.py) |
| [detect_cusum](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_cusum.py) | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_cusum.py/wasm) | [![Open with marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_cusum.py) |
| [detect_seq](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_seq.py) | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/demotu/detecta/blob/master/docs/detect_seq.py/wasm) | [![Open with marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/demotu/detecta/blob/master/docs/detect_seq.py) |

The notebook name links to a static preview with the outputs; the badges run the notebook in your browser with [WebAssembly](https://docs.marimo.io/guides/wasm/).

Or run them locally:

```bash
uvx marimo edit --sandbox docs/detect_peaks.py
```

## Other similar modules

 - [Overview of algorithms for peak detection in Python](https://github.com/MonsieurV/py-findpeaks)

## How to cite this work

Here is a suggestion to cite this GitHub repository:

> Marcos Duarte. (2021). detecta: A Python module to detect events in data (Version v0.0.5). Zenodo. http://doi.org/10.5281/zenodo.4598962

And a possible BibTeX entry:

```tex
@software{marcos_duarte_2021_4598962,
  author       = {Marcos Duarte},
  title        = {detecta: A Python module to detect events in data},
  month        = mar,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {v0.0.5},
  doi          = {10.5281/zenodo.4598962},
  url          = {https://doi.org/10.5281/zenodo.4598962}
}
```

## License

The non-software content of this project is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/), and the software code is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
