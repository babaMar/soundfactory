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
            sig = analytic_sig(freq, samplerate)
            signal_builder = SignalBuilder(
                [freq],
                [1.],
                [wave_shape],
                n_max=1000,
                samplerate=samplerate)
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
    s = SignalBuilder(f, a, wave_types, t_resolution=samplerate)
    s.export(filename, samplerate=samplerate)

    signal, samplerate = load_audio(filename)
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/samplerate)
    amps = 2 * (np.abs(fft) / len(signal))
    idx = np.where((amps > 1e-4) & (freqs >= 0))[0]
    assert (freqs[idx] - f < 1e-5).all()
    assert (amps[idx] - a < 1e-5).all()


def test_time_shift():
    freq, amp = 2.3, 4
    for shape in WAVE_LABELS:
        s0 = SignalBuilder([freq], [amp], [shape], phases=[0])
        np.testing.assert_almost_equal(s0.time_shift(1, freq), s0.signal)
        np.testing.assert_almost_equal(s0.time_shift(13, freq), s0.signal)


def test_phase_shift():
    freq, amp = 2.3, 1
    for shape in WAVE_LABELS:
        s0 = SignalBuilder([freq], [amp], [shape], phases=[0])
        np.testing.assert_almost_equal(s0.phase_shift(360, freq), s0.signal)
        np.testing.assert_almost_equal(s0.phase_shift(720, freq), s0.signal)


def test_initial_phase():
    tolerance = 1e-5
    shift_tolerance = 6e-1
    freq, amp = 2.3, 4
    for shape in WAVE_LABELS:
        s0 = SignalBuilder(
            [freq], [amp], [shape], phases=[0])
        for ph in [360, 720]:
            builder = SignalBuilder([freq], [amp], [shape], phases=[ph])
            assert (np.abs(s0.signal - builder.signal) < tolerance).all()
            
        s0 = SignalBuilder(
            [freq], [amp], [shape], phases=[0], t_resolution=96000)

        for ph in [45, 90, 180]:
            builder = SignalBuilder(
                [freq], [amp], [shape], phases=[ph], t_resolution=96000)
            shifted = s0.phase_shift(ph, freq)
            assert (
                np.abs(shifted - builder.signal[:len(shifted)])
                < shift_tolerance).all()
