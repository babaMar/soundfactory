import matplotlib.pyplot as plt
from itertools import cycle
import matplotlib.font_manager as mfm
from soundfactory.constants import QUARTER_TONE_FLAT_SYMBOL
from fontTools.ttLib import TTFont

FONT_INFO = [
    (f.fname, f.name) for f in mfm.fontManager.ttflist
    if 'Symbol' not in f.name]


def find_font_path_name(char):
    def _char_in_font(unicode_char, font):
        for cmap in font['cmap'].tables:
            if cmap.isUnicode():
                if ord(unicode_char) in cmap.cmap:
                    return True
        return False

    for font in FONT_INFO:
        if _char_in_font(char, TTFont(font[0])):
            return font[0], font[1]
    return None, None


FONT_PATH, FONT_NAME = find_font_path_name(QUARTER_TONE_FLAT_SYMBOL)
FONT_PROP = mfm.FontProperties(size=20) if not FONT_PATH \
    else mfm.FontProperties(size=20, fname=FONT_PATH)

plt.rc('text', usetex=False)
plt.rcParams['legend.numpoints'] = 1
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['font.size'] = 22
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['font.family'] = 'serif'


def get_inches(p_width, p_height, dpi=100):
    x, y = p_width / dpi, p_height / dpi
    return round(x, 1), round(y, 1)


# Screen sizes
try:
    window = plt.get_current_fig_manager().window
except AttributeError:
    # travis runs with 'headless' framework, which is non-interactive
    screen_y = 400
    screen_x = 600
else:
    screen_y = window.winfo_screenheight()  # pixels
    screen_x = window.winfo_screenwidth()
    plt.close()

figure_size_single = (12., 7.)
figure_size_double = (12., 12.)
figure_size_full = get_inches(screen_x, screen_y)


colors = cycle(['b', 'r', 'g', 'c', 'm'])


TONE_FREQ_MAP = {"C0": 16.35,
                 "C0#": 17.32,
                 "D0": 18.35,
                 "D0#": 19.45,
                 "E0": 20.60,
                 "F0": 21.83,
                 "F0#": 23.12,
                 "G0": 24.50,
                 "G0#": 25.96,
                 "A0": 27.50,
                 "A0#": 29.14,
                 "B0": 30.87,
                 "C1": 32.70,
                 "C1#": 34.65,
                 "D1": 36.71,
                 "D1#": 38.89,
                 "E1": 41.20,
                 "F1": 43.65,
                 "F1#": 46.25,
                 "G1": 49.00,
                 "G1#": 51.91,
                 "A1": 55.00,
                 "A1#": 58.27,
                 "B1": 61.74,
                 "C2": 65.41,
                 "C2#": 69.30,
                 "D2": 73.42,
                 "D2#": 77.78,
                 "E2": 82.41,
                 "F2": 87.31,
                 "F2#": 92.50,
                 "G2": 98.00,
                 "G2#": 103.83,
                 "A2": 110.00,
                 "A2#": 116.54,
                 "B2": 123.47,
                 "C3": 130.81,
                 "C3#": 138.59,
                 "D3": 146.83,
                 "D3#": 155.56,
                 "E3": 164.81,
                 "F3": 174.61,
                 "F3#": 185.00,
                 "G3": 196.00,
                 "G3#": 207.65,
                 "A3": 220.00,
                 "A3#": 233.08,
                 "B3": 246.94,
                 "C4": 261.63,
                 "C4#": 277.18,
                 "D4": 293.66,
                 "D4#": 311.13,
                 "E4": 329.63,
                 "F4": 349.23,
                 "F4#": 369.99,
                 "G4": 392.00,
                 "G4#": 415.30,
                 "A4": 440.00,
                 "A4#": 466.16,
                 "B4": 493.88,
                 "C5": 523.25,
                 "C5#": 554.37,
                 "D5": 587.33,
                 "D5#": 622.25,
                 "E5": 659.26,
                 "F5": 698.46,
                 "F5#": 739.99,
                 "G5": 783.99,
                 "G5#": 830.61,
                 "A5": 880.00,
                 "A5#": 932.33,
                 "B5": 987.77,
                 "C6": 1046.50,
                 "C6#": 1108.73,
                 "D6": 1174.66,
                 "D6#": 1244.51,
                 "E6": 1318.51,
                 "F6": 1396.91,
                 "F6#": 1479.98,
                 "G6": 1567.98,
                 "G6#": 1661.22,
                 "A6": 1760.00,
                 "A6#": 1864.66,
                 "B6": 1975.53,
                 "C7": 2093.00,
                 "C7#": 2217.46,
                 "D7": 2349.32,
                 "D7#": 2489.02,
                 "E7": 2637.02,
                 "F7": 2793.83,
                 "F7#": 2959.96,
                 "G7": 3135.96,
                 "G7#": 3322.44,
                 "A7": 3520.00,
                 "A7#": 3729.31,
                 "B7": 3951.07,
                 "C8": 4186.01,
                 "C8#": 4434.92,
                 "D8": 4698.64,
                 "D8#": 4978.03,
                 "E8": 5274.04,
                 "F8": 5587.65,
                 "F8#": 5919.91,
                 "G8": 6271.93,
                 "G8#": 6644.88,
                 "A8": 7040.00,
                 "A8#": 7458.62,
                 "B8": 7902.13
                 }


AMP_THRESHOLD = .05  # percentage on max amplitude threshold
CLOSE_LOG_LABEL_TOLERANCE = 0.1  # if x = 100 -> y < 90 and y > 110 are kept
PLOT_MARGIN = 0.1


def figure_generator(size=figure_size_double):
    yield plt.figure(figsize=size)
