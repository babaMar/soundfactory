#!/usr/bin/env python

import click

from utils.signal import get_envelope, load_audio
from classes.signal_plotter import SignalPlotter


@click.command()
@click.argument("input-file", metavar="INPUT")
@click.option(
    "--calculate_envelope", "-e",
    default=False,
    help="Whether to show the signal envelope")
@click.option(
    "--msec-window", "-w",
    default=1,
    metavar="MSECWINDOW",
    help="Time window for sliding FFT in Specgram Plot")
def main(input_file, calculate_envelope, msec_window):
    """
    Visualize the signal in an INPUT wav file
    """
    # TODO Logging!

    # Load signal and sampling rate
    signal, samplerate = load_audio(input_file)

    # Mono signal
    ch1, ch2 = signal, ()
    # Check if stereo signal
    if len(signal.shape) == 2:
        ch1, ch2 = signal[:, 0], signal[:, 1]

    show_envelope = False
    ch1_envelope, ch2_envelope = (), ()
    if calculate_envelope:
        # Volume envelopes
        ch1_envelope, ch2_envelope = get_envelope(ch1), get_envelope(ch2)
        show_envelope = True

    Plotter = SignalPlotter(
        ch1,
        l_signal_envelope=ch1_envelope,
        r_signal=ch2,
        r_signal_envelope=ch2_envelope,
        sampling_rate=samplerate,
        plot_envelope=show_envelope)
    Plotter.show(wmsec=float(msec_window))


if __name__ == '__main__':
    main()
