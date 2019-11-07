import os
import pytest
import numpy as np
import scipy.signal as signal
from pathlib import Path

from soundfactory.settings.input_validators import DEFAULT_WAVE_TYPE
from soundfactory.constants import DEFAULT_SAMPLERATE


def time_range(start=0., end=1., samples=DEFAULT_SAMPLERATE):
    return np.linspace(start, end, int(samples), endpoint=False)


def sine_wave(freq, phase=0, end=1., samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples, end=end)
    sig = np.sin(2 * np.pi * freq * t + np.radians(phase))
    return sig


def square_wave(freq, phase=0, end=1., samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples, end=end)
    sig = signal.square(2 * np.pi * freq * t + np.radians(phase))
    return sig


def sawtooth_wave(freq, phase=0, end=1., samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples, end=end)
    sig = signal.sawtooth(2 * np.pi * freq * t + np.radians(phase))
    return sig


def triangle_wave(freq, phase=0, end=1., samples=DEFAULT_SAMPLERATE):
    t = time_range(samples=samples, end=end)
    phase_shift = np.pi / 2.  # a phase shift of 90° is needed to have signal=0. at t=0.
    sig = signal.sawtooth(
        2 * np.pi * freq * t + phase_shift
        + np.radians(phase),
        width=0.5)
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


@pytest.fixture
def testfile_path():
    path = '/tmp/export_test.wav'
    yield path
    os.remove(path)


@pytest.fixture
def mono_audio_file():
    return str(Path(__file__).parent.parent / 'samples' / 'mono_bell.wav')


@pytest.fixture
def stereo_audio_file():
    return str(Path(__file__).parent.parent / 'samples' / 'A3-Calib-220.wav')
