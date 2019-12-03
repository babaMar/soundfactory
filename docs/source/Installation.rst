============
Installation
============



Prerequisites
*************

`soundfactory` is a cli tool that uses PortAudio as audio I/O library underneath.
Despite PortAudio being cross-platform so far `soundfactory` was never tested on Windows OSs.

Before you proceed with the installation the ``libffi-dev``, ``python3-tk``,
``libasound2-dev``, ``portaudio19-dev``, ``python-pyaudio``, ``python3-pyaudio`` packages need to be installed
on your machine. On Ubuntu/Debian this can be achieved by:

.. code-block:: bash

  sudo apt-get update
  sudo apt-get install -y libffi-dev python3-tk libasound2-dev portaudio19-dev python-pyaudio python3-pyaudio

If you like LaTex formatting for the plt labels install  `texlive-full` as well

.. code-block:: bash

  sudo apt-get install -y texlive-full

and hack the `<path-to-our-installed-package>/settings/plot.pyL30` file by swapping the `usetex` flag to `True`:

.. code-block:: python

   plt.rc('text', usetex=True)


Installing ``soundfactory``
***************************

The easiest way to install `soundfactory` is through pip.

.. code-block:: bash

  pip install soundfactory
