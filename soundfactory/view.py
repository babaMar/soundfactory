#!/usr/bin/env python

import click
from .settings.input_validators import ExistentWav
from .settings.plot import plt, AMP_THRESHOLD
from .utils.signal import get_envelope, load_audio
from .signal_plotter import SignalPlotter
from .settings.logging_settings import viewlog


def view(
        input_file, calculate_envelope,
        msec_window, start, end, mode,
        min_freq, max_freq,
        threshold, log_pws, save_fig
):

    """
    Visualize the signal in an INPUT wav file
    """
    filename_no_ext = str(input_file).replace('.wav', '')
    viewlog.info("Loading audio from {}".format(input_file))
    signal, samplerate = load_audio(input_file)

    # Mono signal
    ch1, ch2 = signal, ()
    # Check if stereo signal
    if len(signal.shape) == 2:
        ch1, ch2 = signal[:, 0], signal[:, 1]
    duration = len(ch1)/samplerate
    viewlog.info("Loaded {t:.2f} seconds from {c} audio".format(
        t=duration, c="stereo" if len(signal.shape) == 2 else "mono"
    ))
    show_envelope = False
    ch1_envelope, ch2_envelope = (), ()
    if calculate_envelope:
        viewlog.info("Calculating envelope")
        # Volume envelopes
        ch1_envelope, ch2_envelope = get_envelope(ch1), get_envelope(ch2)
        show_envelope = True
    viewlog.info("Creating plots")
    viewlog.info("Frequency resolution: {} Hz".format(round(1./duration, 2)))
    plotter = SignalPlotter(
        plt,
        ch1,
        l_signal_envelope=ch1_envelope,
        r_signal=ch2,
        r_signal_envelope=ch2_envelope,
        sampling_rate=samplerate,
        plot_envelope=show_envelope,
        fname=filename_no_ext)
    plotter.show(
        wmsec=float(msec_window),
        start=start, end=end,
        min_freq=min_freq, max_freq=max_freq,
        threshold=threshold,
        mode=mode, log_pws=log_pws,
        savefigures=save_fig)


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
    default=0.1,
    type=click.FLOAT,
    metavar="MSECWINDOW",
    help="Time window for sliding FFT in Specgram Plot")
@click.option("--start", type=click.FLOAT, help="seconds to start from")
@click.option("--end", type=click.FLOAT, help="seconds to end to")
@click.option("--min-freq", type=click.FLOAT, help="min frequency to show")
@click.option("--max-freq", type=click.FLOAT, help="max frequency to show")
@click.option("--single", "mode", flag_value="single", default=True)
@click.option("--separate", "mode", flag_value="separate")
@click.option(
    "--thr", "threshold",
    type=click.FLOAT,
    default=AMP_THRESHOLD,
    help="amplitude percentage threshold")
@click.option("--log-pws", flag_value="log_pws", default=False)
@click.option('--save-fig', is_flag=True)
def main(
        input_file, calculate_envelope,
        msec_window, start, end, mode,
        min_freq, max_freq,
        threshold, log_pws, save_fig
):
    view(
        input_file, calculate_envelope,
        msec_window, start, end, mode,
        min_freq, max_freq,
        threshold, log_pws, save_fig
    )


if __name__ == '__main__':
    main()
