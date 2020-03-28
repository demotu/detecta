# [detecta](https://pypi.org/project/detecta/)

Python module to detect events in data

The following functions are implemented in detecta:  
 - **detect_peaks.py**: detects peaks in data based on their amplitude and other features.  
 - **detect_onset.py**: detects onset in data based on amplitude threshold.  
 - **detect_cusum.py**: detects abrupt changes in data using cumulative sum algorithm (CUSUM).  
 - **detect_seq.py**: detects initial and final indices of sequential data identical to a parameter.

Installation
------------
```
pip install detecta
```

Examples
--------
 * [detect_peaks](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_peaks.ipynb)  
 * [detect_onset](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_onset.ipynb)  
 * [detect_cusum](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_cusum.ipynb)  
 * [detect_seq](https://nbviewer.jupyter.org/github/demotu/detecta/blob/master/docs/detect_seq.ipynb)  
