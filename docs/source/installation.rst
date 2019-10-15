============
Installation
============


Prerequisites
*************

`soundfactory` is a cli tool that uses PortAudio as audio I/O library underneath.
Despite PortAudio being cross-platform so far `soundfactory` was never tested on Windows OSs.

Before you proceed with the installation the
``libasound2-dev``, ``portaudio19-dev``, ``python-pyaudio``, ``python3-pyaudio`` packages need to be installed
on your machine. On Ubuntu/Debian this can be achieved by:

.. code-block:: bash

  sudo apt-get update
  sudo apt-get install -y libasound2-dev portaudio19-dev python-pyaudio python3-pyaudio

Installing ``soundfactory``
***************************

The easiest way to install `soundfactory` is through pip.

.. code-block:: bash

  pip install soundfactory

