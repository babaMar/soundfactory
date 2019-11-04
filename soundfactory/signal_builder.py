import numbers
import numpy as np

from .constants import DEFAULT_SAMPLERATE
from .settings.signal import B_N_COEFF_MAP
from .utils.signal import wn, write
from .settings.logging_settings import createlog


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


class SignalBuilder:
    """ Create a Signal from Fourier Series """
    def __init__(
            self,
            frequencies,
            amplitudes,
            wave_types,
            phases=None,
            n_max=1000,
            duration=1.,
            samplerate=DEFAULT_SAMPLERATE
    ):
        self.frequencies = frequencies
        self.amplitudes = amplitudes
        self.phases = phases,
        self.set_phases(phases)
        self.wave_types = wave_types
        self.check_input()
        self.n_terms = np.arange(1, n_max + 1)
        self.duration = duration
        self.samplerate = samplerate
        self.n_samples = int(self.duration * self.samplerate)
        self.time_space = np.linspace(
            0., self.duration, self.n_samples, endpoint=False
        )
        self.a0 = 0
        self.signal = self.build_signal()
        self.scaled_signal = self.signal

    def get_time_space(self):
        return self.time_space

    def _fourier_series(self, x, freq, ph, shape):
        # Return the sum of all terms for a single point in time
        partial_sums = self.a0
        coefficients = B_N_COEFF_MAP[shape]
        n = self.n_terms
        partial_sums += np.sum(
            coefficients(n) * np.sin(
                wn(n, freq) * x
                + n * np.radians(ph)
            ))
        return partial_sums

    def check_input(self):
        f, a, p = self.frequencies, self.amplitudes, self.phases
        if not len(set(f)) == len(f):
            raise IdenticalFrequenciesDetected()
        if len({len(x) for x in [f, a, p]}) > 1:
            raise ProvidedInputError(
                'Provided frequency, amplitudes, and phases '
                'need to be equals in number'
            )
        if any(not isinstance(x, numbers.Real) for l in [f, a, p] for x in l):
            raise ProvidedInputError('Use only real numbers (floats or ints)')

    def set_phases(self, phases):
        if phases is None:
            self.phases = [0] * len(self.frequencies)
        else:
            self.phases = phases

    def _single_component(self, a, f, ph, shape):
        period = [
            a * self._fourier_series(_t, 1/self.duration, ph, shape)
            for _t in self.time_space
        ]
        period = np.asarray(period, dtype=np.float64)
        N = self.n_samples
        cycles = f * self.duration
        idxs = (np.round((np.arange(0, N) * cycles)) % N).astype(int)
        return period[idxs]

    def build_signal(self):
        signal = np.zeros(self.n_samples, dtype='float64')
        for freq, amp, ph, shape in zip(
                self.frequencies,
                self.amplitudes,
                self.phases,
                self.wave_types):
            createlog.info(
                "Adding components from {s} wave of {f} hz frequency".format(
                    s=shape, f=freq
                ))
            signal += self._single_component(amp, freq, ph, shape)
        return signal

    def export(self, path, bit_depth=16):
        self.scaled_signal /= np.max(np.abs(self.signal), axis=0)
        write(
            self.scaled_signal, path, samplerate=self.samplerate, bit_depth=bit_depth
        )
