from soundfactory.image_base import SoundImage


def test_rgb(rgb_file):
    sim = SoundImage(rgb_file)
    assert sim.image.mode == "RGB"
    assert all(x in sim.svd for x in sim.image.getbands())


def test_rgba(rgba_file):
    sim = SoundImage(rgba_file)
    assert sim.image.mode == "RGBA"
    assert all(x in sim.svd for x in sim.image.getbands())


def test_grey(grey_file):
    sim = SoundImage(grey_file)
    assert sim.image.mode == "L"
    assert all(x in sim.svd for x in sim.image.getbands())


def test_cmyk(cmyk_file):
    sim = SoundImage(cmyk_file)
    assert sim.image.mode == "CMYK"
    assert all(x in sim.svd for x in sim.image.getbands())

