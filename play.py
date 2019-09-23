#!/usr/bin/env python

from settings.input_validators import ExistentWav
from settings.logging_settings import playlog
import click
import simpleaudio as sa
import soundfile as sf
import time
from utils.helpers import progress_time
from constants import MAX_16_BIT_VALUE, BYTE_PER_16_BIT


def play(path):
    with sf.SoundFile(path) as f:
        playlog.info("Loading audio from {}".format(path))
        channels, samplerate = f.channels, f.samplerate
        total_seconds = len(f) / samplerate
        audio = f.read(dtype="float32")
        playlog.info(
            "Loaded {t:.2f} seconds from {c} audio".format(
                t=total_seconds,
                c="stereo" if channels == 2 else "mono"
            ))
        playlog.info("Converting audio to 16 bit")
        audio = (audio * MAX_16_BIT_VALUE).astype("int16")
        play_obj = sa.play_buffer(audio, channels, BYTE_PER_16_BIT, samplerate)
        start_time = time.time()
        while play_obj.is_playing():
            progress_time(total_seconds, time.time() - start_time)
        print("\n")


@click.command()
@click.option(
    "--input-file", "-i",
    metavar="INPUT",
    required=True,
    type=ExistentWav())
def main(input_file):
    play(input_file)

    
if __name__ == "__main__":
    main()
