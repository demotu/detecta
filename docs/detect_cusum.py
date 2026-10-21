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
    s[t] = x[t] - \hat{\mu}[t-1] \\
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

    where $\hat{\mu}[t-1]$ is a reference level for the data, an estimate of the data mean before the change. Implementations of the CUSUM algorithm differ in this reference level, and `detect_cusum` offers the following ones (parameter `reference`):

    | `reference` | $\hat{\mu}[t-1]$ | Known as |
    |---|---|---|
    | `'previous'` (default) | the previous sample, $x[t-1]$ | detecta 0.0.5 |
    | `'residual'` | exponentially weighted mean of the data (smoothing factor `alpha`) | Gustafsson (2000) |
    | `'run_mean'` | mean of all the data so far | Page-Hinkley test (Hinkley 1971) |
    | `'mean'` | mean of the first `n_baseline` samples | classical CUSUM (Page 1954) |
    | a number | a known reference level, $\mu_0$ | classical CUSUM (Page 1954) |

    With the previous sample as reference, $s[t]$ is the difference between consecutive samples and the cumulative sum is simply the difference between the current sample and the sample where the sum restarted. This form detects abrupt jumps in the data, but the evidence for a change does not accumulate over time. With the other references, the deviations from the level before the change accumulate, and a small but sustained change can be detected. After a change is detected, the estimated references (`'residual'`, `'run_mean'`, and `'mean'`) restart from the data after the alarm.

    There are other implementations of the CUSUM algorithm; for example, the sum term ($s[t]$ above) can be normalized by the data variance, or it can be squared for detecting both variance and parameter changes, etc.

    For the CUSUM algorithm to work properly, it depends on tuning the parameters $threshold$ and $drift$ to what is meant by a change in the data. According to Gustafsson (2000), this tuning can be performed following these steps:

     - Start with a very large $threshold$.
     - Choose $drift$ to one half of the expected change, or adjust $drift$ such that $g$ = 0 more than 50% of the time.
     - Then set the $threshold$ so the required number of false alarms (this can be done automatically) or delay for detection is obtained.
     - If faster detection is sought, try to decrease $drift$.
     - If fewer false alarms are wanted, try to increase $drift$.
     - If there is a subset of the change times that does not make sense, try to increase $drift$.

    The function `detect_cusum.py` ([source code](https://github.com/demotu/detecta/blob/master/detecta/detect_cusum.py)) implements the CUSUM algorithm and a procedure to calculate the ending of the detected change. The function signature is:
    ```python
    ta, tai, taf, amp = detect_cusum(x, threshold=1, drift=0, ending=False, show=True, ax=None,
                                     reference='previous', alpha=0.05, n_baseline=None)
    ```
    The ending of each change (`taf`, when `ending=True`) is estimated by running the CUSUM algorithm backwards in time, from the beginning of the next change to the ending of the previous one, and the amplitude of the change (`amp`) is the difference between the mean of the data after and before the change.
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
    ## Reference level

    Let's compare the references on data with a small but sustained change: noise with standard deviation of 1 and a change of 1.5 in the mean between samples 200 and 400. Following Gustafsson's tuning steps, `drift` is one half of the expected change (0.75), and `threshold` is large enough to avoid false alarms (8):
    """)
    return


@app.cell
def _(np):
    _rng = np.random.default_rng(42)
    x_shift = _rng.normal(0, 1, 600)
    x_shift[200:400] += 1.5
    return (x_shift,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `reference='previous'` (the default): the cumulative sum of the differences between consecutive samples is just the difference between the current sample and the sample where the sum restarted, which never exceeds the threshold here; the change is not detected:
    """)
    return


@app.cell
def _(detect_cusum, x_shift):
    detect_cusum(x_shift, 8, .75, True, True, reference='previous')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `reference='mean'` (classical CUSUM): the reference is the mean of the first `n_baseline` samples (by default, 10% of the data), and it is estimated again after each alarm. Both changes are detected, with their beginning, ending, and amplitude (the reference level is shown in orange):
    """)
    return


@app.cell
def _(detect_cusum, x_shift):
    detect_cusum(x_shift, 8, .75, True, True, reference='mean')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `reference='run_mean'` (as in the Page-Hinkley test): the reference is the mean of all the data since the last alarm, which does not require a baseline:
    """)
    return


@app.cell
def _(detect_cusum, x_shift):
    detect_cusum(x_shift, 8, .75, True, True, reference='run_mean')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `reference='residual'` (Gustafsson, 2000): the reference is an exponentially weighted mean of the data, which follows slow variations in the data level. The smoothing factor `alpha` sets how fast the reference follows the data (it averages about the last 1/`alpha` samples):
    """)
    return


@app.cell
def _(detect_cusum, x_shift):
    detect_cusum(x_shift, 8, .75, True, True, reference='residual', alpha=.01)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the reference follows the data too fast (larger `alpha`), the deviation from the reference vanishes before the evidence for the change accumulates, and the first change is not detected:
    """)
    return


@app.cell
def _(detect_cusum, x_shift):
    detect_cusum(x_shift, 8, .75, True, True, reference='residual', alpha=.05)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A number as `reference` is a known level ($\mu_0$) that is kept fixed, as in quality control, where the process is corrected after each alarm. Here, the data are not corrected after the change, and the alarms repeat while the data stay away from the reference:
    """)
    return


@app.cell
def _(detect_cusum, x_shift):
    detect_cusum(x_shift, 8, .75, False, True, reference=0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Ending of the change

    Data with steps and a ramp (between samples 300 and 320) of 4 in noise with standard deviation of 1. The beginning and ending of a step are found within one sample; the beginning and ending of the ramp are found where its deviation exceeds the `drift`, a few samples inside the ramp:
    """)
    return


@app.cell
def _(detect_cusum, np):
    _rng = np.random.default_rng(3)
    _x = _rng.normal(0, 1, 600)
    _x[150:] += 4
    _x[300:320] -= np.linspace(4/20, 4, 20)
    _x[320:] -= 4
    _x[450:] += 4
    _ta, _tai, _taf, _amp = detect_cusum(_x, 6, 2, True, True, reference='mean')
    print('Beginning:', _tai, '\nEnding:   ', _taf, '\nAmplitude:', _amp.round(2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive example

    Choose the data and the reference, tune `threshold` and `drift` following the steps above, and see the detected changes:
    """)
    return


@app.cell
def _(mo):
    signal = mo.ui.dropdown(['large step', 'small shift', 'steps and ramp'],
                            value='large step', label='data')
    reference = mo.ui.dropdown(['previous', 'mean', 'run_mean', 'residual'],
                               value='previous', label='reference')
    threshold = mo.ui.slider(0.5, 15, step=0.5, value=3, label='threshold', show_value=True)
    drift = mo.ui.slider(0, 3, step=0.05, value=1.5, label='drift', show_value=True)
    alpha = mo.ui.slider(0.005, 1, step=0.005, value=0.05, label='alpha', show_value=True)
    n_baseline = mo.ui.slider(5, 200, value=30, label='n_baseline', show_value=True)
    ending = mo.ui.checkbox(value=True, label='ending')
    mo.hstack([mo.vstack([signal, reference, ending]),
               mo.vstack([threshold, drift]),
               mo.vstack([alpha, n_baseline])], justify='start', gap=4)
    return alpha, drift, ending, n_baseline, reference, signal, threshold


@app.cell
def _(
    alpha,
    detect_cusum,
    drift,
    ending,
    n_baseline,
    np,
    reference,
    signal,
    threshold,
):
    _rng = np.random.default_rng(42)
    if signal.value == 'large step':
        _x = _rng.normal(0, 1, 300)
        _x[100:200] += 6
    elif signal.value == 'small shift':
        _x = _rng.normal(0, 1, 600)
        _x[200:400] += 1.5
    else:
        _x = _rng.normal(0, 1, 600)
        _x[150:] += 4
        _x[300:320] -= np.linspace(4/20, 4, 20)
        _x[320:] -= 4
        _x[450:] += 4
    detect_cusum(_x, threshold.value, drift.value, ending.value, True,
                 reference=reference.value, alpha=alpha.value,
                 n_baseline=n_baseline.value)
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
    - David V. Hinkley (1971) [Inference about the change-point from cumulative sum tests](https://doi.org/10.1093/biomet/58.3.509). Biometrika, 58, 509-523.
    - E. S. Page (1954) [Continuous inspection schemes](https://doi.org/10.1093/biomet/41.1-2.100). Biometrika, 41, 100-115.
    """)
    return


if __name__ == "__main__":
    app.run()
