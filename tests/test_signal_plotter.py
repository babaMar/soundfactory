from unittest import mock
from classes.signal_plotter import SignalPlotter
import numpy as np


@mock.patch('classes.signal_plotter.SignalPlotter.show')
def test_show_plot(mock_plt):
    ch1, ch2 = np.array([1, 2, 3]), np.array([4, 5, 3])
    plotter = SignalPlotter(
        ch1,
        r_signal=ch2
    )
    plotter.show()
    mock_plt.plot.assert_called_once_with(ch1, r_signal=ch2)
