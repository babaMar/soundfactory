import numpy as np
from math import log

BASE = 2
CENTS_PER_OCTAVE = 1200
CENT = pow(BASE, 1. / CENTS_PER_OCTAVE)
SEMITONE_CENTS = 100
QUARTERTONE_CENTS = 50


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

