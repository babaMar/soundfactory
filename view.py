#!/usr/bin/env python

import click
from settings.input_validators import ExistentWav
from utils.signal import get_envelope, load_audio
from classes.signal_plotter import SignalPlotter


@click.command()
@click.option(
    "--input-file", "-i",
    metavar="INPUT",
    required=True,
    type=ExistentWav())
@click.option(
    "--calculate_envelope", "-e", is_flag=True,
    help="Whether to show the signal envelope")
@click.option(
    "--msec-window", "-w",
    default=1,
    type=click.FLOAT,
    metavar="MSECWINDOW",
    help="Time window for sliding FFT in Specgram Plot")
@click.option("--start", type=click.FLOAT, help="seconds to start from")
@click.option("--end", type=click.FLOAT, help="seconds to end to")
@click.option("--single", "mode", flag_value="single")
@click.option("--separate", "mode", flag_value="separate", default=True)
def main(input_file, calculate_envelope, msec_window, start, end, mode):

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
    plotter = SignalPlotter(
        ch1,
        l_signal_envelope=ch1_envelope,
        r_signal=ch2,
        r_signal_envelope=ch2_envelope,
        sampling_rate=samplerate,
        plot_envelope=show_envelope)
    plotter.show(wmsec=float(msec_window), start=start, end=end, mode=mode)


if __name__ == '__main__':
    main()
