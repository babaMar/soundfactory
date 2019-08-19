import numpy as np
import scipy.signal as signal

SAMPLES = 44100


def time_range(start=0., end=1.):
    return np.linspace(start, end, SAMPLES, endpoint=False)


def sine_wave(freq):
    t = time_range()
    sig = np.sin(2 * np.pi * freq * t)
    return sig


def square_wave(freq):
    t = time_range()
    sig = signal.square(2 * np.pi * freq * t)
    return sig


def sawtooth_wave(freq):
    t = time_range()
    sig = signal.sawtooth(2 * np.pi * freq * t)
    return sig


def triangle_wave(freq):
    t = time_range()
    phase_shift = np.pi / 2.  # a phase shift of 90° is needed to have signal=0. at t=0.
    sig = signal.sawtooth(2 * np.pi * freq * t + phase_shift, width=0.5)
    return sig
