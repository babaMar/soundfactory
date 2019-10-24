import numpy as np

import matplotlib.pyplot as plt
from soundfactory.signal_plotter import SignalPlotter


def test_show_plot(mocker):
    plotting_interface = mocker.MagicMock()
    plotting_interface.cm.jet = plt.cm.jet
    plotter = SignalPlotter(
        plotting_interface,
        np.ones(10),
    )
    plotter.show()
    plotting_interface.show.assert_called_once_with()
