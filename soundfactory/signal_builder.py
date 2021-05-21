import numbers
import numpy as np
from pathlib import Path

from .constants import DEFAULT_SAMPLERATE
from .settings.signal import B_N_COEFF_MAP
from .utils.signal import write
from .settings.logging_settings import createlog
from .utils.helpers import load_cache, single_component_cache_key, cache_it
from soundfactory.cyutils import builder_utils as cy_builder_utils

CACHE_PATH = str(Path(__file__).resolve().parent / 'signal_builder.pickle')
CACHE = load_cache(path=CACHE_PATH)


class SignalBuilderError(Exception):
    pass


class NotSupportedWaveShape(SignalBuilderError):
    def __init__(self, wave_shape, supported_shapes):
        self.message = "{} wave_type not supported. It must be one of {}".format(
            wave_shape, supported_shapes
        )
        createlog.error(self.message)

    def __str__(self):
        return self.message


class IdenticalFrequenciesDetected(SignalBuilderError):
    def __init__(self):
        self.message = "Found duplicate frequency value in provided input"
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
        duration=1.0,
        samplerate=DEFAULT_SAMPLERATE,
    ):
        self.frequencies = frequencies
        self.amplitudes = amplitudes
        self.phases = None
        self.set_phases(phases)
        self.wave_types = wave_types
        self.check_input()
        self.n_terms = np.arange(1, n_max + 1, dtype=np.int64)
        self.duration = duration
        self.samplerate = samplerate
        self.n_samples = int(self.duration * self.samplerate)
        self.time_space = np.linspace(
            0.0, self.duration, self.n_samples, endpoint=False, dtype=np.float64
        )
        self.a0 = 0
        self.signal = self.build_signal()
        self.scaled_signal = self.signal / np.max(np.abs(self.signal), axis=0)

    def get_time_space(self):
        return self.time_space

    def check_input(self):
        f, a, p = self.frequencies, self.amplitudes, self.phases
        if not len(set(f)) == len(f):
            raise IdenticalFrequenciesDetected()
        if len({len(x) for x in [f, a, p]}) > 1:
            raise ProvidedInputError(
                "Provided frequency, amplitudes, and phases "
                "need to be equals in number"
            )
        if any(not isinstance(x, numbers.Real) for l in [f, a, p] for x in l):
            raise ProvidedInputError("Use only real numbers (floats or ints)")

    def set_phases(self, phases):
        if phases is None:
            self.phases = [0.] * len(self.frequencies)
        else:
            self.phases = phases

    @cache_it(CACHE, single_component_cache_key, path=CACHE_PATH)
    def _compute_component(self, _freq, _amp, _phase, _shape, n_max, samplerate, duration):
        # n_max and samplerate are used in the specified key_encoder to create the cache key
        coefficients = B_N_COEFF_MAP[_shape]
        coefficients = np.asarray(coefficients(self.n_terms), dtype=np.float64)
        upsampled = cy_builder_utils.upsample_component(
            _amp, _phase, duration, self.time_space, coefficients, self.n_terms
        )
        component = cy_builder_utils.single_component(
            _freq, self.duration, upsampled, self.n_samples
        )
        return component

    def build_signal(self):
        signal = np.zeros(self.n_samples, dtype="float64")
        for freq, amp, ph, shape in zip(
            self.frequencies, self.amplitudes, self.phases, self.wave_types
        ):
            freq = round(freq, 2)
            createlog.info(
                "Adding components from {s} wave of {f} hz frequency with amplitude {a}".format(
                    s=shape, f=freq, a=round(amp, 2)
                )
            )
            signal += self._compute_component(
                float(freq), float(amp), float(ph), shape, self.n_terms.shape[0], self.samplerate, float(self.duration)
            )

        return signal

    def export(self, path, bit_depth=16):
        write(self.scaled_signal, path, samplerate=self.samplerate, bit_depth=bit_depth)
