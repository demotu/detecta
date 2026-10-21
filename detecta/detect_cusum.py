"""Cumulative sum algorithm (CUSUM) to detect abrupt changes in data."""

import numbers

import numpy as np

__author__ = 'Marcos Duarte, https://github.com/demotu'
__version__ = "1.1.0"
__license__ = "MIT"

REFERENCES = ('previous', 'residual', 'run_mean', 'mean')


def detect_cusum(x, threshold=1, drift=0, ending=False, show=True, ax=None,
                 reference='previous', alpha=0.05, n_baseline=None):
    """Cumulative sum algorithm (CUSUM) to detect abrupt changes in data.

    Parameters
    ----------
    x : 1D array_like
        data.
    threshold : positive number, optional (default = 1)
        amplitude threshold for the change in the data.
    drift : positive number, optional (default = 0)
        drift term that prevents any change in the absence of change.
    ending : bool, optional (default = False)
        True (1) to estimate when the change ends; False (0) otherwise.
    show : bool, optional (default = True)
        True (1) plots data in matplotlib figure, False (0) don't plot.
    ax : a matplotlib.axes.Axes instance, optional (default = None).
    reference : {'previous', 'residual', 'run_mean', 'mean'} or number,
        optional (default = 'previous')
        reference level from which the deviations of the data are summed,
        s[t] = x[t] - reference[t-1]:
        'previous': the previous sample (version 1.0.5 of this function).
        'residual': exponentially weighted mean of the data with smoothing
        factor `alpha` (Gustafsson, 2000); it is the running mean while there
        are less than 1/`alpha` samples.
        'run_mean': mean of all the data so far (as in the Page-Hinkley test).
        'mean': mean of the first `n_baseline` samples (Page, 1954).
        number: a known reference level, kept fixed.
        After a change is detected, the estimated references ('residual',
        'run_mean', and 'mean') restart from the data after the alarm.
    alpha : number in (0, 1], optional (default = 0.05)
        smoothing factor for `reference` = 'residual'. A larger `alpha`
        follows the data faster; `alpha` = 1 is the same as 'previous'.
    n_baseline : positive integer, optional (default = None)
        number of samples used to estimate the reference level for
        `reference` = 'mean'. If None, 10% of the data (at least 5 samples).

    Returns
    -------
    ta : 1D array_like [indi, indf], int
        alarm time (index of when the change was detected).
    tai : 1D array_like, int
        index of when the change started.
    taf : 1D array_like, int
        index of when the change ended (if `ending` is True).
    amp : 1D array_like, float
        amplitude of changes (if `ending` is True).

    Notes
    -----
    Tuning of the CUSUM algorithm according to Gustafsson (2000)[1]_:
    Start with a very large `threshold`.
    Choose `drift` to one half of the expected change, or adjust `drift` such
    that `g` = 0 more than 50% of the time.
    Then set the `threshold` so the required number of false alarms (this can
    be done automatically) or delay for detection is obtained.
    If faster detection is sought, try to decrease `drift`.
    If fewer false alarms are wanted, try to increase `drift`.
    If there is a subset of the change times that does not make sense,
    try to increase `drift`.

    The classical CUSUM (Page, 1954)[2]_ sums the deviations of the data from
    a reference level, the mean of the data before the change. With
    `reference` = 'previous' (the default), the deviations are the
    differences between consecutive samples and their sum is the difference
    between the current sample and the sample where the sum restarted. This
    form detects abrupt jumps in the data, but a small sustained change is
    better detected with one of the other references, because the evidence
    for the change accumulates over many samples.

    Note that with `reference` = 'previous' repeated sequential changes,
    i.e., changes that have the same beginning (`tai`), are not deleted
    because the changes were detected by the alarm (`ta`) at different
    instants.

    If `ending` is True, repeated sequential changes are deleted (only the
    first alarm of the changes with the same beginning is kept) and the
    ending of each change (`taf`) is estimated by running the CUSUM algorithm
    backwards in time, from the beginning of the next change (or from the end
    of the data) to the ending of the previous change (or to the beginning of
    the data). If no change is detected backwards, the ending is the alarm
    time. The amplitude of the change
    (`amp`) is the difference between the mean of the data after the change
    ends and the mean of the data before the change starts.

    See this marimo notebook [4]_.

    References
    ----------
    .. [1] Gustafsson (2000) Adaptive Filtering and Change Detection.
    .. [2] Page (1954) Continuous inspection schemes. Biometrika, 41, 100-115.
    .. [3] Hinkley (1971) Inference about the change-point from
           cumulative sum tests. Biometrika, 58, 509-523.
    .. [4] https://github.com/demotu/detecta/blob/master/docs/detect_cusum.py

    Examples
    --------
    >>> x = np.random.randn(300)/5
    >>> x[100:200] += np.arange(0, 4, 4/100)
    >>> ta, tai, taf, amp = detect_cusum(x, 2, .02, True, True)

    >>> x = np.random.randn(300)
    >>> x[100:200] += 6
    >>> detect_cusum(x, 4, 1.5, True, True)

    >>> x = 2*np.sin(2*np.pi*np.arange(0, 3, .01))
    >>> ta, tai, taf, amp = detect_cusum(x, 1, .05, True, True)

    >>> x = np.random.randn(400)
    >>> x[200:] += 1
    >>> # a small sustained change detected with a reference level
    >>> detect_cusum(x, 8, .5, True, True, reference='mean')

    Version history
    ---------------
    '1.1.0':
        Add parameters `reference`, `alpha`, and `n_baseline`
        Estimate the ending of each change in its own segment of the data
        Amplitude of the change from the mean of the data before and after
    '1.0.5':
        Part of the detecta module - https://pypi.org/project/detecta/
    """

    x = np.atleast_1d(x).astype('float64')
    if isinstance(reference, numbers.Number) and not isinstance(reference, bool):
        reference = float(reference)
    elif reference not in REFERENCES:
        raise ValueError("reference must be one of %s or a number." % (REFERENCES,))
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in the interval (0, 1].")
    if n_baseline is None:
        n_baseline = max(int(round(0.1*x.size)), 5)
    elif n_baseline < 1:
        raise ValueError("n_baseline must be a positive integer.")
    n_baseline = int(n_baseline)

    ta, tai, sign, gp, gn, ref = _cusum(x, threshold, drift, reference, alpha,
                                        n_baseline)
    taf, amp = np.array([], dtype=int), np.array([])
    if tai.size and ending:
        ta, tai, taf, amp = _ending(x, threshold, drift, reference, alpha,
                                    n_baseline, ta, tai, sign)

    if show:
        _plot(x, threshold, drift, ending, ax, ta, tai, taf, gp, gn,
              None if reference == 'previous' else ref)

    return ta, tai, taf, amp


def _cusum(x, threshold, drift, reference, alpha, n_baseline):
    """Two-sided CUSUM of the deviations of `x` from a reference level."""

    def restart(i):
        """Reference level estimated from the data starting at index `i`."""
        if reference == 'mean':
            return np.mean(x[i:i+n_baseline])
        return x[i]

    fixed = not isinstance(reference, str)
    gp, gn, ref = np.zeros(x.size), np.zeros(x.size), np.full(x.size, np.nan)
    ta, tai, sign = [], [], []
    tap, tan = 0, 0
    level = reference if fixed else restart(0) if x.size else np.nan
    count = 1  # number of samples in the reference level since its restart
    ref[:1] = level
    for i in range(1, x.size):
        ref[i] = x[i-1] if reference == 'previous' else level
        s = x[i] - ref[i]
        gp[i] = gp[i-1] + s - drift  # cumulative sum for + change
        gn[i] = gn[i-1] - s - drift  # cumulative sum for - change
        if gp[i] < 0:
            gp[i], tap = 0, i
        if gn[i] < 0:
            gn[i], tan = 0, i
        # update the reference level with the current sample; the weighted
        # mean is a running mean until it has about 1/alpha samples
        count += 1
        if reference == 'residual':
            level = level + max(alpha, 1/count)*(x[i] - level)
        elif reference == 'run_mean':
            level = level + (x[i] - level)/count
        if gp[i] > threshold or gn[i] > threshold:  # change detected!
            up = gp[i] > threshold
            ta.append(i)  # alarm index
            tai.append(tap if up else tan)  # start
            sign.append(1 if up else -1)
            gp[i], gn[i] = 0, 0  # reset alarm
            if reference != 'previous':  # restart the sums from the alarm
                tap, tan = i, i
                if not fixed:
                    level, count = restart(i), 1

    return (np.array(ta, dtype=int), np.array(tai, dtype=int),
            np.array(sign, dtype=int), gp, gn, ref)


def _ending(x, threshold, drift, reference, alpha, n_baseline, ta, tai, sign):
    """Estimate the ending and the amplitude of each change (offline form)."""

    # changes with the same beginning are the same change: keep the first alarm
    tai, ind = np.unique(tai, return_index=True)
    ta, sign = ta[ind], sign[ind]
    # the ending of each change is searched until the next change starts
    ends = np.append(tai[1:], x.size)
    # a fixed reference level is only valid before the change
    backward = 'mean' if not isinstance(reference, str) else reference
    taf = np.zeros(tai.size, dtype=int)
    begins = np.zeros(tai.size, dtype=int)
    for k in range(tai.size):
        # run backwards from the next change to the end of the previous one,
        # so the data before the change provide evidence for it
        begins[k] = taf[k-1] if k else 0
        seg = x[begins[k]:ends[k]][::-1]
        _, tai2, sign2, _, _, _ = _cusum(seg, threshold, drift, backward,
                                         alpha, n_baseline)
        # backwards, the change has the opposite sign and it starts after
        # (forwards) the beginning of the change; keep the closest one
        f = ends[k] - 1 - tai2
        f = f[(sign2 == -sign[k]) & (f >= tai[k])]
        taf[k] = f.min() if f.size else min(ta[k], ends[k] - 1)
    # amplitude: mean of the data after the change minus mean before it
    amp = np.array([x[taf[k]:ends[k]].mean() - x[begins[k]:tai[k]+1].mean()
                    for k in range(tai.size)])

    return ta, tai, taf, amp


def _plot(x, threshold, drift, ending, ax, ta, tai, taf, gp, gn, ref):
    """Plot results of the detect_cusum function, see its help."""

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
        return

    if ax is None:
        _, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    else:
        if len(ax) != 2:
            print("Plotting failed. Expecting instances of 2 matplotlib axes.")
            return
        (ax1, ax2) = ax

    t = range(x.size)
    ax1.plot(t, x, 'b-', lw=2)
    if ref is not None:
        ax1.plot(t, ref, color='orange', lw=1.5, label='Reference')
    if len(ta):
        ax1.plot(tai, x[tai], '>', mfc='g', mec='g', ms=10,
                    label='Start')
        if ending:
            ax1.plot(taf, x[taf], '<', mfc='g', mec='g', ms=10,
                        label='Ending')
        ax1.plot(ta, x[ta], 'o', mfc='r', mec='r', mew=1, ms=5,
                    label='Alarm')
    if len(ta) or ref is not None:
        ax1.legend(loc='best', framealpha=.5, numpoints=1)
    ax1.set_xlim(-.01*x.size, x.size*1.01-1)
    ax1.set_xlabel('Data #', fontsize=14)
    ax1.set_ylabel('Amplitude', fontsize=14)
    ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
    yrange = ymax - ymin if ymax > ymin else 1
    ax1.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
    ax1.set_title('Time series and detected changes ' +
                    '(threshold= %.3g, drift= %.3g): N changes = %d'
                    % (threshold, drift, len(tai)))
    ax2.plot(t, gp, 'y-', label='+')
    ax2.plot(t, gn, 'm-', label='-')
    ax2.set_xlim(-.01*x.size, x.size*1.01-1)
    ax2.set_xlabel('Data #', fontsize=14)
    ax2.set_ylim(-0.01*threshold, 1.1*threshold)
    ax2.axhline(threshold, color='r')
    ax1.set_ylabel('Amplitude', fontsize=14)
    ax2.set_title('Time series of the cumulative sums of ' +
                    'positive and negative changes')
    ax2.legend(loc='best', framealpha=.5, numpoints=1)
    plt.tight_layout()
    plt.show()
