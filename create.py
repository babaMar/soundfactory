#!/usr/bin/env python

import click
import numpy as np
from classes.signal_builder import SignalBuilder
from settings.input_validators import Wav
from settings.signal import B_N_COEFF_MAP
from settings.logging_settings import createlog


logger = createlog


@click.command()
@click.option(
    '--freq_amp', "-fa", required=True,
    type=(click.FLOAT, click.FLOAT), multiple=True)
@click.option(
    "--out", "-o",
    metavar="OUTFILE",
    default="out.wav",
    type=Wav())
@click.option(
    "--wave", "-w", metavar="WAVETYPE", default="square",
    type=click.Choice(list(B_N_COEFF_MAP.keys())))
@click.option(
    "--samplerate", "-s", default=44100,
    metavar="SAMPLERATE", type=click.INT)
def main(freq_amp, wave, out, samplerate):
    """
    Create a signal from given frequencies and amplitudes and
    save it on an out file

    """
    freqs = [x[0] for x in freq_amp]
    amps = [x[1] for x in freq_amp]
    freqs, amps = np.array(freqs), np.array(amps)
    logger.info("Building signal")
    s = SignalBuilder(freqs, amps, wave_type=wave, t_resolution=samplerate)
    logger.info("Exporting signal")
    s.export(out, samplerate=samplerate)
    logger.info("Saved audio on {}".format(out))


if __name__ == "__main__":
    main()
