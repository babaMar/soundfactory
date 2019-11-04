from .utils.signal import (get_envelope,
                           load_audio)
from .utils.helpers import spectrum
from .settings.logging_settings import signal_log


class Signal:
    CH = 'ch'
    CH1 = 'ch1'
    CH2 = 'ch2'
    ENVELOPE_SUFFIX = '_envelope'
    FREQUENCIES = 'freqs'
    POWERS = 'pws'
    FFT_SUFFIX = '_fft'
    CHANNELS = dict()
    SPECTRA = dict()

    def __init__(self, input_file, with_envelope=False):
        self.MONO = False
        self.CALCULATE_ENVELOPE = with_envelope
        self.ENVELOPES = dict()
        self.CHANNELS = dict()
        self.SPECTRA = dict()
        self.signal = None
        self.sampling_rate = None
        self.duration = 0
        self._load_audio(input_file)
        self._calculate_envelope()
        self._calculate_fft()

    @staticmethod
    def _is_mono(signal_arr):
        return len(signal_arr.shape) == 1

    def _load_audio(self, input_file):
        self.signal, self.sampling_rate = load_audio(input_file)

        if self._is_mono(self.signal):
            self.MONO = True
            self.CHANNELS.update({self.CH1: self.signal})
        else:
            self.CHANNELS.update(
                {self.CH + str(i + 1): self.signal[:, i]
                 for i in range(len(self.signal.shape))
                 }
            )

        self.duration = len(self.CHANNELS[self.CH1]) / self.sampling_rate
        signal_log.info("Loaded {t:.2f} seconds from {c} audio".format(
            t=self.duration, c="mono" if self.MONO else "stereo"
        ))

    def _calculate_envelope(self):
        if self.CALCULATE_ENVELOPE:
            signal_log.info("Calculating envelope%s"
                            % ('' if self.MONO else 's'))
            # Volume envelopes
            self.ENVELOPES.update(
                {ch + self.ENVELOPE_SUFFIX: get_envelope(sig)
                 for ch, sig in self.CHANNELS.items()
                 }
            )

    def _calculate_fft(self):
        for ch, sig in self.CHANNELS.items():
            res = dict()
            res[self.FREQUENCIES], res[self.POWERS] = \
                spectrum(sig, self.sampling_rate)
            self.SPECTRA.update({ch + self.FFT_SUFFIX: res})
