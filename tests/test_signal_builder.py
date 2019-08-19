from random import choice
import numpy as np

from classes.signal_builder import SignalBuilder
from tests.conftest import sine_wave, square_wave, time_range, sawtooth_wave, triangle_wave
import matplotlib.pyplot as plt

TIME_RANGE = time_range()
TEST_FREQUENCIES = [27.0, 54.0, 108.0, 216.0, 432.0, 864.0, 1728.0, 3456.0, 6912.0, 13824.0, 27648.0]
APPROXIMATION_TOLERANCE = 0.01


class ApproximationDifferences:
    sine = list()
    square = list()
    sawtooth = list()
    triangle = list()


# Y: Diff (for each wave form) X: Freq
def test_signal_approximation():
    for freq in TEST_FREQUENCIES: # [choice(TEST_FREQUENCIES) for _ in range(4)]:
        for analytic_sig, wave_shape in zip([sine_wave, square_wave, sawtooth_wave, triangle_wave],
                                        ['sine', 'square', 'sawtooth', 'triangle']):
            sig = analytic_sig(freq)
            signal_builder = SignalBuilder([freq],
                                           [1.],
                                           n_max=200,
                                           wave_type=wave_shape,
                                           t_resolution=TIME_RANGE.size)
            rec_sig = signal_builder.build_signal()
            diff = rec_sig - sig
            wave_shape_diff = getattr(ApproximationDifferences, wave_shape)
            wave_shape_diff.append(abs(diff.mean()))

            print(f'======= {wave_shape.upper()} =======', f'@ {freq} Hz')
            print('Average difference between signals: ', diff.mean(), ' ',
                  f'{diff[diff > APPROXIMATION_TOLERANCE].shape} Samples where difference > {APPROXIMATION_TOLERANCE}')
            print()
#            plt.figure()
#            plt.suptitle(wave_shape.upper() + f' WAVE FORM: Built Signal - Analytic Signal @ {freq} Hz', y=1.)
#
#            plt.subplot(3, 1, 1)
#            period = 2 * np.pi/freq
#            indexes = np.where(TIME_RANGE <= period)
#            for curve, label in zip([rec_sig, sig],
#                                    ['Built Signal', 'Scipy Signal']):
#                plt.plot(TIME_RANGE[indexes], curve[indexes], label=label)
#            plt.legend(loc='best')
#
#            plt.subplot(3, 1, 2)
#            plt.hist(diff, 100, histtype='step', density=True)
#
#            plt.subplot(3, 1, 3)
#            plt.plot(TIME_RANGE[indexes], diff[indexes])
#            plt.show()

            # assert abs(diff.mean()) < APPROXIMATION_TOLERANCE * 0.1
            # mean difference vs frequency?
    plt.figure()
    for wave_form in ['sine', 'square', 'sawtooth', 'triangle']:
        plt.plot(TEST_FREQUENCIES, getattr(ApproximationDifferences, wave_form), label=wave_form.upper())
    plt.legend(loc='best')


test_signal_approximation()
