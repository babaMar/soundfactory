from PIL import Image
from scipy import linalg
import numpy as np


class SoundImage:
    def __init__(self, input_file, **kw):
        self.image = Image.open(input_file)
        self.svd = self._svd()

    def _svd(self):
        bands, channels = self.image.getbands(), self.image.split()
        out = {}
        M, N = self.image.size
        for band, channel in zip(bands, channels):
            U, s, V = linalg.svd(np.asarray(channel))
            diagsvd = linalg.diagsvd(s, M, N)
            out[band] = (U, s, V, diagsvd)
        return out
