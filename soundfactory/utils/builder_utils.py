import numpy as np
from numba import njit


@njit
def wn(n, freq):
    """ compute the angular frequency """
    return (2 * np.pi * n) * freq


@njit
def fourier_sum(x, coefficients, freq, phase, terms):
    """ sum the fourier series for the first nterms"""
    partial_sums = np.sum(
        coefficients * np.sin(wn(terms, freq) * x + terms * np.radians(phase))
    )
    return partial_sums


@njit
def upsample_component(amp, phase, duration, times, coefficients, terms):
    period = [
        amp * fourier_sum(_t, coefficients, 1 / duration, phase, terms) for _t in times
    ]
    return np.asarray(period, dtype=np.float64)


def single_component(freq, duration, upsampled, samples):
    cycles = freq * duration
    indexes = (np.round((np.arange(0, samples) * cycles)) % samples).astype(np.int64)
    return upsampled[indexes]
