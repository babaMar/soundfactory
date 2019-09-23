from random import choice
import numpy as np
from utils.signal import load_audio
from classes.signal_builder import SignalBuilder
from tests.conftest import (
    sine_wave, square_wave, time_range, sawtooth_wave, triangle_wave
    )
import matplotlib.pyplot as plt


TIME_RANGE = time_range()
TEST_FREQUENCIES = [
    27.0, 54.0, 108.0, 216.0, 432.0, 864.0,
    1728.0, 3456.0, 6912.0, 13824.0, 27648.0
]
APPROXIMATION_TOLERANCE = 0.01
WAVE_ANALYTICS = [sine_wave, square_wave, sawtooth_wave, triangle_wave]
WAVE_LABELS = ['sine', 'square', 'sawtooth', 'triangle']
WAVE_TOLERANCES = [1e-12, 1e-3, 1e-3, 1e-12]
WAVES = zip(WAVE_ANALYTICS, WAVE_LABELS, WAVE_TOLERANCES)


class ApproximationDifferences:
    sine = list()
    square = list()
    sawtooth = list()
    triangle = list()


# Y: Diff (for each wave form) X: Freq
def test_signal_approximation():
    for freq in TEST_FREQUENCIES:
        for analytic_sig, wave_shape, tolerance in WAVES:
            sig = analytic_sig(freq)
            signal_builder = SignalBuilder(
                [freq],
                [1.],
                [wave_shape],
                n_max=200,
                t_resolution=TIME_RANGE.size)
            rec_sig = signal_builder.signal
            diff = rec_sig - sig
            assert diff.mean() < tolerance


def test_export():
    filename = "export_test.wav"
    samplerate = 44100
    f = [432]
    a = [1]
    f, a = np.array(f), np.array(a)
    wave_types = ["sine"]
    s = SignalBuilder(f, a, wave_types, t_resolution=samplerate)
    s.export(filename, samplerate=samplerate)

    signal, samplerate = load_audio(filename)
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/samplerate)
    amps = 2 * (np.abs(fft) / len(signal))
    idx = np.where((amps > 1e-4) & (freqs >= 0))[0]
    assert (freqs[idx] - f < 1e-5).all()
    assert (amps[idx] - a < 1e-5).all()
