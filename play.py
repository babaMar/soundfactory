from settings.input_validators import ExistentWav
import click
import simpleaudio as sa
import soundfile as sf
import getch


@click.command()
@click.option(
    "--input-file", "-i",
    metavar="INPUT",
    required=True,
    type=ExistentWav())
def main(input_file):
    with sf.SoundFile(input_file) as f:
        channels, samplerate = f.channels, f.samplerate
        is_paused = False
        audio = f.read(dtype="int16")
        play_obj = sa.play_buffer(audio, channels, 2, samplerate)
        print("Playing")
        while play_obj.is_playing():
            command = getch.getch()
            if command == " ":
                if is_paused:
                    play_obj.resume()
                    print("Playing")
                    is_paused = False
                else:
                    play_obj.pause()
                    print("Paused")
                    is_paused = True
        play_obj.wait_done()


if __name__ == "__main__":
    main()
