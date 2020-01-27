from PIL import Image
from scipy import linalg
import numpy as np
from itertools import combinations
from pathlib import Path

from .utils.signal import write
from .signal_builder import SignalBuilder

COLORSPACE = {
    "RGB": {"range": (0, 255), "channels": ("R", "G", "B")},
    "RGBA": {"range": (0, 255), "channels": ("R", "G", "B", "A")},
    "CMYK": {"range": (0, 100), "channels": ("C", "M", "Y", "K")},
}


class Channel:
    def __init__(self, data, name, fudge=5, components=None, **kwargs):
        self.data = np.asarray(data)
        self.name = name
        self._svd()
        self.fundamental = 2 ** fudge * self.separability_index
        self.intervals = self._intervals()
        self.resolution = min(self.data.shape) if not components else components
        self.amplitudes = self.calculate_amplitudes(self.resolution)
        self.frequencies = self.fundamental * self.intervals[: self.resolution]
        self.signal = None

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
        self.eigUvalues, self.eigUvectors = linalg.eig(self.U)
        self.eigVvalues, self.eigVvectors = linalg.eig(self.V)
        for row_idx in range(limit):
            v = self.eigVvalues * self.eigVvectors[row_idx]
            u = self.eigUvalues * self.eigUvectors[row_idx]
            v_s, u_s = sum(v), sum(u)

            sign = np.sign(np.angle(v_s + u_s)) * np.sign(np.angle(v_s - u_s,))
            amps.append(
                1 / 2 * np.sqrt(((v_s + u_s).real + sign * (v_s - u_s).real) ** 2)
            )
        return amps

    def audio_signal(self, **kw):
        waves = kw.get("waves", ["sine" for _ in range(self.resolution)])
        samplerate = kw.get("samplerate", 48000)
        duration = kw.get("duration", 1)
        s = SignalBuilder(
            self.frequencies,
            self.amplitudes,
            waves,
            samplerate=samplerate,
            duration=duration,
        )
        return s

    def export_audio(self, fname):
        self.signal.export('_'.join([fname, self.name]) + '.wav')


class SoundImage:
    def __init__(self, input_file, **kw):
        self.name = str(input_file).split('/')[-1].split('.')[0]
        self.image = Image.open(input_file)
        self.channels = self._channels(**kw)
        self.signals = None
        
    def _channels(self, **kw):
        return {
            band: Channel(
                self.image.getchannel(band), band, **kw)
            for band in self.image.getbands()
        }

    def reconstructed(self, resolution):
        rec_im = np.zeros(self.image.shape)
        for i, channel in enumerate(self.channels.values()):
            rec_im[:, :, i] = channel.reconstruct(resolution)
        return Image.fromarray(rec_im)

    def stereo_signals(self, **kw):
        res = dict()
        for band, channel in self.channels.items():
            if channel.signal is None:
                channel.signal = channel.audio_signal(**kw)
        for c1, c2 in combinations(self.channels.keys(), 2):
            left = self.channels[c1].signal
            right = self.channels[c2].signal
            res[c1 + c2] = (left, right)
        self.signals = res
        return res

    def export_audio(self, path='./', bit_depth=16, **kw):
        if self.signals is None:
            self.stereo_signals(**kw)
        for pair, channels in self.signals.items():
            left, right = channels
            signal = np.array([left.scaled_signal, right.scaled_signal]).T
            assert left.samplerate == right.samplerate
            outpath = Path(path) / self.name / "".join((pair, '.wav'))
            outpath.parent.mkdir(parents=True, exist_ok=True)
            write(signal, str(outpath), samplerate=left.samplerate, bit_depth=bit_depth)
