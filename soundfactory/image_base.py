from PIL import Image
from scipy import linalg
import numpy as np
from pathlib import Path
from os import getenv
from .utils.helpers import load_cache, builder_cache_key, cache_it
from .utils.signal import write_stereo
from .signal_builder import SignalBuilder
from .settings.logging_settings import get_logger


logger = get_logger(__name__)
logger.setLevel(getenv("APP_LOG_LEVEL", "DEBUG"))

COLORSPACE = {
    "RGB": {"range": (0, 255), "channels": ("R", "G", "B")},
    "RGBA": {"range": (0, 255), "channels": ("R", "G", "B", "A")},
    "CMYK": {"range": (0, 100), "channels": ("C", "M", "Y", "K")},
}
BUILDER_CACHE = load_cache()


class Channel:
    def __init__(self, data, name):
        self.data = np.asarray(data)
        self.name = name
        self._svd()
        logger.debug(
            '<{} band> Calculating eigenvalues and eigenvectors for U...'
            .format(self.name)
        )
        self.eigUvalues, self.eigUvectors = linalg.eig(self.U)
        logger.debug(
            '<{} band> Calculating eigenvalues and eigenvectors for V...'
            .format(self.name)
        )
        self.eigVvalues, self.eigVvectors = linalg.eig(self.V)
        self.intervals = self._intervals()

    def _svd(self):
        M, N = self.data.shape
        self.U, self.s, self.V = linalg.svd(self.data)
        self.diagsvd = linalg.diagsvd(self.s, M, N)
        self.separability_index = self.s[0] ** 2 / sum(self.s ** 2)

    def reconstruct(self, resolution):
        reduced_mat = np.dot(
            self.U[:, :resolution],
            np.dot(np.diag(self.s[:resolution]), self.V[:resolution, :]),
        )
        return np.asarray(reduced_mat, dtype="uint8")

    def _intervals(self):
        return self.s[0] / self.s

    def calculate_amplitudes(self, limit):
        amps = list()
        for row_idx in range(limit):
            v = self.eigVvalues * self.eigVvectors[row_idx]
            u = self.eigUvalues * self.eigUvectors[row_idx]
            v_s, u_s = sum(v), sum(u)

            sign = np.sign(np.angle(v_s + u_s)) * np.sign(np.angle(v_s - u_s,))
            amps.append(
                1 / 2 * np.sqrt(((v_s + u_s).real + sign * (v_s - u_s).real) ** 2)
            )
        return amps

    def audio_signal(self, resolution, fudge, **kw):
        fundamental = 2**fudge * self.separability_index
        amplitudes = self.calculate_amplitudes(resolution)
        frequencies = fundamental * self.intervals[:resolution]
        phases = kw.get("phases", None)
        n_max = kw.get("n_max", 1000)
        waves = kw.get("waves", ["sine" for _ in range(resolution)])
        samplerate = kw.get("samplerate", 48000)
        duration = kw.get("duration", 1)
        s = self._cached_builder(
            frequencies,
            amplitudes,
            waves,
            phases,
            n_max,
            duration,
            samplerate
        )
        return s

    @staticmethod
    @cache_it(BUILDER_CACHE, builder_cache_key)
    def _cached_builder(
            freqs, amps, waves, phases, n_max, samplerate, duration):
        return SignalBuilder(
            freqs, amps, waves, phases,
            n_max, samplerate, duration
        )


class SoundImage:
    def __init__(self, input_file):
        self.name = str(input_file).split('/')[-1].split('.')[0]
        self.image = Image.open(input_file)
        self.width, self.height = self.image.size
        self.channels = self._channels()
        self.bands = tuple(self.channels.keys())
        
    def _channels(self):
        return {
            band: Channel(
                self.image.getchannel(band), band)
            for band in self.image.getbands()
        }

    def reconstructed(self, resolution):
        rec_im = np.zeros(
            (self.height, self.width, len(self.bands)), dtype="uint8"
        )
        for i, channel in enumerate(self.channels.values()):
            rec_im[:, :, i] = channel.reconstruct(resolution)
        return Image.fromarray(rec_im)

    def export_audio(self, left_band, right_band=None, resolution=10,
                     fudge=5, path="./", bit_depth=16, **kw):
        outpath = Path(path) / self.name / "".join(
            (left_band, right_band or "", '.wav'))
        outpath.parent.mkdir(parents=True, exist_ok=True)
        left_builder = self.channels.get(left_band).audio_signal(
                resolution, fudge, **kw
            )
        if right_band is None:
            left_builder.export(str(outpath), bit_depth=bit_depth)
        else:
            right_builder = self.channels.get(right_band).audio_signal(
                resolution, fudge, **kw
            )
            assert left_builder.samplerate == right_builder.samplerate
            write_stereo(
                left_builder.scaled_signal, right_builder.scaled_signal,
                str(outpath),
                bit_depth=bit_depth,
                samplerate=left_builder.samplerate
            )
