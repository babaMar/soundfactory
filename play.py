#!/usr/bin/env python

from settings.input_validators import ExistentWav
import click
import simpleaudio as sa
import soundfile as sf
import time
from utils.helpers import progress_time


@click.command()
@click.option(
    "--input-file", "-i",
    metavar="INPUT",
    required=True,
    type=ExistentWav())
def main(input_file):
    with sf.SoundFile(input_file) as f:
        channels, samplerate = f.channels, f.samplerate
        audio = f.read(dtype="float32")
        audio = (audio * 32767).astype("int16")
        total_seconds = len(f) / samplerate
        play_obj = sa.play_buffer(audio, channels, 2, samplerate)
        start_time = time.time()
        while play_obj.is_playing():
            progress_time(total_seconds, time.time() - start_time)
        print("\n")


if __name__ == "__main__":
    main()
