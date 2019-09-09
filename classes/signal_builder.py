import numbers
import numpy as np
import soundfile as sf

from settings.signal import B_N_COEFF_MAP
from utils.signal import wn, find_soundfile_subtype
from settings.logging_settings import createlog


class SignalBuilderError(Exception):
    pass


class NotSupportedWaveShape(SignalBuilderError):
    def __init__(self, wave_shape, supported_shapes):
        self.message = '{} wave_type not supported. It must be one of {}'\
            .format(wave_shape, supported_shapes)
        createlog.error(self.message)

    def __str__(self):
        return self.message


class IdenticalFrequenciesDetected(SignalBuilderError):
    def __init__(self):
        self.message = 'Found duplicate frequency value in provided input'
        createlog.error(self.message)

    def __str__(self):
        return self.message


class ProvidedInputError(SignalBuilderError):
    def __init__(self, message):
        self.message = message
        createlog.error(self.message)

    def __str__(self):
        return self.message


class SignalBuilder(object):
    """ Create a Signal from Fourier Series """
    def __init__(
            self,
            frequencies,
            amplitudes,
            phases=None,
            n_max=1000,
            wave_type='sine',
            t_resolution=10000):
        self.frequencies = frequencies
        self.amplitudes = amplitudes
        self.phases = None
        self.set_phases(phases)
        self.check_input()
        self.nterms = n_max
        supported_wave_shapes = list(B_N_COEFF_MAP.keys())
        if wave_type not in supported_wave_shapes:
            raise NotSupportedWaveShape(wave_type, supported_wave_shapes)

        self.time_resolution = t_resolution
        self.time_space = np.linspace(
            0., 1., self.time_resolution, endpoint=False)
        self.coefficients = B_N_COEFF_MAP[wave_type]   # array
        self.a0 = 0
        self.signal = self.build_signal()

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

    def export(self, filename, bit_depth=16, samplerate=44100):
        subtype = find_soundfile_subtype(bit_depth)
        sf.write(filename, self.signal, samplerate, subtype=subtype)

    def check_input(self):
        f, a, p = self.frequencies, self.amplitudes, self.phases
        if not len(set(f)) == len(f):
            raise IdenticalFrequenciesDetected()
        if len({len(x) for x in [f, a, p]}) > 1:
            raise ProvidedInputError('Provided frequency, amplitudes, and phases need to be equals in number')
        if any(not isinstance(x, numbers.Real) for l in [f, a, p] for x in l):
            raise ProvidedInputError('Use only real numbers (floats or ints)')

    def set_phases(self, phases):
        if phases is None:
            self.phases = [0] * len(self.frequencies)
        else:
            self.phases = phases
