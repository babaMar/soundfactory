from scipy.signal import hilbert
# from python_toolbox import caching
import soundfile as sf
import numpy as np


#@caching.cache()
def get_envelope(mono_audio):
    analytic_audio = hilbert(mono_audio)
    return np.abs(analytic_audio)


def load_audio(wavfile):
    # Load audio
    f = sf.SoundFile(wavfile)
    samplerate = f.samplerate
    # Stereo signal
    signal = f.read(dtype=np.float32)
    return signal, samplerate


def wn(n, freq):
    # Return the w_n angular frequency
    wn = (2 * np.pi * n) * freq
    return wn


def sf_wav_sub(depth, default=16):
    """ Find wav subtype for given bit depth"""
    try:
        subs = sf.available_subtypes("wav")
        r = next(
            k for k in subs
            if k.startswith("PCM") and k.endswith(str(depth))
        )
    except StopIteration:
        print("depth not available, default {} bits selected".format(default))
        r = "PCM_{}".format(default)
    return r


def freq_indexes(freqs, n=44100, samplerate=44100):
    """
    Find positions of freqs in the numpy.fft.fftfreq
    with given n e spacing = 1 / samplerate

    Params
    ------
    freqs (float or array) -- frequencies to find index of
    n (int) -- the n argument in numpy.fft.fftfreq
    samplerate (float) -- points per second

    Returns
    -------
    array of indexes

    """
    d = 1 / samplerate
    return np.round(freqs * n * d).astype(int)


def build_fft(freqs, amps, phases, period=1, samplerate=44100):
    """
    Build fft 'standard' components (see numpy.fft docs) from
    given freqs, amps, phases, and a signal with given
    period and samplerate

    NOTE:
    freqs, amps and phases must be in the same order to refer to the
    Fourier component
    """
    freqs, amps, phases = np.array(freqs), np.array(amps), np.array(phases)
    idx = np.where(freqs >= 0)[0]
    freqs, amps, phases = freqs[idx], amps[idx], phases[idx]
    n = np.round(period * samplerate).astype(int)
    amps = amps * n

    N = (n-1)//2 + 1
    r = np.zeros(N, dtype=np.complex_)
    freq_idx = freq_indexes(freqs, n=n, samplerate=samplerate)
    pos_X_k = amps * np.exp(1j * phases)
    r[freq_idx] = pos_X_k
    if N > n//2:
        neg_X_k = r[::-1][:-1].conj()
    else:
        neg_X_k = np.concatenate(([0], r[::-1][:-1])).conj()
    return np.concatenate((r, neg_X_k))


def build_signal(freqs, amps, phases, period=1, samplerate=44100):
    fft = build_fft(freqs, amps, phases, period=period, samplerate=samplerate)
    return np.fft.ifft(fft)
