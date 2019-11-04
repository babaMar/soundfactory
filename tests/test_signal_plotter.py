import matplotlib.pyplot as plt
from numpy import ndarray
from soundfactory.signal_plotter import SignalPlotter


def test_show_plot(mocker,
                   mono_audio_file,
                   stereo_audio_file):
    plotting_interface = mocker.MagicMock()
    plotting_interface.cm.jet = plt.cm.jet
    plotter = SignalPlotter(
        plotting_interface,
        mono_audio_file,
    )
    assert plotter.y_label == "Mono Channel (t)"
    assert plotter.x_label == "t [sec]"
    assert not plotter.plot_envelope
    assert plotter.n_figures == 1
    assert isinstance(plotter.time_range, ndarray)

    plotter.show()
    plotting_interface.show.assert_called_once_with()
    plotting_interface.tight_layout.assert_called_once_with()

    plotter = SignalPlotter(
        plotting_interface,
        stereo_audio_file,
        with_envelope=True,
    )
    assert plotter.y_label == "Left Channel (t)"
    assert plotter.x_label == "t [sec]"
    assert plotter.plot_envelope
    assert plotter.n_figures == 2
    assert isinstance(plotter.time_range, ndarray)

    plotter.show(wmsec=0.1,
                 start=0.1, end=0.9,
                 min_freq=20, max_freq=10000,
                 threshold=0.1, close_tolerance=0.001,
                 mode='single',
                 log_pws=True, savefigures=True)
    plotting_interface.tight_layout.assert_called_with()
