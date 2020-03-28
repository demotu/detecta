# detecta

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
 * [detect_peaks](./docs/detect_peaks.ipynb)  
 * [detect_onset](./docs/detect_onset.ipynb)  
 * [detect_cusum](./docs/detect_cusum.ipynb)  
 * [detect_seq](./docs/detect_seq.ipynb)  
