# soundfactory

A simple python cli to play, visualize, and create every kind of signal.

Packages required on host OS: `portaudio19-dev`, `texlive-full`

### Pre-Requirements
```
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
```

At the moment only visualization working examples are available.
Run the mono example with:

```
./view.py -i mono_bell.wav -w 0.9
```

And the stereo one with

```
./view.py -i A-Calib440.wav
```
