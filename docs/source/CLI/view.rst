==========================
The ``view`` functionality
==========================

To check all the options run


.. code-block:: bash

    soundfactory view --help


.. code-block:: bash

    Usage: soundfactory view [OPTIONS]

    Options:
      -i, --input-file INPUT        [required]
      -e, --calculate_envelope      Whether to show the signal envelope
      -w, --msec-window MSECWINDOW  Time window for sliding FFT in Specgram Plot
      --start FLOAT                 seconds to start from
      --end FLOAT                   seconds to end to
      --min-freq FLOAT              min frequency to show
      --max-freq FLOAT              max frequency to show
      --single
      --separate
      --thr FLOAT                   amplitude percentage threshold
      --log-pws
      --save-fig
      --help                        Show this message and exit.


To inspect 300 milliseconds of the ``beat_20_1.wav`` sample produced in the
``create`` example run

.. code-block:: bash

    soundfactory view --start 0.2 --end 0.5 -i beat_20_1.wav

You should get the following image:

.. image:: https://raw.githubusercontent.com/babaMar/soundfactory/master/docs/source/_static/beat_20_1.png

You can save on disk all the single plots separately by running

.. code-block:: bash

    soundfactory view --start 0.2 --end 0.5 -i beat_20_1.wav --separate --save-fig

which will create the ``beat_20_1_signal_0.png``, ``beat_20_1_fft_0.png``,
and ``view_spectrogram_0.png`` in the current directory.