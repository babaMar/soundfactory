import pickle
from pathlib import Path
import hashlib

import numpy as np
from math import log

from soundfactory.constants import (
    CENTS_PER_OCTAVE,
    BASE,
    SEMITONE_CENTS,
    QUARTERTONE_CENTS,
)
from soundfactory.settings.config import BUILDER_CACHE_PATH
from soundfactory.settings.logging_settings import helperlog


def cents_from_freq_ratio(upper_tone, lower_tone):
    freq_ratio = upper_tone / lower_tone
    return CENTS_PER_OCTAVE * log(freq_ratio, BASE)


def freq_at_n_semitones(tone_freq, n):
    cents_interval = n * SEMITONE_CENTS
    return tone_freq * pow(2, cents_interval / CENTS_PER_OCTAVE)


def freq_at_n_quartertones(tone_freq, n):
    cents_interval = n * QUARTERTONE_CENTS
    return tone_freq * pow(2, cents_interval / CENTS_PER_OCTAVE)


def above_thr_mask(a, threshold=.1):
    """a is a numpy.array"""
    peak_threshold = threshold * a.max()
    return a >= peak_threshold


def indexes_above_threshold(a, threshold=0.1):
    a = np.array(a)
    return np.where(above_thr_mask(a, threshold=threshold))[0]


def spectrum(signal, samplerate):
    n = len(signal)
    fft = np.fft.rfft(signal)
    freqs = np.fft.fftfreq(n, d=1/samplerate)
    freqs_mask = np.where(freqs >= 0)[0]
    pws = 2 * ((np.abs(fft) / n) ** 2)  # amps = 2 * (np.abs(fft) / n)
    return freqs[freqs_mask], pws[freqs_mask]


def progress_bar(
        iteration,
        total,
        prefix='',
        suffix='',
        decimals=1,
        length=100,
        fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals
                                  in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    x = 100 * (iteration / total)
    percent = round(x, decimals)
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r{prefix} |{bar}| {percent}% {suffix}'.format(
        prefix=prefix,
        bar=bar,
        percent=percent,
        suffix=suffix
    ), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def progress_time(
        total_time,
        elapsed=0,
        prefix='',
        suffix='',
        decimals=1,
        length=100,
        fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals
                                  in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """

    filled_length = int(length * elapsed // total_time)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r{prefix} |{bar}| {left} {suffix}'.format(
        prefix=round(elapsed),
        bar=bar,
        left=round(total_time-elapsed),
        suffix=suffix
    ), end='\r')


def load_cache(path=BUILDER_CACHE_PATH):
    try:
        with open(path, 'rb') as f:
            cache = pickle.load(f)
    except FileNotFoundError:
        cache = {}
    return cache


def save_cache(cache, path=BUILDER_CACHE_PATH):
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(cache, f, protocol=pickle.HIGHEST_PROTOCOL)
        helperlog.debug(f'Cache saved')


def builder_cache_key(freqs, amps, waves, phases, n_max, samplerate, duration):
    if phases is None:
        phases = [0] * len(freqs)
    key = sorted(zip(freqs, amps, waves, phases), key=lambda x: x[0])
    key += [n_max, samplerate, duration]
    key = '_'.join([str(k) for k in key])
    return key


def single_component_cache_key(self, freq, amp, wave, phase, n_max, samplerate, duration):
    # To use on a class method
    key = [freq, amp, wave, phase, n_max, samplerate, duration]
    key = '_'.join([str(k) for k in key])
    return key


def cache_it(cache, key_encoder, path=BUILDER_CACHE_PATH):
    def decorator(func):
        def wrapped(*args):
            key = key_encoder(*args)
            val = cache.get(key)
            if val is None:
                helperlog.debug(f'Value for {key} not found in Cache')
                val = func(*args)
                helperlog.debug(f'Setting {val} for {key} in Cache')
                cache[key] = val
                save_cache(cache, path)
            return val
        return wrapped
    return decorator
