=============
API Reference
=============

The ``signal_builder`` module implement the ``SignalBuilder`` class used in
``create`` to produce an audio sample by additive synthesis. It basically
**approximates** the analytical signal by summing the Fourier series for each
component given as input (when ``triangle``, ``sawtooth``, or ``square`` is
specified as shape parameter), and finally sum together all components. To save
the audio on file, call its ``export(filename)`` method.

-------------------------------------------------------------------------------

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
to: plot the signal itself, its Frequency Spectrum and the Spectrogram. The class takes
as input the audio file path.

-------------------------------------------------------------------------------

.. automodule:: soundfactory.signal_plotter
.. autoclass:: SignalPlotter

    :param plotting_interface: an interface to matplotlib, usually pyplot
    :param l_signal: the left channel audio content
    :type l_signal: array
    :param l_signal_envelope: left channel envelope
    :type l_signal_envelope: array or None
    :param r_signal: the right channel audio content
    :type r_signal: array or None
    :param r_signal_envelope: right channel envelope
    :type r_signal_envelope: array or None
    :param sampling_rate: sampling rate of the audio input
    :type sampling_rate: int
    :param plot_envelope: whether to plot the envelope together with the signal
    :type plot_envelope: bool
    :param fname: prefix for the image files
    :type fname: string

                 plotting_interface,
                 l_signal,
                 l_signal_envelope=(),
                 r_signal=(),
                 r_signal_envelope=(),
                 sampling_rate=44100,
                 plot_envelope=False,
                 fname='view'):
