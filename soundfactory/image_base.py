from PIL import Image
from scipy import linalg
import numpy as np
from .utils.signal import write
from .signal_builder import SignalBuilder

COLORSPACE = {
    "RGB": {"range": (0, 255), "channels": ("R", "G", "B")},
    "RGBA": {"range": (0, 255), "channels": ("R", "G", "B", "A")},
    "CMYK": {"range": (0, 100), "channels": ("C", "M", "Y", "K")}
}


def compress_image(img, k, mode="RGB"):
    img = np.asarray(img)
    n_channels = len(COLORSPACE[mode]["channels"])
    mode_min, mode_max = COLORSPACE[mode]["range"]
    rec_im = np.zeros(img.shape)
    for i in range(n_channels):
        layer = Channel.compress_svd(img[:, :, i], k)[0]
        rec_im[:, :, i] = layer
    return np.round(np.clip(rec_im, mode_min, mode_max)).astype(np.uint8)


class SVD:
    def __init__(self, data):
        data = np.asarray(data)
        M, N = data.shape
        self.U, self.s, self.V = linalg.svd(data)
        self.diagsvd = linalg.diagsvd(self.s, M, N)
        self.separability_index = self.s[0]**2 / sum(self.s**2)


class Channel:
    def __init__(self, data, name, fudge=5, components=None):
        self.data = np.asarray(data)
        self.name = name
        self._svd()
        self.fundamental = 2**fudge * self.svd.separability_index
        self.intervals = self._intervals()
        limit = min(self.data.shape) if not components else components
        self.amplitudes = self.calculate_amplitudes(limit)
        self.frequencies = self.fundamental * self.intervals
        self.frequencies = self.frequencies[:limit]
        
    def _svd(self):
        M, N = self.data.shape
        self.U, self.s, self.V = linalg.svd(self.data)
        self.diagsvd = linalg.diagsvd(self.s, M, N)
        self.separability_index = self.s[0]**2 / sum(self.s**2)
            
    @property
    def svd(self):
        return SVD(self.data)

    @classmethod
    def compress_svd(self, image, k):
        """
        https://medium.com/@rameshputalapattu/
        jupyter-python-image-compression-and-svd-an-interactive-exploration-703c953e44f6

        """
        
        U, s, V = linalg.svd(image, full_matrices=False)
        reduced_mat = np.dot(U[:, :k], np.dot(np.diag(s[:k]), V[:k, :]))
        return reduced_mat, s
    
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
                1 / 2*np.sqrt(((v_s + u_s).real + sign*(v_s - u_s).real)**2)
            )
        return amps


class SoundImage:
    def __init__(self, input_file, **kw):
        self.image = Image.open(input_file)
        self.channels = self._channels()

    def _channels(self):
        return [
            Channel(self.image.getchannel(band), band)
            for band in self.image.getbands()
        ]

    def compressed_image(self, k):
        return compress_image(self.image, k, self.image.mode)

    def signal_from_channel(self, channel, **kw):
        limit = kw.get("limit", min(channel.data.shape))
        waves = kw.get("waves", ['sine' for i in range(limit)])
        samplerate = kw.get("samplerate", 48000)
        duration = kw.get("duration", 1)
        return SignalBuilder(
            channel.frequencies[:limit],
            channel.amplitudes[:limit],
            waves,
            samplerate=samplerate,
            duration=duration
        )
 
    def stereo_signal(self, channels, **kw):
        c1, c2 = channels
        left = self.signal_from_channel(c1, **kw)
        right = self.signal_from_channel(c2, **kw)
        return left, right
    
    def export_audio(self, path, *signals, bit_depth=16):
        if len(signals) == 1:
            mono = signals[0]
            mono.scaled_signal /= np.max(np.abs(mono.signal), axis=0)
            signal = mono.scaled_signal
        elif len(signals) == 2:
            left, right = signals
            left.scaled_signal /= np.max(np.abs(left.signal), axis=0)
            right.scaled_signal /= np.max(np.abs(right.signal), axis=0)
            signal = np.array([left.scaled_signal, right.scaled_signal]).T
        else:
            return
        write(
            signal,
            path,
            samplerate=signals[0].samplerate,
            bit_depth=bit_depth
        )
    
