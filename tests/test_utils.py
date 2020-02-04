import numpy as np
from soundfactory.utils.helpers import (
    cents_from_freq_ratio,
    freq_at_n_semitones,
    freq_at_n_quartertones
)
from soundfactory.constants import (
    _24_TET_SCALE_INIT,
    A_SUB_SUB_CONTRA_FREQ
)
from soundfactory.settings.plot import TONE_FREQ_MAP
from soundfactory.utils.signal import (
    freq_indexes, build_fft, write_stereo, load_audio
)
from soundfactory.utils.scale import (
    next_label, next_freq, build_24_tet_scale, build_24_tet_scale_by_sequence
)
from soundfactory.utils.labels import remove_close_values_on_log_scale
from pathlib import Path


def test_cents_from_freq_ratio():
    octave_cents = cents_from_freq_ratio(TONE_FREQ_MAP['A4'], TONE_FREQ_MAP['A3'])
    assert int(round(octave_cents)) == 1200
    semitone_cents = cents_from_freq_ratio(TONE_FREQ_MAP['A3#'], TONE_FREQ_MAP['A3'])
    assert int(round(semitone_cents)) == 100
    tone_cents = cents_from_freq_ratio(TONE_FREQ_MAP['A3'], TONE_FREQ_MAP['G3'])
    assert int(round(tone_cents)) == 200


def test_freq_at_n_quartertones():
    freq_quartertone_up = freq_at_n_quartertones(A_SUB_SUB_CONTRA_FREQ, 1)
    # See https://en.wikipedia.org/wiki/Cent_(music)#Use
    assert freq_quartertone_up == A_SUB_SUB_CONTRA_FREQ * pow(2, 50 / 1200)


def test_freq_at_n_semitones():
    freq_semitone_up = freq_at_n_semitones(TONE_FREQ_MAP['A3'], 1)
    assert round(freq_semitone_up, 2) == TONE_FREQ_MAP['A3#']


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


def test_24_scale_builder():

    def repeat(foo, n, x):
        for _ in range(n):
            x = foo(x)
        return x

    ref_label = list(_24_TET_SCALE_INIT.keys())[-1]
    ref_frequency = list(_24_TET_SCALE_INIT.values())[-1]
    quarter_tone_up_label, quarter_tone_up_freq = (
         next_label(ref_label), next_freq(ref_frequency)
        )
    diff = abs(
        quarter_tone_up_freq - (A_SUB_SUB_CONTRA_FREQ * pow(2, 50 / 1200)))
    assert quarter_tone_up_label == 'A-1𝄲'
    assert diff < 1e-2
    
    semitone_tone_up_label, semitone_tone_up_freq = (
        next_label(quarter_tone_up_label), next_freq(quarter_tone_up_freq)
    )
    diff = abs(
        semitone_tone_up_freq - (A_SUB_SUB_CONTRA_FREQ * pow(2, 100 / 1200)))
    assert semitone_tone_up_label == 'A-1#'
    assert diff < 1e-2

    three_quarter_tone_up_label, three_quarter_tone_up_freq = (
        next_label(semitone_tone_up_label), next_freq(semitone_tone_up_freq)
    )
    diff = abs(
        three_quarter_tone_up_freq -
        (A_SUB_SUB_CONTRA_FREQ * pow(2, 150 / 1200)))
    assert three_quarter_tone_up_label == 'B-1𝄳'
    assert diff < 1e-2

    tone_up_label, tone_up_freq = (
        next_label(three_quarter_tone_up_label),
        next_freq(three_quarter_tone_up_freq)
    )
    diff = abs(tone_up_freq - (A_SUB_SUB_CONTRA_FREQ * pow(2, 200 / 1200)))
    assert tone_up_label == 'B-1'
    assert diff < 1e-2

    c0_label, c0_frequency = (
        repeat(next_label, 2, tone_up_label),
        repeat(next_freq, 2, tone_up_freq)
        )
    assert c0_label == 'C0'
    assert abs(c0_frequency - TONE_FREQ_MAP['C0']) < 1e-2

    f0_label, f0_frequency = (
        repeat(next_label, 10, c0_label),
        repeat(next_freq, 10, c0_frequency)
    )
    assert f0_label == 'F0'
    assert abs(f0_frequency - TONE_FREQ_MAP['F0']) < 1e-2


def test_24_scale_builder_by_sequence():
    ref_label = list(_24_TET_SCALE_INIT.keys())[-1]
    ref_frequency = list(_24_TET_SCALE_INIT.values())[-1]
    scale_24 = build_24_tet_scale(ref_label, ref_frequency)
    scale_24_by_sequence = build_24_tet_scale_by_sequence(
        ref_label, ref_frequency)
    assert scale_24 == scale_24_by_sequence


def test_remove_close_values_on_log_scale():
    freqs = [
        687.17735221, 692.42298085,
        681.93172356, 860.28309742,
        855.03746878
    ]
    assert remove_close_values_on_log_scale(freqs) == [freqs[0], freqs[3]]


def test_write_stereo(mono8bit_audio_file, mono_audio_file):
    c1_path = mono_audio_file
    c2_path = mono_audio_file
    left, l_samplerate = load_audio(c1_path)
    right, r_samplerate = load_audio(c2_path)
    assert l_samplerate == r_samplerate
    out = "stereo_test.wav"
    write_stereo(left, right, out, samplerate=l_samplerate)
    stereo, samplerate = load_audio(out)
    c1, c2 = stereo[:, 0], stereo[:, 1]
    Path(out).unlink()
    assert (c1 == left).all()
    assert (c2 == right).all()
