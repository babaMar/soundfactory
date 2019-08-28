from math import log

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
