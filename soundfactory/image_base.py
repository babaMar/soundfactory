from PIL import Image
from scipy import linalg
import numpy as np

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


class Channel:
    def __init__(self, data, name):
        self.data = np.asarray(data)
        self.name = name

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
