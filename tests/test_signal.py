import numpy as np
from soundfactory.signal_base import Signal


def test_mono_input(mono_audio_file):
    s = Signal(mono_audio_file, with_envelope=True)
    assert s.MONO
    assert s.sampling_rate > 0
    assert s.CALCULATE_ENVELOPE

    assert 'ch1' in s.CHANNELS
    channel = s.CHANNELS['ch1']
    assert isinstance(channel, np.ndarray)
    assert channel.size > 0
    assert s.duration > 0

    assert 'ch1_envelope' in s.ENVELOPES
    envelope = s.ENVELOPES['ch1_envelope']
    assert isinstance(envelope, np.ndarray)
    assert envelope.size > 0
    assert np.all(envelope > 0)

    assert 'ch1_fft' in s.SPECTRA
    frequency_spectrum = s.SPECTRA['ch1_fft']
    assert isinstance(frequency_spectrum,dict)
    assert 'freqs' in frequency_spectrum
    assert 'pws' in frequency_spectrum
    freqs = frequency_spectrum['freqs']
    pws = frequency_spectrum['pws']
    assert freqs.size == pws.size
    assert np.all(freqs >= 0)
    assert np.all(pws > 0)

    _s = Signal(mono_audio_file)
    assert not _s.CALCULATE_ENVELOPE
    assert len(_s.ENVELOPES) == 0, _s.ENVELOPES


def test_stereo_input(stereo_audio_file):
    s = Signal(stereo_audio_file, with_envelope=True)
    assert not s.MONO
    assert s.sampling_rate > 0
    assert s.CALCULATE_ENVELOPE

    for ch in ('ch1', 'ch2'):
        ch_envelope = ch + s.ENVELOPE_SUFFIX
        ch_fft = ch + s.FFT_SUFFIX

        assert ch in s.CHANNELS
        channel = s.CHANNELS[ch]
        assert isinstance(channel, np.ndarray)
        assert channel.size > 0
        assert s.duration > 0

        assert ch_envelope in s.ENVELOPES
        envelope = s.ENVELOPES[ch_envelope]
        assert isinstance(envelope, np.ndarray)
        assert envelope.size > 0
        assert np.all(envelope > 0)

        assert ch_fft in s.SPECTRA
        frequency_spectrum = s.SPECTRA[ch_fft]
        assert isinstance(frequency_spectrum,dict)
        assert 'freqs' in frequency_spectrum
        assert 'pws' in frequency_spectrum
        freqs = frequency_spectrum['freqs']
        pws = frequency_spectrum['pws']
        assert freqs.size == pws.size
        assert np.all(freqs >= 0)
        assert np.all(pws > 0)

    _s = Signal(stereo_audio_file)
    assert not _s.CALCULATE_ENVELOPE
    assert len(_s.ENVELOPES) == 0, _s.ENVELOPES
