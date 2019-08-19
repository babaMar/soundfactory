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
