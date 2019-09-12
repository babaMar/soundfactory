import re
from utils.helpers import freq_at_n_quartertones
from constants import SEQUENCE_24, SYMBOLS_24


def next_tone(tone):
    tone = tone.upper()
    A = ord("A")
    if ord(tone) >= (A + 7):
        raise ValueError("tone must be between A and G")
    return chr((ord(tone) + 1 - A) % 7 + A)


def next_subtone(tone, sub):
    N = 2 if tone.upper() in ("E", "B") else 4
    indx = (SYMBOLS_24.index(sub) + 1) % N
    return SYMBOLS_24[indx]


def label_info_re(label):
    gex = "([A-Ga-g])(-?\d+)([{}]|)".format("".join(SYMBOLS_24))
    try:
        tone, octave, sub = re.match(gex, label).groups()
        return tone.upper(), octave, sub
    except AttributeError:
        raise ValueError("{} is not a valid tone label".format(label))


def label_info(label):
    octave = label[1:].rstrip("".join(SYMBOLS_24))
    return label[0], octave, label[len(octave) + 1:]


def next_label(label):
    tone, octave, subtone = label_info_re(label)
    new_subtone = next_subtone(tone, subtone)
    syms = SYMBOLS_24[-1:] + SYMBOLS_24[:-1]  # right shift
    old, new = syms.index(subtone), syms.index(new_subtone)
    new_tone = next_tone(tone) if new < old else tone
    new_octave = str(int(octave) + 1) \
        if "".join([tone, subtone]) == "B𝄲" else octave
    return new_tone.upper() + new_octave + new_subtone


def next_label_by_sequence(label):
    tone, octave, subtone = label_info_re(label)
    idx = SEQUENCE_24.index(tone + subtone)
    new_idx = (idx + 1) % len(SEQUENCE_24)
    new_tone, new_subtone = SEQUENCE_24[new_idx][:1], SEQUENCE_24[new_idx][1:]
    new_octave = str(int(octave) + 1) if idx > new_idx else octave
    return new_tone + new_octave + new_subtone


def next_freq(freq):
    return round(freq_at_n_quartertones(freq, 1), 2)


def build_24_tet_scale(init_label, init_freq, max_octave=10):
    label, freq = init_label, init_freq
    scale = [(label, freq)]
    last_label = "G" + str(max_octave)
    while label != last_label:
        scale.append((next_label(label), next_freq(freq)))
        label, freq = scale[-1][0], scale[-1][1]
    return dict(scale)


def build_24_tet_scale_by_sequence(init_label, init_freq, max_octave=10):
    label, freq = init_label, init_freq
    scale = [(label, freq)]
    last_label = "G" + str(max_octave)
    while label != last_label:
        scale.append((next_label_by_sequence(label), next_freq(freq)))
        label, freq = scale[-1][0], scale[-1][1]
    return dict(scale)

