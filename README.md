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

How to cite this work
---------------------
Here is a suggestion to cite this GitHub repository:

> Duarte, M. (2020) detecta: A Python module to detect events in data. GitHub repository, https://github.com/demotu/detecta.

And a possible BibTeX entry:

```tex
@misc{Duarte2020,  
    author = {Duarte, M.},
    title = {detecta: A Python module to detect events in data},  
    year = {2020},  
    publisher = {GitHub},  
    journal = {GitHub repository},  
    howpublished = {\url{https://github.com/demotu/detecta}}  
}
```

License
-------
The non-software content of this project is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/), and the software code is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
