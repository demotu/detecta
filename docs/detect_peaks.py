# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "detecta",
#     "marimo",
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # detect_peaks.py

    A function from [detecta](https://pypi.org/project/detecta/) - Python module to detect events in data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One way to detect peaks (local maxima) or valleys (local minima) in data is to use the property that a peak (or valley) must be greater (or smaller) than its immediate neighbors. The function `detect_peaks.py` ([source code](https://github.com/demotu/detecta/blob/master/detecta/detect_peaks.py)) detects peaks (or valleys) based on this feature and other characteristics. The function signature is:
    ```python
    ind = detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising', kpsh=False, valley=False, show=False, ax=None, title=True)
    ```
    The parameters `mph`, `mpd`, and `threshold` follow the convention of the Matlab function `findpeaks.m`.
    Let's see how to use `detect_peaks.py`; first let's import the necessary Python libraries and configure the environment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Installation

    ```bash
    pip install "detecta[plot]"
    ```

    Or

    ```bash
    conda install -c duartexyz detecta
    ```

    To run this [marimo](https://marimo.io) notebook in an isolated environment with all its dependencies:

    ```bash
    uvx marimo edit --sandbox detect_peaks.py
    ```
    """)
    return


@app.cell
def _():
    import timeit

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    from detecta import detect_peaks

    return detect_peaks, mo, np, plt, timeit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Examples

    Detect all peaks in data with missing values (NaN's):
    """)
    return


@app.cell
def _(detect_peaks, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(100)
    _x[60:81] = np.nan
    detect_peaks(_x, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Set minimum peak height = 0 and minimum peak distance = 20:
    """)
    return


@app.cell
def _(detect_peaks, np):
    _rng = np.random.default_rng(42)
    _x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + _rng.standard_normal(200)/5
    detect_peaks(_x, mph=0, mpd=20, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Set minimum peak distance = 2:
    """)
    return


@app.cell
def _(detect_peaks):
    _x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    detect_peaks(_x, mpd=2, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Detection of valleys instead of peaks:
    """)
    return


@app.cell
def _(detect_peaks, np):
    _rng = np.random.default_rng(42)
    _x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + _rng.standard_normal(200)/5
    detect_peaks(_x, mph=-1.2, mpd=20, valley=True, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Detect both edges of flat peaks:
    """)
    return


@app.cell
def _(detect_peaks):
    _x = [0, 1, 1, 0, 1, 1, 0]
    detect_peaks(_x, edge='both', show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Set threshold = 2:
    """)
    return


@app.cell
def _(detect_peaks):
    _x = [-2, 1, -2, 2, 1, 1, 3, 0]
    detect_peaks(_x, threshold=2, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plot in existing axes, without the standard title:
    """)
    return


@app.cell
def _(detect_peaks, plt):
    _x = [-2, 1, -2, 2, 1, 1, 3, 0]
    _fig, _axs = plt.subplots(ncols=2, nrows=1, figsize=(10, 4))
    detect_peaks(_x, show=True, ax=_axs[0], threshold=0.5, title=False)
    detect_peaks(_x, show=True, ax=_axs[1], threshold=1.5, title=False)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive example

    Change the parameters and see the detected peaks:
    """)
    return


@app.cell
def _(mo):
    use_mph = mo.ui.checkbox(value=True, label='use mph')
    mph = mo.ui.slider(-1.5, 1.5, step=0.1, value=0, label='mph', show_value=True)
    mpd = mo.ui.slider(1, 50, value=20, label='mpd', show_value=True)
    threshold = mo.ui.slider(0, 1, step=0.05, value=0, label='threshold', show_value=True)
    edge = mo.ui.dropdown(['rising', 'falling', 'both'], value='rising', label='edge')
    kpsh = mo.ui.checkbox(label='kpsh')
    valley = mo.ui.checkbox(label='valley')
    mo.hstack([mo.vstack([use_mph, mph, mpd, threshold]),
               mo.vstack([edge, kpsh, valley])], justify='start', gap=4)
    return edge, kpsh, mpd, mph, threshold, use_mph, valley


@app.cell
def _(detect_peaks, edge, kpsh, mpd, mph, np, threshold, use_mph, valley):
    _rng = np.random.default_rng(42)
    _x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + _rng.normal(0, .2, 200)
    detect_peaks(_x, mph=mph.value if use_mph.value else None, mpd=mpd.value,
                 threshold=threshold.value, edge=edge.value, kpsh=kpsh.value,
                 valley=valley.value, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function performance

    The function `detect_peaks.py` is relatively fast but the parameter minimum peak distance (mpd) slows down the function if the data has several peaks (>1000). Try to decrease the number of peaks by tuning the other parameters or smooth the data before calling this function with several peaks in the data.
    Here is a simple test of its performance:
    """)
    return


@app.cell
def _(detect_peaks, np, timeit):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(10000)
    _ind = detect_peaks(_x)
    print('Data with %d points and %d peaks\n' % (_x.size, _ind.size))

    def _bench(stmt, number=100):
        t = min(timeit.repeat(stmt, number=number, repeat=5)) / number
        print('%.3f ms per loop' % (1e3*t))

    print('Performance (without the minimum peak distance parameter):')
    print('detect_peaks(x)')
    _bench(lambda: detect_peaks(_x))
    print('\nPerformance (using the minimum peak distance parameter):')
    print('detect_peaks(x, mpd=10)')
    _bench(lambda: detect_peaks(_x, mpd=10), number=10)
    return


if __name__ == "__main__":
    app.run()
