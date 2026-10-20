import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from detecta import detect_cusum, detect_onset, detect_peaks, detect_seq


def test_peaks_mpd():
    x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    assert detect_peaks(x, mpd=2).tolist() == [1, 5, 9]


def test_peaks_edge_both():
    assert detect_peaks([0, 1, 1, 0, 1, 1, 0], edge='both').tolist() == [1, 2, 4, 5]


def test_peaks_threshold():
    assert detect_peaks([-2, 1, -2, 2, 1, 1, 3, 0], threshold=2).tolist() == [1, 6]


def test_peaks_valley():
    assert detect_peaks([0, -1, 0, -2, 0], valley=True).tolist() == [1, 3]


def test_peaks_nan():
    x = [0, 1, 0, 2, np.nan, 2, 0, 3, 0]
    # values next to NaN's cannot be peaks
    assert detect_peaks(x).tolist() == [1, 7]


def test_peaks_short_input():
    assert detect_peaks([1, 2]).size == 0


def test_onset():
    x = [0, 0, 2, 0, np.nan, 0, 2, 3, 3, 0, 1, 1, 0]
    inds = detect_onset(x, threshold=1, n_above=1, n_below=0)
    assert inds.tolist() == [[2, 2], [6, 8], [10, 11]]


def test_onset_n_above_n_below():
    x = [0, 0, 2, 0, np.nan, 0, 2, 3, 3, 0, 1, 1, 0]
    assert detect_onset(x, threshold=1, n_above=2, n_below=1).tolist() == [[6, 11]]


def test_onset_none():
    assert detect_onset([0, 0, 0], threshold=1).size == 0


def test_cusum():
    x = np.zeros(100)
    x[50:] = 5
    ta, tai, taf, amp = detect_cusum(x, threshold=2, drift=.1, ending=True,
                                     show=False)
    assert ta.tolist() == [50]
    assert tai.tolist() == [49]
    assert taf.tolist() == [50]
    assert amp.tolist() == [5]


def test_seq():
    x = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0]
    assert detect_seq(x, 0).tolist() == [False, True, True, True, False, False,
                                         False, True, False, True, True, True]
    assert detect_seq(x, 0, index=True).tolist() == [[1, 3], [7, 7], [9, 11]]
    assert detect_seq(x, 0, index=True, min_seq=2).tolist() == [[1, 3], [9, 11]]
    assert detect_seq(x, 10, index=True).size == 0


def test_seq_nan():
    assert detect_seq([1, np.nan, np.nan, 2], index=True).tolist() == [[1, 2]]


def test_seq_max_alert(capsys):
    detect_seq([1, 0, 0, 1, 0, 0, 0], 0, max_alert=2)
    out = capsys.readouterr().out.splitlines()
    assert out == ['Sequential data equal or longer than 2: (2, [1 2])',
                   'Sequential data equal or longer than 2: (3, [4 6])']


@pytest.mark.parametrize("func, args", [
    (detect_peaks, ([0, 1, 0, 2, np.nan, 2, 0, 3, 0],)),
    (detect_onset, ([0, 0, 2, 0, 0, 2, 3, 3, 0], 1)),
    (detect_cusum, (np.r_[np.zeros(50), np.ones(50) * 5], 2, 0, True)),
    (detect_seq, ([1, 0, 0, 1, 0], 0)),
])
def test_plots(func, args):
    func(*args, show=True)
    matplotlib.pyplot.close('all')


def test_cusum_external_axes():
    import matplotlib.pyplot as plt
    _, ax = plt.subplots(2, 1)
    detect_cusum(np.r_[np.zeros(50), np.ones(50) * 5], 2, 0, True, show=True, ax=ax)
    plt.close('all')
