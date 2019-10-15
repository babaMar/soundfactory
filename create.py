#!/usr/bin/env python

import click
import numpy as np
from classes.signal_builder import SignalBuilder
from settings.input_validators import Wav, ArbitraryNArgs, WaveComponent
from settings.logging_settings import createlog


@click.command()
@click.option(
    '--wave-component', "-wc", required=True,
    cls=ArbitraryNArgs,
    type=WaveComponent(),
    multiple=True)
@click.option(
    "--out", "-o",
    metavar="OUTFILE",
    default="out.wav",
    type=Wav())
@click.option(
    "--samplerate", "-s", default=44100,
    metavar="SAMPLERATE", type=click.INT)
def main(wave_component, out, samplerate):
    """
    Create a signal from given frequencies and amplitudes and
    save it on an out file

    """
    freqs = np.array([x[0] for x in wave_component])
    amps = np.array([x[1] for x in wave_component])
    phases = np.array([x[2] for x in wave_component])
    wave_types = [x[3] for x in wave_component]
    createlog.info("Building signal")
    s = SignalBuilder(
        freqs, amps, wave_types,
        phases=phases, t_resolution=samplerate)
    createlog.info("Exporting signal")
    s.export(out, samplerate=samplerate)
    createlog.info("Saved audio on {}".format(out))


if __name__ == "__main__":
    main()
