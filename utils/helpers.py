from math import log
import numpy as np

BASE = 2
CENTS_PER_OCTAVE = 1200
CENT = pow(BASE, 1. / CENTS_PER_OCTAVE)
SEMITONE_CENTS = 100
QUARTERTONE_CENTS = 50


def cents_from_freq_ratio(upper_tone, lower_tone):
    freq_ratio = upper_tone / lower_tone
    return CENTS_PER_OCTAVE * log(freq_ratio, BASE)


def freq_at_n_semitones(tone_freq, n):
    cents_interval = n * SEMITONE_CENTS
    return tone_freq * pow(2, cents_interval / CENTS_PER_OCTAVE)


def freq_at_n_quartertones(tone_freq, n):
    cents_interval = n * QUARTERTONE_CENTS
    return tone_freq * pow(2, cents_interval / CENTS_PER_OCTAVE)


def above_thr_mask(a, threshold=.1):
    """a is a numpy.array"""
    peak_threshold = threshold * a.max()
    return a >= peak_threshold


def spectrum(signal, samplerate):
    fft = np.fft.rfft(signal)
    freqs = np.fft.fftfreq(signal.size, d=1/samplerate)
    freqs_mask = np.where(freqs >= 0)[0]
    pws = np.abs(fft)**2
    return freqs[freqs_mask], pws[freqs_mask]
