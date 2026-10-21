import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from detecta import detect_cusum


def _legacy_detection(x, threshold, drift):
    """Detection part of detect_cusum 0.0.5 (first differences), frozen."""
    x = np.atleast_1d(x).astype('float64')
    gp, gn = np.zeros(x.size), np.zeros(x.size)
    ta, tai = np.array([[], []], dtype=int)
    tap, tan = 0, 0
    for i in range(1, x.size):
        s = x[i] - x[i-1]
        gp[i] = gp[i-1] + s - drift
        gn[i] = gn[i-1] - s - drift
        if gp[i] < 0:
            gp[i], tap = 0, i
        if gn[i] < 0:
            gn[i], tan = 0, i
        if gp[i] > threshold or gn[i] > threshold:
            ta = np.append(ta, i)
            tai = np.append(tai, tap if gp[i] > threshold else tan)
            gp[i], gn[i] = 0, 0
    return ta, tai


def _signal(seed):
    """Steps, ramps, sinusoids and random walks with random parameters."""
    rng = np.random.default_rng(seed)
    n = 300
    t = np.arange(n)
    kind = seed % 4
    if kind == 0:
        x = rng.normal(0, 1, n)
        for _ in range(rng.integers(1, 4)):
            a = rng.integers(20, 260)
            x[a:a + rng.integers(10, 60)] += rng.choice([-1, 1]) * rng.uniform(2, 6)
    elif kind == 1:
        x = rng.normal(0, 1, n)
        x[100:200] += np.linspace(0, rng.uniform(2, 8), 100)
    elif kind == 2:
        x = rng.uniform(1, 3)*np.sin(2*np.pi*t/rng.uniform(40, 150)) + rng.normal(0, .3, n)
    else:
        x = np.cumsum(rng.normal(0, 1, n))
    return x, rng.uniform(1, 4), rng.uniform(0, 1)


def _shift(seed=0, n=400, at=200, delta=1.0):
    """Gaussian noise (sd=1) with a small sustained shift in the mean."""
    x = np.random.default_rng(seed).normal(0, 1, n)
    x[at:] += delta
    return x


@pytest.mark.parametrize("seed", range(200))
def test_previous_reference_keeps_legacy_detection(seed):
    x, threshold, drift = _signal(seed)
    ta0, tai0 = _legacy_detection(x, threshold, drift)
    for kwargs in ({}, {'reference': 'previous'}):
        ta, tai, taf, amp = detect_cusum(x, threshold, drift, show=False, **kwargs)
        assert ta.tolist() == ta0.tolist()
        assert tai.tolist() == tai0.tolist()
        assert taf.size == 0 and amp.size == 0


def test_invalid_reference_raises():
    with pytest.raises(ValueError):
        detect_cusum([0, 1, 2], reference='median', show=False)


@pytest.mark.parametrize("kwargs", [{'reference': 'mean'}, {'reference': 'run_mean'},
                                    {'reference': 'residual', 'alpha': 0.01}])
def test_reference_detects_small_sustained_shift(kwargs):
    # a shift of one standard deviation is hard to see sample by sample but
    # accumulates when compared with a reference level
    ta, tai, _, _ = detect_cusum(_shift(), 8, 0.5, show=False, **kwargs)
    assert ta.size == 1
    assert 190 <= tai[0] <= 210
    assert 200 <= ta[0] <= 240


def test_previous_reference_misses_small_sustained_shift():
    ta, _, _, _ = detect_cusum(_shift(), 8, 0.5, show=False)
    assert ta.size == 0


def test_mean_reference_from_baseline():
    # the baseline (first n_baseline samples) defines the reference level
    x = np.r_[np.zeros(50), np.ones(50)]
    ta, tai, _, _ = detect_cusum(x, 2, .1, reference='mean', n_baseline=10, show=False)
    assert ta.tolist() == [52]
    assert tai.tolist() == [49]


def test_fixed_reference_value_does_not_restart():
    # with a fixed reference, a sustained shift keeps triggering alarms
    x = np.r_[np.zeros(50), np.ones(50)]
    ta, _, _, _ = detect_cusum(x, 2, .1, reference=0.0, show=False)
    assert ta.tolist() == [52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88,
                           91, 94, 97]


def test_estimated_reference_restarts_after_alarm():
    x = np.r_[np.zeros(50), np.ones(50)]
    for reference in ('mean', 'run_mean', 'residual'):
        ta, _, _, _ = detect_cusum(x, 2, 0, reference=reference, show=False)
        assert ta.size == 1, reference


@pytest.mark.parametrize("kwargs", [{'reference': 'mean'}, {'reference': 'run_mean'},
                                    {'reference': 'residual', 'alpha': 0.01}])
def test_reference_restart_is_not_a_single_noisy_sample(kwargs):
    # after the alarm, the reference must not be dominated by the noise of
    # the sample where it restarted (it would cause false alarms)
    x = np.random.default_rng(42).normal(0, 1, 600)
    x[200:400] += 1.5
    ta, tai, taf, amp = detect_cusum(x, 8, .75, ending=True, show=False, **kwargs)
    assert tai == pytest.approx([199, 399], abs=2)
    assert taf == pytest.approx([200, 400], abs=2)
    assert amp == pytest.approx([1.5, -1.5], abs=0.2)


def test_residual_with_alpha_one_equals_previous():
    for seed in range(50):
        x, threshold, drift = _signal(seed)
        ta0, _, _, _ = detect_cusum(x, threshold, drift, show=False)
        ta1, _, _, _ = detect_cusum(x, threshold, drift, reference='residual',
                                    alpha=1, show=False)
        assert ta1.tolist() == ta0.tolist()


@pytest.mark.parametrize("seed", range(300))
def test_ending_keeps_the_detected_changes(seed):
    # estimating the ending must not drop or replace detected changes;
    # changes with the same start are the same change (first alarm kept)
    x, threshold, drift = _signal(seed)
    ta0, tai0, _, _ = detect_cusum(x, threshold, drift, show=False)
    tai0, ind = np.unique(tai0, return_index=True)
    ta, tai, taf, amp = detect_cusum(x, threshold, drift, ending=True, show=False)
    assert tai.tolist() == tai0.tolist()
    assert ta.tolist() == ta0[ind].tolist()
    assert taf.size == tai.size == amp.size


@pytest.mark.parametrize("seed", range(300))
def test_ending_is_inside_its_own_segment(seed):
    x, threshold, drift = _signal(seed)
    ta, tai, taf, amp = detect_cusum(x, threshold, drift, ending=True, show=False)
    assert (taf >= tai).all()
    assert (taf[:-1] < tai[1:]).all()
    assert (taf < x.size).all()


@pytest.mark.parametrize("reference", ['previous', 'mean', 'run_mean', 'residual'])
def test_ending_and_amplitude_of_steps(reference):
    x = np.random.default_rng(1).normal(0, .2, 300)
    x[100:200] += 5
    ta, tai, taf, amp = detect_cusum(x, 2, .5, ending=True, reference=reference,
                                     show=False)
    assert tai.tolist() == [99, 199]
    assert taf.tolist() == [100, 200]
    # amplitude is the difference between the mean levels after and before
    assert amp == pytest.approx([5, -5], abs=0.1)


@pytest.mark.parametrize("reference", ['mean', 'run_mean', 'residual'])
def test_ending_of_noisy_steps_and_ramps(reference):
    # steps and 20-sample ramps of 4 sd in noise with sd = 1
    x = np.random.default_rng(3).normal(0, 1, 600)
    x[150:] += 4
    x[300:320] -= np.linspace(4/20, 4, 20)
    x[320:] -= 4
    x[450:] += 4
    ta, tai, taf, amp = detect_cusum(x, 6, 2, ending=True, reference=reference,
                                     show=False)
    assert tai[[0, 2]] == pytest.approx([149, 449], abs=2)
    assert taf[[0, 2]] == pytest.approx([150, 450], abs=2)
    # the start and the end of a ramp are found where its deviation exceeds
    # the drift (here, about 10 samples inside the ramp)
    assert 299 <= tai[1] <= 312
    assert 307 <= taf[1] <= 324
    assert amp == pytest.approx([4, -4, 4], abs=0.5)


@pytest.mark.parametrize("reference", ['previous', 'mean', 0.0])
def test_plot_with_reference(reference):
    import matplotlib.pyplot as plt
    detect_cusum(_shift(), 8, 0.5, ending=True, reference=reference, show=True)
    plt.close('all')
