import os
import click


class ExistentWav(click.ParamType):
    name = '--input_file'

    def convert(self, value, param, ctx):
        is_wav = os.path.splitext(value)[1] == ".wav"
        if not is_wav:
            self.fail('{} is not a wav file'.format(value), param, ctx)
        if not os.path.isfile(value):
            self.fail('{} not found'.format(value), param, ctx)
        return value


class Wav(click.ParamType):
    name = '--out'

    def convert(self, value, param, ctx):
        is_wav = os.path.splitext(value)[1] == ".wav"
        if not is_wav:
            self.fail('Output should be a .wav', param, ctx)
        return value
