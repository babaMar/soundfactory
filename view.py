#!/usr/bin/env python

import click
from settings.input_validators import ExistentWav
from settings.plot import plt, AMP_THRESHOLD
from utils.signal import get_envelope, load_audio
from classes.signal_plotter import SignalPlotter
from settings.logging_settings import viewlog


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
    default=0.005,
    type=click.FLOAT,
    metavar="MSECWINDOW",
    help="Time window for sliding FFT in Specgram Plot")
@click.option("--start", type=click.FLOAT, help="seconds to start from")
@click.option("--end", type=click.FLOAT, help="seconds to end to")
@click.option("--min-freq", type=click.FLOAT, help="min frequency to show")
@click.option("--max-freq", type=click.FLOAT, help="max frequency to show")
@click.option("--single", "mode", flag_value="single")
@click.option("--separate", "mode", flag_value="separate", default=True)
@click.option(
    "--thr", "threshold",
    type=click.FLOAT,
    default=AMP_THRESHOLD,
    help="amplitude percentage threshold")
@click.option("--log-pws", flag_value="log_pws", default=False)
def main(
        input_file, calculate_envelope,
        msec_window, start, end, mode,
        min_freq, max_freq, threshold, log_pws
):

    """
    Visualize the signal in an INPUT wav file
    """

    viewlog.info("Loading audio from {}".format(input_file))
    signal, samplerate = load_audio(input_file)

    # Mono signal
    ch1, ch2 = signal, ()
    # Check if stereo signal
    if len(signal.shape) == 2:
        ch1, ch2 = signal[:, 0], signal[:, 1]
    viewlog.info("Loaded {t:.2f} seconds from {c} audio".format(
        t=len(ch1)/samplerate, c="stereo" if len(signal.shape) == 2 else "mono"
    ))
    show_envelope = False
    ch1_envelope, ch2_envelope = (), ()
    if calculate_envelope:
        viewlog.info("Calculating envelope")
        # Volume envelopes
        ch1_envelope, ch2_envelope = get_envelope(ch1), get_envelope(ch2)
        show_envelope = True
    viewlog.info("Creating plots")
    plotter = SignalPlotter(
        plt,
        ch1,
        l_signal_envelope=ch1_envelope,
        r_signal=ch2,
        r_signal_envelope=ch2_envelope,
        sampling_rate=samplerate,
        plot_envelope=show_envelope)
    plotter.show(
        wmsec=float(msec_window),
        start=start, end=end,
        min_freq=min_freq, max_freq=max_freq,
        threshold=threshold,
        mode=mode, log_pws=log_pws)


if __name__ == '__main__':
    main()
