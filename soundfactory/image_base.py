from PIL import Image
from scipy import linalg
import numpy as np


class SVD:
    def __init__(self, data):
        M, N = np.asarray(data).shape
        self.U, self.s, self.V = linalg.svd(data)
        self.diagsvd = linalg.diagsvd(self.s, M, N)


class Channel:
    def __init__(self, data, name):
        self.data = np.asarray(data)
        self.name = name

    @property
    def svd(self):
        return SVD(self.data)

    
class SoundImage:
    def __init__(self, input_file, **kw):
        self.image = Image.open(input_file)
        self.channels = self._channels()

    def _channels(self):
        return [
            Channel(self.image.getchannel(band), band)
            for band in self.image.getbands()
        ]
