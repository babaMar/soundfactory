import time
from numpy import pi, arange, ndarray, round as npround

from soundfactory.cyutils import builder_utils as cy_builder_utils
from soundfactory.utils.builder_utils import (
    wn,
    fourier_sum,
    upsample_component,
    single_component
)
from soundfactory.settings.signal import B_N_COEFF_MAP
from soundfactory.constants import DEFAULT_SAMPLERATE
from tests.conftest import time_range

TIME_RANGE = time_range()


def test_angular_frequency(frequencies, n_max_range):
    for n, f in zip(n_max_range, frequencies):
        assert round(cy_builder_utils.wn(n, f), 2) == round(2 * pi * n * f, 2)


def test_vect_angular_frequency(frequencies, n_max_range):
    for n, f in zip(n_max_range, frequencies):
        terms = arange(1, n + 1)
        mask = cy_builder_utils.wn_arr(terms, f) == wn(terms, f)
        assert all(mask)


def test_fourier_sum(n_max_range, frequencies):
    for shape in B_N_COEFF_MAP.keys():
        for n, f in zip(n_max_range, frequencies):
            terms = arange(1, n + 1)
            coefficients = B_N_COEFF_MAP[shape](terms)
            partial_sums = \
                cy_builder_utils.fourier_sum(0.1, coefficients, f, 45., terms)
            assert isinstance(partial_sums, float)
            assert round(partial_sums, 12) \
                    == round(fourier_sum(0.1, coefficients, f, 45., terms), 12)


def test_upsample_component(n_max_range, frequencies):
    for shape in B_N_COEFF_MAP.keys():
        for n, f in zip(n_max_range, frequencies):
            terms = arange(1, n + 1)
            coefficients = B_N_COEFF_MAP[shape](terms)
            upsampled = cy_builder_utils.upsample_component(
                0.9, 45., 1., TIME_RANGE, coefficients, terms
            )
            assert isinstance(upsampled, ndarray)
            mask = npround(upsampled, 8) == \
                   npround(upsample_component(
                       0.9, 45., 1., TIME_RANGE, coefficients, terms), 8
                   )
            assert all(mask)


def test_single_component(n_max_range, frequencies):
    duration = 1.
    n_samples = int(duration * DEFAULT_SAMPLERATE)
    for shape in B_N_COEFF_MAP.keys():
        for n, f in zip(n_max_range, frequencies):
            start = time.time()
            terms = arange(1, n + 1)
            coefficients = B_N_COEFF_MAP[shape](terms)
            print(f'Testing {f} with shape {shape}')
            upsampled = cy_builder_utils.upsample_component(
                0.9, 45., duration, TIME_RANGE, coefficients, terms
            )
            print(f'Upsampling done in {round(time.time() - start, 2)} sec')
            start_new = time.time()
            sc = cy_builder_utils.single_component(
                    f, duration, upsampled, n_samples
            )
            print(f'Single Component in {round(time.time() - start_new, 2)} sec')
            assert isinstance(sc, ndarray)
            mask = sc == single_component(f, duration, upsampled, n_samples)
            assert all(mask)
