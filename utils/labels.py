from utils.scale import build_24_tet_scale_by_sequence
import numpy as np
from bisect import bisect_left
from constants import _24_TET_SCALE_INIT
from matplotlib import ticker


note_hz_24_tet = build_24_tet_scale_by_sequence(
    list(_24_TET_SCALE_INIT.keys())[-1],
    list(_24_TET_SCALE_INIT.values())[-1]
)
hz_note_24_tet = {v: k for k, v in note_hz_24_tet.items()}


def find_closest(sorted_list, x):
    pos = bisect_left(sorted_list, x)
    if pos == 0:
        return sorted_list[0]
    if pos == len(sorted_list):
        return sorted_list[-1]
    before = sorted_list[pos - 1]
    after = sorted_list[pos]
    if after - x < x - before:
        closest = after
    else:
        closest = before
    return closest


def remove_too_close(values, thr=0.1):
    """ remove close elements in values following their position in values"""
    values = list(values)
    for i, x in enumerate(values):
        d = thr * x
        left_values = list(values[i+1:])
        for y in left_values:
            if abs(x - y) < d:
                values.remove(y)
    return values


def hz_to_note(x):
    return hz_note_24_tet[
        find_closest(sorted(hz_note_24_tet.keys()), x)
    ]


@ticker.FuncFormatter
def log_khz_formatter(hz, pos):
    return '{:g}'.format(hz / 1000)


def above_thr_indexes(amps, thr=0.1):
    amps = np.array(amps)
    return np.where(amps > thr * amps.max())[0]


def sparse_major_freqs(freqs, amps, thr=0.1, close_thr=0.1):
    idx = above_thr_indexes(amps, thr=thr)
    freqs, amps = freqs[idx], amps[idx]
    
    idx = np.argsort(-amps)
    freqs, amps = freqs[idx], amps[idx]
    return remove_too_close(freqs, thr=close_thr)



