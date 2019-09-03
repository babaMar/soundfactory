import numpy as np
from settings.signal import B_N_COEFF_MAP
from utils.signal import wn, sf_wav_sub
import soundfile as sf


class SignalBuilder(object):
    """ Create a Signal from Fourier Series
    """
    def __init__(
            self, frequencies, amplitudes,
            n_max=1000, wave_type='square', t_resolution=10000):
        self.amplitudes = set(amplitudes)
        self.frequencies = set(frequencies)
        self.nterms = n_max
        supported_forms = list(B_N_COEFF_MAP.keys())
        if wave_type not in supported_forms:
            raise Exception(
                'Wave form type must be one of %s' % supported_forms)
        self.time_resolution = t_resolution
        self.time_space = np.linspace(
            0., 1., self.time_resolution, endpoint=False)
        self.coefficients = B_N_COEFF_MAP[wave_type]   # array
        self.a0 = 0

    def get_time_space(self):
        return self.time_space

    def _fourier_series(self, x, freq):
        # Return the sum of all terms for a single point in time
        partial_sums = self.a0
        n = np.arange(1, self.nterms + 1)
        partial_sums += np.sum(self.coefficients(n) * np.sin(wn(n, freq) * x))
        return partial_sums

    def _single_component(self, amplitude, freq):
        res = [
            amplitude * self._fourier_series(_t, freq)
            for _t in self.time_space
        ]
        return np.asarray(res, dtype=np.float32)

    def build_signal(self):
        signal = np.zeros(self.time_resolution)
        for amp, freq in zip(self.amplitudes, self.frequencies):
            signal += self._single_component(amp, freq)
        return signal

    def export(self, signal, filename, bit_depth=16, samplerate=44100):
        try:
            signal = signal.real
        except AttributeError:
            signal = np.asarray(signal).real
        subtype = sf_wav_sub(bit_depth)
        sf.write(filename, signal, samplerate, subtype=subtype)
