# soundfactory
[![Build Status](https://travis-ci.org/babaMar/soundfactory.svg?branch=development)](https://travis-ci.org/babaMar/soundfactory)
[![codecov](https://codecov.io/gl/babaMar/soundfactory/branch/development/graph/badge.svg)](https://codecov.io/gl/babaMar/soundfactory)
[![Documentation Status](https://readthedocs.org/projects/soundfactory/badge/?version=latest)](https://soundfactory.readthedocs.io/en/latest/?badge=latest)

`soundfactory` is a simple tool to experiment and be creative with audio taking a data-oriented approach.
It is primarily directed to digital artists that want to generate audio samples
from diverse data sources, and to audio-engineering students at their first steps
into the beautiful world of additive sound synthesis.

The peculiarity about `soundfactory` is the adoption of fourier-series approximation
when `square`, `sawtooth`, or `triangle` wave shapes are chosen. In fact, being 
approximated the single-oscillator signals will contain upper harmonics with respect
to the analytical signal (with the same amplitude, frequency, and wave shape), 
that can be obtained by `scipy` (see tests). The result will be a warmer and 
unexpectedly coloured sound.
 
It comes from some scripts I have been writing a few years back and thought about
having few reusable core modules and a command-line tool for researching new sounds.
And I wanted to be able to develop it and have fun with it in my Jupyter Notebook of course!

You can find the documentation at https://soundfactory.readthedocs.io

---
**WARNING**

Before installing with `pip` check the [pre-requirements](https://soundfactory.readthedocs.io/en/latest/installation.html#prerequisites)

---

## Examples
### Random Sample Generator
```python
from random import uniform, choice
from soundfactory import SignalBuilder, SignalPlotter
import matplotlib.pyplot as plt

n_components = 4
MAX_FREQ = 1000.

fname = ''
freqs, amps, shapes = list(), list(), list()
for _ in range(n_components):
    freq = round(uniform(20., MAX_FREQ), 1)
    freqs.append(freq)
    amp = round(uniform(0.1, 1.), 1)
    amps.append(amp)
    shape = choice(['sine', 'square', 'sawtooth', 'triangle'])
    shapes.append(shape)
    fname += '_'.join([str(freq), str(amp), shape])

s = SignalBuilder(
    freqs, amps, shapes,
    samplerate=96000,
    duration=2.
)
fname += '.wav'
s.export(fname)

# Analyse with SignalPlotter
sig = SignalPlotter(plt, fname, True)
sig.show(wmsec=0.1)
```

### Reproducing a Sound Characteristic at an arbitrary Frequency
```python
from numpy import where, sqrt
import matplotlib.pyplot as plt

from soundfactory import SignalBuilder, SignalPlotter
from soundfactory import Signal
from soundfactory.utils.scale import build_24_tet_scale

SCALE_INIT = {'E0': 20.6}

ref_label = list(SCALE_INIT.keys())[-1]
ref_frequency = list(SCALE_INIT.values())[-1]
scale_24 = build_24_tet_scale(ref_label, ref_frequency, max_octave=3)

ref_signal = Signal('/<path-to-packages>/soundfactory/samples/A3-Calib-220.wav')

freqs = ref_signal.SPECTRA['ch1_fft'][ref_signal.FREQUENCIES]
pws = ref_signal.SPECTRA['ch1_fft'][ref_signal.POWERS]

# Select only few of the spectral components
select_idx = where(pws > 0.00001)[0]
# Get the fundamental frequency to obtain the upper-harmonic orders
fundamental_idx = where(pws == pws.max())[0]
freq_ratios = freqs / freqs[fundamental_idx]

tone = 'E3𝄲'  # Choose an arbitrary tone NOT playble on the keyboard
input_freqs = scale_24[tone] * freq_ratios[select_idx]
input_amps = sqrt(2 * pws[select_idx])

my_signal = SignalBuilder(input_freqs,
                          input_amps, [
                          'sine' for _ in range(len(select_idx))]
                         )

filename = './%s_sample.wav' % tone
my_signal.export(filename)

# Analyse with SignalPlotter
sig = SignalPlotter(plt, filename, True)
sig.show(wmsec=0.1)

```