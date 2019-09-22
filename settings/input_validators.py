import os
import click
import numbers
from settings.signal import B_N_COEFF_MAP

DEFAULT_PHASE = 0
DEFAULT_WAVE_TYPE = "sine"


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

    
class ArbitraryNArgs(click.Option):
    """
    https://stackoverflow.com/questions/48391777/
    nargs-equivalent-for-options-in-click

    """
    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(ArbitraryNArgs, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(ArbitraryNArgs, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) \
                or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


class WaveComponent(click.ParamType):

    def convert(self, value, param, ctx):
        self.validate(value, param, ctx)
        freq, amp = float(value[0]), float(value[1])
        if len(value) == 2:
            phase, wave_type = DEFAULT_PHASE, DEFAULT_WAVE_TYPE
        if len(value) == 3:
            try:
                phase = float(value[-1])
                wave_type = DEFAULT_WAVE_TYPE
            except ValueError:
                phase = DEFAULT_PHASE
                wave_type = value[-1]
        if len(value) == 4:
            phase, wave_type = float(value[2]), value[3]
        return freq, amp, phase, wave_type

    def validate(self, value, param, ctx):
        if len(value) > 4:
            self.fail('too many values provided', param, ctx)
        try:
            float(value[0]), float(value[1])
        except (ValueError, IndexError):
            self.fail('provide two real numbers for frequency and amplitude')
        if len(value) == 3:
            try:
                float(value[-1])
            except ValueError:
                if not self.is_valid_waveshape(value[-1]):
                    self.fail('available waveforms are: {}'.format(
                        sorted(B_N_COEFF_MAP.keys())),
                        param, ctx)
        
        if len(value) == 4:
            try:
                float(value[-2])
            except ValueError:
                self.fail(
                    "provide a real number for phase argument in {}".format(
                        value))
            if not self.is_valid_waveshape(value[-1]):
                self.fail(
                    'available waveforms are: {}'.format(
                        sorted(B_N_COEFF_MAP.keys())),
                    param, ctx)

    @staticmethod
    def is_valid_waveshape(shape):
        return shape in B_N_COEFF_MAP
