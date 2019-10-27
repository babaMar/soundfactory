from soundfactory.utils.scale import build_24_tet_scale_by_sequence
import numpy as np
from bisect import bisect_left
from soundfactory.constants import _24_TET_SCALE_INIT
from matplotlib import ticker
from soundfactory.utils.helpers import indexes_above_threshold

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


def remove_close_values_on_log_scale(values, tolerance=0.1):
    """
    Params
    ------
    values -- array-like of floats
    tolerance (float) -- for a given x remove all y:
                         x - tolerance*x < y < x + tolerance*x


    Example
    -------
    tolerance = 0.1
    [1, 1.01, 15, 14, 1.11] -> [1, 15, 1.11]

    """
    values = list(values)
    for i, x in enumerate(values):
        d = abs(tolerance * x)
        remaining_values = values[i + 1:]
        for y in remaining_values:
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


def sparse_major_freqs(freqs, amps, threshold=0.1, close_tolerance=0.1):
    idx = indexes_above_threshold(amps, threshold=threshold)
    freqs, amps = freqs[idx], amps[idx]
    
    idx = np.argsort(-amps)
    freqs, amps = freqs[idx], amps[idx]
    return remove_close_values_on_log_scale(freqs, tolerance=close_tolerance)



