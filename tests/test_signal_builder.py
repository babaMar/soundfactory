import numpy as np
from utils.signal import load_audio
from classes.signal_builder import SignalBuilder
from tests.conftest import (
    sine_wave, square_wave, time_range, sawtooth_wave, triangle_wave
    )
from constants import DEFAULT_SAMPLERATE


TIME_RANGE = time_range()
TEST_FREQUENCIES = [
    832.2, 30.1, 1.9, 1, 432
]
APPROXIMATION_TOLERANCE = 0.01
WAVE_ANALYTICS = [sine_wave, square_wave, sawtooth_wave, triangle_wave]
WAVE_LABELS = ['sine', 'square', 'sawtooth', 'triangle']
WAVE_TOLERANCES = [1e-2, 1e-2, 1e-2, 1e-2]
WAVES = list(zip(WAVE_ANALYTICS, WAVE_LABELS, WAVE_TOLERANCES))


class ApproximationDifferences:
    sine = list()
    square = list()
    sawtooth = list()
    triangle = list()


# Y: Diff (for each wave form) X: Freq
def test_signal_approximation():
    samplerate = DEFAULT_SAMPLERATE
    for freq in TEST_FREQUENCIES:
        for analytic_sig, wave_shape, tolerance in WAVES:
            sig = analytic_sig(freq, samples=samplerate)
            signal_builder = SignalBuilder(
                [freq],
                [1.],
                [wave_shape],
                n_max=1000,
                samplerate=samplerate
            )
            rec_sig = signal_builder.signal
            diff = np.abs(rec_sig - sig)
            assert diff.mean() < tolerance


def test_export():
    filename = "export_test.wav"
    samplerate = 44100
    f = [432]
    a = [1]
    f, a = np.array(f), np.array(a)
    wave_types = ["sine"]
    s = SignalBuilder(f, a, wave_types, samplerate=samplerate)
    s.export(filename)

    signal, samplerate = load_audio(filename)
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/samplerate)
    amps = 2 * (np.abs(fft) / len(signal))
    idx = np.where((amps > 1e-4) & (freqs >= 0))[0]
    assert (freqs[idx] - f < 1e-5).all()
    assert (amps[idx] - a < 1e-5).all()


def test_phase_shift():
    freq, amp = 2.3, 1
    for analytic, shape, tolerance in WAVES:
        for phase in [0, 180, 45.7]:
            builder = SignalBuilder(
                [freq], [amp], [shape], phases=[phase])
            analytic_sig = amp * analytic(freq, phase=phase)
            diff = builder.signal - analytic_sig
            assert abs(diff).mean() < tolerance
