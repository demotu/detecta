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

Or

```bash
conda install -c duartexyz detecta
```

## Examples

- [detect_peaks](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_peaks.ipynb)  
- [detect_onset](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_onset.ipynb)  
- [detect_cusum](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_cusum.ipynb)  
- [detect_seq](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_seq.ipynb)  

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
