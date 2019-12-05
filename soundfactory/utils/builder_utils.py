from numpy import (
    pi,
    radians,
    sum as npsum,
    sin,
    int64,
    float64,
    asarray,
    round as npround,
    arange,
)
from numba import njit


@njit
def wn(n, freq):
    """ compute the angular frequency """
    return (2 * pi * n) * freq


@njit
def fourier_sum(x, coefficients, freq, phase, terms):
    """ sum the fourier series for the first nterms"""
    partial_sums = npsum(
        coefficients * sin(wn(terms, freq) * x + terms * radians(phase))
    )
    return partial_sums


@njit
def upsample_component(amp, phase, duration, times, coefficients, terms):
    period = [
        amp * fourier_sum(_t, coefficients, 1 / duration, phase, terms) for _t in times
    ]
    return asarray(period, dtype=float64)


def single_component(freq, duration, upsampled, samples):
    cycles = freq * duration
    indexes = (npround((arange(0, samples) * cycles)) % samples).astype(int64)
    return upsampled[indexes]
