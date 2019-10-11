import pytest
import numpy as np
import scipy.signal as signal
from settings.input_validators import DEFAULT_WAVE_TYPE
from constants import DEFAULT_SAMPLERATE


def time_range(start=0., end=1., samples=DEFAULT_SAMPLERATE):
    return np.linspace(start, end, samples, endpoint=False)


def sine_wave(freq, samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples)
    sig = np.sin(2 * np.pi * freq * t)
    return sig


def square_wave(freq, samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples)
    sig = signal.square(2 * np.pi * freq * t)
    return sig


def sawtooth_wave(freq, samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples)
    sig = signal.sawtooth(2 * np.pi * freq * t)
    return sig


def triangle_wave(freq, samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples)
    phase_shift = np.pi / 2.  # a phase shift of 90° is needed to have signal=0. at t=0.
    sig = signal.sawtooth(2 * np.pi * freq * t + phase_shift, width=0.5)
    return sig


@pytest.fixture
def lengths_samplerates():
    yield ((121, 121.354), (1, 1), (1, 4), (12, 1), (3, 12), (3 * 44100, 44100))


@pytest.fixture
def signals():
    def _x(L, n):
        return np.linspace(0, L, n)
    yield (_x(1, 101),
           3.4 * np.sin(_x(1, 202)),
           2 * np.sin(_x(10, 80000)) + _x(1, 80000) + np.exp(_x(1, 80000)),
           [0] * 44101)


@pytest.fixture
def bad_wavecomponents():
    yield (
        "",
        "1", DEFAULT_WAVE_TYPE, "1,1"
        "1 " + DEFAULT_WAVE_TYPE, " ".join([DEFAULT_WAVE_TYPE]*2), "1,1 1",
        "1 1 sin",
        "1 2 {} 2".format(DEFAULT_WAVE_TYPE),
        "1 1 " + " ".join([DEFAULT_WAVE_TYPE]*2),
        "1 2 4 si",
    )
