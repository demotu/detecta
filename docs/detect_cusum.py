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
    # detect_cusum.py

    A function from [detecta](https://pypi.org/project/detecta/) - Python module to detect events in data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Change detection](http://en.wikipedia.org/wiki/Change_detection) refers to procedures to identify abrupt changes in a phenomenon (Basseville and Nikiforov 1993, Gustafsson 2000). By abrupt change it is meant any difference in relation to previous known data faster than expected of some characteristic of the data such as amplitude, mean, variance, frequency, etc.

    The [Cumulative sum (CUSUM)](http://en.wikipedia.org/wiki/CUSUM) algorithm is a classical technique for monitoring change detection. One form of implementing the CUSUM algorithm involves the calculation of the cumulative sum of positive and negative changes ($g_t^+$ and $g_t^-$) in the data ($x$) and comparison to a $threshold$. When this threshold is exceeded a change is detected ($t_{talarm}$) and the cumulative sum restarts from zero. To avoid the detection of a change in absence of an actual change or a slow drift, this algorithm also depends on a parameter $drift$ for drift correction. This form of the CUSUM algorithm is given by:

    $$ \begin{array}{l l}
    \left\{ \begin{array}{l l}
    s[t] = x[t] - x[t-1] \\
    g^+[t] = max\left(g^+[t-1] + s[t]-drift,\; 0\right) \\
    g^-[t] = max\left(g^-[t-1] - s[t]-drift,\; 0\right)
    \end{array} \right. \\
    \\
    \; if \;\;\; g^+[t] > threshold \;\;\; or \;\;\;  g^-[t] > threshold: \\
    \\
    \left\{ \begin{array}{l l}
    t_{talarm}=t \\
    g^+[t] = 0 \\
    g^-[t] = 0
    \end{array} \right.
    \end{array} $$

    There are different implementations of the CUSUM algorithm; for example, the term for the sum of the last elements ($s[t]$ above) can have a longer history (with filtering), it can be normalized by removing the data mean and then divided by the data variance), or this sum term can be squared for detecting both variance and parameter changes, etc.

    For the CUSUM algorithm to work properly, it depends on tuning the parameters $threshold$ and $drift$ to what is meant by a change in the data. According to Gustafsson (2000), this tuning can be performed following these steps:

     - Start with a very large $threshold$.
     - Choose $drift$ to one half of the expected change, or adjust $drift$ such that $g$ = 0 more than 50% of the time.
     - Then set the $threshold$ so the required number of false alarms (this can be done automatically) or delay for detection is obtained.
     - If faster detection is sought, try to decrease $drift$.
     - If fewer false alarms are wanted, try to increase $drift$.
     - If there is a subset of the change times that does not make sense, try to increase $drift$.

    The function `detect_cusum.py` ([source code](https://github.com/demotu/detecta/blob/master/detecta/detect_cusum.py)) implements the CUSUM algorithm and a procedure to calculate the ending of the detected change. The function signature is:
    ```python
    ta, tai, taf, amp = detect_cusum(x, threshold=1, drift=0, ending=False, show=True, ax=None)
    ```
    Let's see how to use `detect_cusum.py`; first let's import the necessary Python libraries and configure the environment.
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
    uvx marimo edit --sandbox detect_cusum.py
    ```
    """)
    return


@app.cell
def _():
    import timeit

    import marimo as mo
    import numpy as np

    from detecta import detect_cusum

    return detect_cusum, mo, np, timeit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Examples

    A ramp change:
    """)
    return


@app.cell
def _(detect_cusum, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(300)/5
    _x[100:200] += np.arange(0, 4, 4/100)
    _ta, _tai, _taf, _amp = detect_cusum(_x, 2, .02, True, True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A step change:
    """)
    return


@app.cell
def _(detect_cusum, np):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(300)
    _x[100:200] += 6
    detect_cusum(_x, 4, 1.5, True, True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A sinusoid:
    """)
    return


@app.cell
def _(detect_cusum, np):
    _x = 2*np.sin(2*np.pi*np.arange(0, 3, .01))
    _ta, _tai, _taf, _amp = detect_cusum(_x, 1, .05, True, True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive example

    Tune `threshold` and `drift` following the steps above and see the detected changes:
    """)
    return


@app.cell
def _(mo):
    threshold = mo.ui.slider(0.5, 10, step=0.5, value=3, label='threshold', show_value=True)
    drift = mo.ui.slider(0, 3, step=0.1, value=1.5, label='drift', show_value=True)
    ending = mo.ui.checkbox(value=True, label='ending')
    mo.hstack([threshold, drift, ending], justify='start', gap=4)
    return drift, ending, threshold


@app.cell
def _(detect_cusum, drift, ending, np, threshold):
    _rng = np.random.default_rng(42)
    _x = _rng.normal(0, 1, 300)
    _x[100:200] += 6
    detect_cusum(_x, threshold.value, drift.value, ending.value, True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function performance

    Here is a poor test of the `detect_cusum.py` performance:
    """)
    return


@app.cell
def _(detect_cusum, np, timeit):
    _rng = np.random.default_rng(42)
    _x = _rng.standard_normal(10000)
    _x[400:600] += 6
    print('Detection of onset (data size = %d):' % _x.size)
    _number = 10
    _t = min(timeit.repeat(lambda: detect_cusum(_x, 4, 1.5, True, False),
                           number=_number, repeat=5)) / _number
    print('%.3f ms per loop' % (1e3*_t))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Michèle Basseville and Igor V. Nikiforov (1993). [Detection of Abrupt Changes: Theory and Application](http://books.google.com.br/books/about/Detection_of_abrupt_changes.html?id=Vu5SAAAAMAAJ). Prentice-Hall.
    - Fredrik Gustafsson (2000) [Adaptive Filtering and Change Detection](http://books.google.com.br/books?id=cyNTAAAAMAAJ). Wiley.
    """)
    return


if __name__ == "__main__":
    app.run()
