# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "detecta",
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "pyversions",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # detect_onset.py

    A function from [detecta](https://pypi.org/project/detecta/) - Python module to detect events in data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One of the simplest methods to automatically detect or identify the change or occurrence of a particular event in the data, for example, its beginning and ending, or simply the data onset, is based on amplitude threshold, where the signal is considered to be 'on' when it is above a certain threshold. This threshold can be proportional to the amplitude of the baseline (the part of the data that we know there is no real signal, only noise).

    For instance, a threshold equals to two or three times the standard deviation of the baseline is a common procedure employed in the analysis of electromyographic data. Other way to set the threshold would be as a percentage value of the maximum or peak of the data. For instance, in movement analysis it's common to define the onset period as the signal above 5% of the peak velocity of the investigated movement.

    The function `detect_onset.py` ([source code](https://github.com/demotu/detecta/blob/master/detecta/detect_onset.py)) implements such onset detection based on the amplitude-threshold method with a parameter to specify a minimum number of samples above threshold to detect as onset, other parameter to specify the minimum number of samples (continuous or not) below threshold that will be ignored in the detection of data greater or equal to threshold (to avoid the detection of spikes or transients in the data), and a second threshold parameter to specify the minimum amplitude that a minimum number of samples should have (to avoid the detection of baseline fluctuations that are above the first threshold but are not actual signals).

    `detect_onset.py` signature is:
    ```python
    inds = detect_onset(x, threshold=0, n_above=1, n_below=0,
                        threshold2=None, n_above2=1, show=False, ax=None)
    ```
    Let's see how `detect_onset.py` works; first let's import the necessary Python libraries and configure the environment.
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
    uvx marimo edit --sandbox detect_onset.py
    ```
    """)
    return


@app.cell
def _():
    import timeit

    import marimo as mo
    import numpy as np
    import pyversions

    from detecta import detect_onset

    return detect_onset, mo, np, pyversions, timeit


@app.cell
def _(pyversions):
    _info = pyversions.versions()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Examples

    Let's run the function examples:
    """)
    return


@app.cell
def _(detect_onset, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(200)/10
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    detect_onset(_x, np.std(_x[:50]), n_above=10, n_below=0, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Add some noise:
    """)
    return


@app.cell
def _(detect_onset, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(200)/10
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    _x[80:140:20] = 0
    detect_onset(_x, np.std(_x[:50]), n_above=10, n_below=0, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will use the `n_below` parameter to not detect the noise from former example as onsets:
    """)
    return


@app.cell
def _(detect_onset, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(200)/10
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    _x[80:140:20] = 0
    detect_onset(_x, np.std(_x[:50]), n_above=10, n_below=2, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `detect_onset` works with missing values (NaNs):
    """)
    return


@app.cell
def _(detect_onset, np):
    _x = [0, 0, 2, 0, np.nan, 0, 2, 3, 3, 0, 1, 1, 0]
    detect_onset(_x, threshold=1, n_above=1, n_below=0, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider the case where there is a false onset because some data in the baseline are greater than the `threshold`:
    """)
    return


@app.cell
def _(detect_onset, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(200)/10
    _x[11:41] = np.ones(30)*.3
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    _x[80:140:20] = 0
    detect_onset(_x, .1, n_above=10, n_below=1, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can't increase the value of the `threshold` because this would delay the detection of the actual onset:
    """)
    return


@app.cell
def _(detect_onset, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(200)/10
    _x[11:41] = np.ones(30)*.3
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    _x[80:140:20] = 0
    detect_onset(_x, .4, n_above=10, n_below=1, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this situation we can use the second threshold parameter, `threshold2` with corresponding `n_above2` parameter:
    """)
    return


@app.cell
def _(detect_onset, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(200)/10
    _x[11:41] = np.ones(30)*.3
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    _x[80:140:20] = 0
    detect_onset(_x, .1, n_above=10, n_below=1,
                 threshold2=.4, n_above2=5, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive example

    Change the parameters and see the detected onsets in the data of the former example:
    """)
    return


@app.cell
def _(mo):
    threshold = mo.ui.slider(0, 1, step=0.05, value=0.1, label='threshold', show_value=True)
    n_above = mo.ui.slider(1, 50, value=10, label='n_above', show_value=True)
    n_below = mo.ui.slider(0, 10, value=1, label='n_below', show_value=True)
    use_threshold2 = mo.ui.checkbox(value=True, label='use threshold2')
    threshold2 = mo.ui.slider(0, 1, step=0.05, value=0.4, label='threshold2', show_value=True)
    n_above2 = mo.ui.slider(1, 50, value=5, label='n_above2', show_value=True)
    mo.hstack([mo.vstack([threshold, n_above, n_below]),
               mo.vstack([use_threshold2, threshold2, n_above2])], justify='start', gap=4)
    return n_above, n_above2, n_below, threshold, threshold2, use_threshold2


@app.cell
def _(
    detect_onset,
    n_above,
    n_above2,
    n_below,
    np,
    threshold,
    threshold2,
    use_threshold2,
):
    _rng = np.random.default_rng(42)
    _x = _rng.normal(0, .1, 200)
    _x[11:41] = np.ones(30)*.3
    _x[51:151] += np.hstack((np.linspace(0, 1, 50), np.linspace(1, 0, 50)))
    _x[80:140:20] = 0
    detect_onset(_x, threshold.value, n_above=n_above.value, n_below=n_below.value,
                 threshold2=threshold2.value if use_threshold2.value else None,
                 n_above2=n_above2.value, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function performance

    The performance of the `detect_onset` function varies with the data and parameters.
    Here is a simple test of the `detect_onset.py` performance:
    """)
    return


@app.cell
def _(detect_onset, np, timeit):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(10000)
    print('Detection of onset (data size= %d):' % _x.size)
    _number = 100
    _t = min(timeit.repeat(lambda: detect_onset(_x, threshold=0, n_above=10, n_below=1,
                                                threshold2=.5, n_above2=5, show=False),
                           number=_number, repeat=5)) / _number
    print('%.3f ms per loop' % (1e3*_t))
    return


if __name__ == "__main__":
    app.run()
