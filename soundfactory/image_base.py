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


def default_amp_calculator(
        u_values, v_values, u_vecs, v_vecs, limit):
    amps = list()
    for row_idx in range(limit):
        u = u_values * u_vecs[row_idx]
        v = v_values * v_vecs[row_idx]
        v_s, u_s = sum(v), sum(u)
        sign = np.sign(np.angle(v_s + u_s)) * np.sign(np.angle(v_s - u_s,))
        amps.append(
            1 / 2 * np.sqrt(((v_s + u_s).real + sign * (v_s - u_s).real) ** 2)
        )
    return amps


class Channel:
    def __init__(
            self, data, name, resolution, amplitude_calculator=default_amp_calculator,
    ):
        self.data = np.asarray(data)
        self.name = name
        self.resolution = resolution
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
        self.amp_calc = amplitude_calculator

    def _svd(self):
        M, N = self.data.shape
        self.U, self.s, self.V = linalg.svd(self.data)
        self.diagsvd = linalg.diagsvd(self.s, M, N)
        self.separability_index = self.s[0] ** 2 / sum(self.s ** 2)

    def reconstruct(self):
        reduced_mat = np.dot(
            self.U[:, :self.resolution],
            np.dot(np.diag(self.s[:self.resolution]), self.V[:self.resolution, :]),
        )
        return np.asarray(reduced_mat, dtype="uint8")

    def _intervals(self):
        return self.s[0] / self.s

    def calculate_amplitudes(self, limit):
        return self.amp_calc(
            self.eigUvalues, self.eigVvalues,
            self.eigUvectors, self.eigVvectors,
            limit
        )

    def audio_signal(self, fudge, **kw):
        fundamental = 2**fudge * self.separability_index
        amplitudes = self.calculate_amplitudes(self.resolution)
        frequencies = fundamental * self.intervals[:self.resolution]
        phases = kw.get("phases", None)
        n_max = kw.get("n_max", 1000)
        waves = kw.get("waves", ["sine" for _ in range(self.resolution)])
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
    def __init__(
            self, input_file, amplitude_calculator=default_amp_calculator, resolution=10
    ):
        self.name = str(input_file).split('/')[-1].split('.')[0]
        self.image = Image.open(input_file)
        self.amp_calc = amplitude_calculator
        self.resolution = resolution
        self.width, self.height = self.image.size
        self.channels = self._channels()
        self.bands = tuple(self.channels.keys())

    def _channels(self):
        return {
            band: Channel(
                self.image.getchannel(band),
                band,
                self.resolution,
                amplitude_calculator=self.amp_calc,
            )
            for band in self.image.getbands()
        }

    def convert(self):
        # a possible mapping between Image space and Sound space might be formulated by associating the R, G, B
        # representation to a 3-band subdivision of the audible frequency spectrum. As the visualised color of a certain
        # pixel is the combination of the channel values, one can imagine that the associated sound to that pixel is the
        # combination of an equivalent audible-band value. As for each color band we find 256 possible values, it seems
        # reasonable to divide the entire audible spectrum in 3 bands (corresponding to the R, G, B channels) each made
        # of 256 subdivisions. Basically, one assumes that the final signal is made of the sum
        # of a low (R), mid (G), and high (B) contribution. To associate the R/G/B channel to a low/mid/high channel,
        # seems reasonable to divide the low/mid/high band for 256, and obtain a relative frequency increment (d) size
        # in Hz. So, assuming the common low/mid/high frequency ranges:
        # d_low = (low_max - low_min) / 256, d_mid = (mid_max - mid_min)/256, d_high = (high_max - high_min)/256
        # So that, to map a single pixel [i, j] value to a frequency value one can do:
        # pixel_hz = R[i, j] * d_low + (G[i, j] * d_mid + mid_min) + (B[i, j] * d_high + high_min)
        # Now, as the eye grasps the picture features rather than the single pixels, it seems also reasonable to cluster
        # pixels together before attempting any conversion of sort. So an exemplified version of this algorithm might be
        # 1. Analyse the image to identify the features
        # 1a. Order them in terms of "importance"?
        # 2. group the pixels belonging to each feature and associate a duration according to the feature population
        # 3. perform a weighted average (luminosity?) on the cluster
        # 4. perform the transformation above for each cluster
        # 4.a According to the order and duration, concatenate the feature extracted sounds together
        pass

    def reconstructed(self):
        rec_im = np.zeros(
            (self.height, self.width, len(self.bands)), dtype="uint8"
        )
        for i, channel in enumerate(self.channels.values()):
            rec_im[:, :, i] = channel.reconstruct()
        return Image.fromarray(rec_im)

    def export_audio(self, left_band, right_band=None,
                     fudge=5, path=None, bit_depth=16, **kw):
        if path is None:
            outpath = Path("./") / self.name / "".join(
                (left_band, right_band or "", '.wav'))
        else:
            if not path.endswith(".wav"):
                path = path + ".wav"
            outpath = Path(path)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        left_builder = self.channels.get(left_band).audio_signal(fudge, **kw)
        logger.info("saving audio to {}".format(str(outpath)))
        if right_band is None:
            left_builder.export(str(outpath), bit_depth=bit_depth)
        else:
            right_builder = self.channels.get(right_band).audio_signal(fudge, **kw)
            assert left_builder.samplerate == right_builder.samplerate
            write_stereo(
                left_builder.scaled_signal, right_builder.scaled_signal,
                str(outpath),
                bit_depth=bit_depth,
                samplerate=left_builder.samplerate
            )
