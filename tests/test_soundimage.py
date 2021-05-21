from soundfactory.image_base import (
    COLORSPACE,
    SoundImage,
    Channel
)
import numpy as np
from PIL import ImageChops
from itertools import combinations
from pathlib import Path


def test_rgb(rgb_file):
    sim = SoundImage(rgb_file)
    assert sim.image.mode == "RGB"


def test_rgba(rgba_file):
    sim = SoundImage(rgba_file)
    assert sim.image.mode == "RGBA"


def test_grey(grey_file):
    sim = SoundImage(grey_file)
    assert sim.image.mode == "L"


def test_cmyk(cmyk_file):
    sim = SoundImage(cmyk_file)
    assert sim.image.mode == "CMYK"


def test_class(rgb_file):
    channels = COLORSPACE["RGB"]["channels"]
    sim = SoundImage(rgb_file, resolution=160)
    assert isinstance(sim.channels, dict)
    assert sorted(sim.bands) == sorted(channels)

    for band in channels:
        assert band in sim.channels
        channel = sim.channels[band]
        assert isinstance(channel, Channel)
        assert isinstance(channel.data, np.ndarray)
        assert channel.name == band

    rec_im = sim.reconstructed()
    diff = ImageChops.difference(sim.image, rec_im)
    # (Almost) all pixels are black
    assert diff.histogram().count(0) >= 762

    sim = SoundImage(rgb_file, resolution=10)
    folder = rgb_file.split('/')[-1].split('.')[0]
    # Mono
    l_band = "R"
    sim.export_audio(l_band)
    assert Path(
        Path(__file__).parent.parent / folder / str(l_band + '.wav')
    ).is_file()
    # Stereo
    for couple in combinations(channels, 2):
        l, r = couple
        sim.export_audio(l, r)
        assert Path(
            Path(__file__).parent.parent / folder / str(l + r + '.wav')
        ).is_file()
