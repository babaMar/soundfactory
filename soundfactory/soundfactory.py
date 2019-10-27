import click
from soundfactory.view import view as vv
from soundfactory.create import create as cc
from soundfactory.play import play as pp
from soundfactory.settings.input_validators import (
    ExistentWav, Wav, ArbitraryNArgs, WaveComponent
)
from soundfactory.settings.plot import AMP_THRESHOLD


@click.group()
def main():
    pass


@main.command()
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
@click.option("--single", "mode", flag_value="single")
@click.option("--separate", "mode", flag_value="separate", default=True)
@click.option(
    "--thr", "threshold",
    type=click.FLOAT,
    default=AMP_THRESHOLD,
    help="amplitude percentage threshold")
@click.option("--log-pws", flag_value="log_pws", default=False)
@click.option("--save-fig", is_flag=True)
def view(
        input_file, calculate_envelope,
        msec_window, start, end, mode,
        min_freq, max_freq,
        threshold, log_pws, save_fig
):
    vv(
        input_file, calculate_envelope,
        msec_window, start, end, mode,
        min_freq, max_freq,
        threshold, log_pws, save_fig

    )


@main.command()
@click.option(
    "--wave-component", "-wc",
    metavar="FREQ AMP [PHASE] [SHAPE]",
    required=True,
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
@click.option(
    "--duration", "-dur", default=1.,
    metavar="DURATION", type=click.FLOAT
)
@click.option(
    "--fourierterms", "-n", default=100,
    metavar="N", type=click.INT
)
def create(wave_component, out, samplerate, duration, fourierterms):
    cc(wave_component, out, samplerate, duration, fourierterms)


@main.command()
@click.option(
    "--input-file", "-i",
    metavar="INPUT",
    required=True,
    type=ExistentWav())
def play(input_file):
    pp(input_file)


if __name__ == "__main__":
    main()
