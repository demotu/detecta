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
    # detect_seq.py

    A function from [detecta](https://pypi.org/project/detecta/) - Python module to detect events in data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The function `detect_seq.py` ([source code](https://github.com/demotu/detecta/blob/master/detecta/detect_seq.py)) detects initial and final indices of sequential data identical to parameter `value` in `x`.
    Use parameter `min_seq` to set the minimum number of sequential values to detect.

    The signature of `detect_seq.py` is:
    ```python
    idx = detect_seq(x, value=np.nan, index=False, min_seq=1, max_alert=0, show=False, ax=None)
    ```
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
    uvx marimo edit --sandbox detect_seq.py
    ```
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pyversions

    from detecta import detect_seq

    return detect_seq, mo, np, pyversions


@app.cell
def _(pyversions):
    _info = pyversions.versions()
    return


@app.cell
def _(detect_seq, mo):
    mo.doc(detect_seq)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Examples
    """)
    return


@app.cell
def _():
    x = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0]
    return (x,)


@app.cell
def _(detect_seq, x):
    detect_seq(x, 0)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 0, index=True)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 0, index=True, min_seq=2)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 10)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 10, index=True)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 1, index=True, min_seq=2, show=True)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 1, index=False, min_seq=1, show=True)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 0, index=True, min_seq=2, show=True)
    return


@app.cell
def _(detect_seq, x):
    detect_seq(x, 0, index=True, max_alert=2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Detect sequences of missing values (NaN's):
    """)
    return


@app.cell
def _(detect_seq, np):
    _x = [1, 2, np.nan, np.nan, 5, 4, 5, np.nan, 2, 1, 2]
    detect_seq(_x, np.nan, index=True, max_alert=2, show=True)
    return


if __name__ == "__main__":
    app.run()
