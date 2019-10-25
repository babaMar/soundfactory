BASE = 2
CENTS_PER_OCTAVE = 1200
CENT = pow(BASE, 1. / CENTS_PER_OCTAVE)
SEMITONE_CENTS = 100
QUARTERTONE_CENTS = 50

QUARTER_TONE_SHARP_SYMBOL = '𝄲'
SHARP_SYMBOL = '#'
QUARTER_TONE_FLAT_SYMBOL = '𝄳'

A_SUB_SUB_CONTRA_FREQ = 13.75
_24_TET_SCALE_INIT = {'A-1': A_SUB_SUB_CONTRA_FREQ}

SEQUENCE_24 = (
    'C', 'C𝄲', 'C#',
    'D𝄳', 'D', 'D𝄲', 'D#',
    'E𝄳', 'E', 'E𝄲',
    'F', 'F𝄲', 'F#',
    'G𝄳', 'G', 'G𝄲', 'G#',
    'A𝄳', 'A', 'A𝄲', 'A#',
    'B𝄳', 'B', 'B𝄲'
)
SYMBOLS_24 = ('', '𝄲', '#', '𝄳')

MAX_16_BIT_VALUE = 2**15 - 1
BYTE_PER_16_BIT = 2

DEFAULT_SAMPLERATE = 44100
