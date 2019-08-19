#!/usr/bin/env python

import argparse

from utils.signal import get_envelope, load_audio
from classes.signal_plotter import SignalPlotter


def parse_arguments():
    parser = argparse.ArgumentParser(description='Visualize the Signal in a wave file')
    parser.add_argument('-i', '--input-file', metavar='INPUT', required=True, help='Path to wav input file')
    parser.add_argument('-e', '--calculate-envelope', action='store_true', help='Whether to show the signal envelope')
    parser.add_argument('-w', '--msec-window', metavar='MSECWINDOW', default=1, help='Time window for sliding FFT in Specgram Plot.')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    audio_file = args.input_file
    # TODO Logging!

    # Load signal and sampling rate
    signal, samplerate = load_audio(audio_file)

    # Mono signal
    ch1, ch2 = signal, ()
    # Check if stereo signal
    if len(signal.shape) == 2:
        ch1, ch2 = signal[:,0], signal[:,1]

    show_envelope = False
    ch1_envelope, ch2_envelope = (), ()
    if args.calculate_envelope:
        # Volume envelopes
        ch1_envelope, ch2_envelope = get_envelope(ch1), get_envelope(ch2)
        show_envelope = True

    Plotter = SignalPlotter(ch1,
                            l_signal_envelope=ch1_envelope,
                            r_signal=ch2,
                            r_signal_envelope=ch2_envelope,
                            sampling_rate=samplerate,
                            plot_envelope=show_envelope)
    Plotter.show(wmsec=float(args.msec_window))


if __name__ == '__main__':
    main()
