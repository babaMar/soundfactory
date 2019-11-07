============================
The ``create`` functionality
============================

To check all the options run

.. code-block:: bash

    $ soundfactory create --help


.. code-block:: bash

    Usage: soundfactory create [OPTIONS]

    Options:
      -wc, --wave-component FREQ AMP [PHASE] [SHAPE]
                                      [required]
      -o, --out OUTFILE
      -s, --samplerate SAMPLERATE
      -dur, --duration DURATION.. code-block:: bash
      -n, --fourierterms N
      --help

.. warning::
   Use with care the ``fourierterms`` option,
   as more terms in the Fourier series are used to calculate the signal
   as the computing time increases.


Example
*******

Create a two-second sample to hear a 20 Hz beating frequency

.. code-block:: bash

    soundfactory create -wc 109.5 1.2 -wc 139.5 1.2 -dur 2 -o beat_20.wav

where ``109.5 1.2`` and ``139.5 1.2`` are respectively the frequencies and amplitudes
of the two wave components.

The ``waveshape`` and ``phase`` parameters can be also specified as part of the
``-wc`` option. Try running the command above this time for a triangular and a
square wave out of phase of ``90`` degrees.

.. code-block:: bash

    soundfactory create -wc 109.5 1.2 90 triangle -wc 139.5 1.2 square -dur 2 -o beat_20_1.wav

Use ``soundfactory play -i beat_20_1.wav`` to listen to difference and
``soundfactory view -i beat_20_1.wav`` to display the signal and the spectra.
