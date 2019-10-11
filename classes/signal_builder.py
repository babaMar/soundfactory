import numbers
import numpy as np

from constants import DEFAULT_SAMPLERATE
from settings.signal import B_N_COEFF_MAP
from utils.signal import wn, write
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


DEFAULT_SAMPLERATE = 44100

class SignalBuilder:
    """ Create a Signal from Fourier Series """
    def __init__(
            self,
            frequencies,
            amplitudes,
            wave_types,
            phases=None,
            n_max=1000,
            t_resolution=10000,
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
        self.time_resolution = t_resolution
        self.n_samples = int(self.duration * self.samplerate)
        self.time_space = np.linspace(
            0., self.duration, self.n_samples, endpoint=False
        )
        self.a0 = 0
        self.signal = self.build_signal()

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
                # + n*np.radians(ph)
            ))
        return partial_sums

    def _single_component(self, amplitude, freq, ph, shape):
        res = [
            amplitude * self._fourier_series(_t, freq, ph, shape)
            for _t in self.time_space
        ]
        return np.asarray(res, dtype=np.float32)

    def build_signal(self):
        signal = np.zeros(self.n_samples)
        for freq, amp, ph, shape in zip(
                self.frequencies,
                self.amplitudes,
                self.phases,
                self.wave_types):
            createlog.info(
                "Adding components from {s} wave of {f} hz frequency".format(
                    s=shape, f=freq
                ))
            signal += self._single_component_from_period(amp, freq, ph, shape)
        return signal

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

    @staticmethod
    def deg2time(deg, freq):
        return (deg/360) * (1/freq)

    @staticmethod
    def index_at_time_shift(t, duration, rate):
        return int(round(((t % duration) * rate)))

    @staticmethod
    def index_at_first_period(freq, rate, duration):
        return int(round((rate*duration) / freq))
        
    def time_shift(self, t, freq):
        i0 = self.index_at_time_shift(t, self.duration, self.time_resolution)
        period_pos = self.index_at_first_period(
            freq, self.time_resolution, self.duration)
        decimal_freq_pos = int(round((freq - int(freq)) * period_pos))
        shifted = np.concatenate((
            self.signal[i0:period_pos],
            np.tile(self.signal[:period_pos], int(freq - 1)),
            self.signal[:i0 + decimal_freq_pos]
        ))[:len(self.time_space)]
        return shifted
        
    def phase_shift(self, ph, freq):
        delt = self.deg2time(ph, freq) % (1/freq)
        return self.time_shift(delt, freq)
    
    def _single_component_from_period(self, a, f, ph, shape):
        period = [
            a * self._fourier_series(_t, 1, ph, shape)
            for _t in self.time_space
        ]
        period = np.asarray(period, dtype=np.float32)
        N = self.n_samples
        idxs = (np.round((np.arange(0, N) * f)) % N).astype(int)
        return period[idxs]

    def export(self, path, bit_depth=16):
        write(
            self.signal, path, samplerate=self.samplerate, bit_depth=bit_depth
        )

