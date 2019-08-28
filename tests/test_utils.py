from settings.plot import TONE_FREQ_MAP
from utils.helpers import (cents_from_freq_ratio,
                           freq_at_n_semitones,
                           freq_at_n_quartertones)


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
