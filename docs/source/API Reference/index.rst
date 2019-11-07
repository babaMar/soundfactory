=============
API Reference
=============

The ``signal_builder`` module implement the ``SignalBuilder`` class used in
``create`` to produce an audio sample by additive synthesis. It basically
**approximates** the analytical signal by summing the Fourier series for each
component given as input (when ``triangle``, ``sawtooth``, or ``square`` is
specified as shape parameter), and finally sum together all components. To save
the audio on file, call its ``export(filename)`` method.


.. automodule:: soundfactory.signal_builder
.. autoclass:: SignalBuilder

    :param frequencies: the frequency value for each component
    :type frequencies: list or array of floats
    :param amplitudes: the amplitude value for each component
    :type amplitudes: list or array of floats
    :param wave_types: the wave shape type for each component
    :type wave_types: list or array of strings. Allowed values: 'triangle', 'square', 'sawtooth'
    :param phases: the phase value for each component
    :type phases: list or array of floats or None
    :param n_max: Number of terms to consider in the Fourier series
    :type n_max: int
    :param duration: length of the desired audio sample in seconds
    :type duration: float
    :param samplerate: sampling rate of the generated audio
    :type samplerate: integer or default to 44100

-------------------------------------------------------------------------------

The ``signal_plotter`` module implement the ``SignalPlotter`` class used in ``view``
to: plot the signal itself, its Frequency Spectrum and the Spectrogram.

The class takes as input the audio file path as it is a subclass of the base class
``Signal``, which loads the audio, calculate envelopes and spectra directly in the constructor.


.. automodule:: soundfactory.signal_base
.. autoclass:: Signal

    :param input_file: the audio to be analysed
    :type input_file: wav format
    :param with_envelope: whether to calculate and store the signal envelope
    :type with_envelope: bool

To retrieve the audio information, assuming ``s`` is a ``Signal`` instance:

* ``s.CHANNELS`` is a ``dict`` holding the audio signal as an array accessible via
  the ``'ch1'`` (and ``'ch2'`` if stereo) keys.

* ``s.ENVELOPES`` is a ``dict`` holding the signal envelop calculated via the
  ``hilbert`` method in ``scipy.signal`` accessible via the ``'ch1_envelope'``
  (and ``'ch2_envelope'`` if stereo) keys.

* ``s.SPECTRA`` is a ``dict`` holding the spectral information accessible via
  the ``'ch1_fft'`` (and ``'ch2_fft'`` if stereo) keys, which in turn returns
  another ``dict`` with the ``'freqs'`` and ``'pws'`` (respectively defined as class
  constants ``s.FREQUENCIES`` and ``s.POWERS``) keys. So to get the power spectrum
  information for the first channel: ``s.SPECTRA['ch1_fft'][s.POWERS]`` and
  ``s.SPECTRA['ch1_fft'][s.FREQUENCIES]``.

-------------------------------------------------------------------------------

.. automodule:: soundfactory.signal_plotter
.. autoclass:: SignalPlotter

    :param plotting_interface: an interface to matplotlib, usually pyplot
    :param input_file: the audio to be analysed
    :type input_file: wav format
    :param with_envelope: whether to plot the envelope together with the signal
    :type with_envelope: bool
    :param fname: prefix for the image files
    :type fname: string
