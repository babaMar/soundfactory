from settings.plot import TONE_FREQ_MAP
from utils.helpers import (
    cents_from_freq_ratio,
    freq_at_n_semitones,
    freq_at_n_quartertones)
from utils.signal import freq_indexes, build_fft
import numpy as np


def test_cents_from_freq_ratio():
    octave_cents = cents_from_freq_ratio(TONE_FREQ_MAP['A4'], TONE_FREQ_MAP['A3'])
    assert int(round(octave_cents)) == 1200
    semitone_cents = cents_from_freq_ratio(TONE_FREQ_MAP['A3#'], TONE_FREQ_MAP['A3'])
    assert int(round(semitone_cents)) == 100
    tone_cents = cents_from_freq_ratio(TONE_FREQ_MAP['A3'], TONE_FREQ_MAP['G3'])
    assert int(round(tone_cents)) == 200


def test_freq_at_n_semitones():
    freq_semitone_up = freq_at_n_semitones(TONE_FREQ_MAP['A3'], 1)
    assert round(freq_semitone_up, 2) == TONE_FREQ_MAP['A3#']


def test_freq_at_n_quartertones():
    # Need to integrate quarter-tone notes in TONE_FREQ_MAP first
    pass


def test_freq_indexes(lengths_samplerates):
    def _test_case(n, samplerate):
        f = np.fft.fftfreq(n=n, d=1/samplerate)
        fi = freq_indexes(f, n=n, samplerate=samplerate)
        ranf = np.random.permutation(f)
        ranfi = freq_indexes(ranf, n=n, samplerate=samplerate)
        assert (f[fi] == f).all()
        assert (f[ranfi] == ranf).all()

    for case in lengths_samplerates:
        length, samplerate = case
        _test_case(length, samplerate)


def test_build_fft(signals):
    def _test_case(signal, samplerate):
        fft = np.fft.fft(signal)
        n = len(signal)
        if n % 2 == 0:
            fft[n//2] = 0
        freqs = np.fft.fftfreq(n, d=1/samplerate)
        amps = np.abs(fft) / n
        phases = np.angle(fft)
        rev_fft = build_fft(freqs, amps, phases, n / samplerate, samplerate)
        assert ((rev_fft.real - fft.real) < 1e-8).all()
        assert ((rev_fft.imag - fft.imag) < 1e-8).all()

    samplerate = 44100
    for signal in signals:
        _test_case(signal, samplerate)
