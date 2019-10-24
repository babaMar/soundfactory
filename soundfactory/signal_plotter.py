import numpy as np
from matplotlib.ticker import (NullFormatter,
                               LogLocator,
                               NullLocator)

from soundfactory.utils.helpers import (above_thr_mask,
                                        spectrum)
from soundfactory.settings.plot import (
    figure_size_single,
    figure_size_double,
    figure_size_full,
    figure_generator,
    colors,
    FONT_PROP,
    AMP_THRESHOLD,
    PLOT_MARGIN,
    CLOSE_LOG_LABEL_TOLERANCE
)
from soundfactory.settings.logging_settings import plotterlog
from soundfactory.utils.labels import (sparse_major_freqs,
                                       hz_to_note,
                                       log_khz_formatter)


class SignalPlotter:

    def __init__(self,
                 plotting_interface,
                 l_signal,
                 l_signal_envelope=(),
                 r_signal=(),
                 r_signal_envelope=(),
                 sampling_rate=44100,
                 plot_envelope=False):

        # Mono signal is treated as left only
        self.left_raw = l_signal
        self.plot_envelope = plot_envelope
        self.y_label = "Mono Channel (t)"
        self.x_label = "t [sec]"
        self.plt = plotting_interface

        if any(l_signal_envelope):
            self.left_envelope = l_signal_envelope
            self.envelopes = [self.left_envelope]
            self.i_env = 0

        self.n_figures = 1
        self.figures = dict()
        self.channels = [self.left_raw]
        if any(r_signal):
            self.right_raw = r_signal
            self.y_label = self.y_label.replace('Mono', 'Left')
            self.n_figures += 1
            self.channels.append(self.right_raw)
            if any(r_signal_envelope):
                self.right_envelope = r_signal_envelope
                self.envelopes.append(self.right_envelope)

        self.sampling_rate = float(sampling_rate)
        # Time domain information
        self.samples = self.left_raw.shape[0]
        self.time_length = self.samples / self.sampling_rate  # in seconds
        self.time_range = np.linspace(0., self.time_length, self.samples)

    def _create_figures(self, size=figure_size_single):
        return [next(figure_generator(size=size)) for _ in range(self.n_figures)]

    @staticmethod
    def _lims_above_thr(ax, threshold=.1):
        x, y = ax.lines[0].get_xdata(), ax.lines[0].get_ydata()
        mask = above_thr_mask(y, threshold=threshold)
        mask_idx = np.where(mask)[0]
        return x[mask_idx[0]], x[mask_idx[-1]]

    @staticmethod
    def _setup_log_decimals_labels(
            axis, subs=np.linspace(0, 1, 5, endpoint=False)):
        axis.set_major_formatter(log_khz_formatter)
        axis.set_minor_locator(LogLocator(subs=subs))
        axis.set_minor_formatter(log_khz_formatter)

    @staticmethod
    def _set_xlim(axes, left=None, right=None):
        for ax in axes:
            ax.set_xlim(left, right)

    @staticmethod
    def _set_ylim(axes, bottom=None, top=None):
        for ax in axes:
            ax.set_ylim(bottom, top)

    def _plot_fft(self, axes, axcolors=None):
        if not axcolors:
            axcolors = [next(colors) for _ in range(len(axes))]
        for ax, channel, c in zip(axes, self.channels, axcolors):
            freqs, pws = spectrum(channel, self.sampling_rate)
            ax.plot(freqs, pws, c + "-")
            ax.set_xlabel("Frequency [kHz]", fontproperties=FONT_PROP)
            ax.set_ylabel("Power(f)", fontproperties=FONT_PROP)

    def _plot_signal(
            self,
            axes,
            axcolors=None):
        if not axcolors:
            axcolors = [next(colors) for _ in range(self.n_figures)]
        for ax, channel, c in zip(axes, self.channels, axcolors):
            ax.plot(self.time_range, channel, c + '--', lw=0.1)
            if self.plot_envelope:
                ax.plot(
                    self.time_range, self.envelopes[self.i_env], 'k-', lw=0.1)
                self.i_env += 1
            ax.set_xlim(self.time_range[0], self.time_range[-1])
            ax.set_ylabel(self.y_label, fontproperties=FONT_PROP)
            ax.set_xlabel(self.x_label, fontproperties=FONT_PROP)
            self.y_label = self.y_label.replace('Left', 'Right')

    def _plot_spectrogram(self, axes, wmsec=0.005):
        npoints = int(self.sampling_rate * wmsec)
        overlap = int(self.sampling_rate * wmsec / 2.)
        for ax, channel, in zip(axes, self.channels):
            Pxx, freqs, bins, im = ax.specgram(
                channel, NFFT=npoints, Fs=self.sampling_rate,
                noverlap=overlap, cmap=self.plt.cm.jet)
            ax.set_xlabel(self.x_label, fontproperties=FONT_PROP)
            ax.set_ylabel("Frequency [kHz]", fontproperties=FONT_PROP)
            ax.set_ylim(20., 20000.)
            ax.set_yscale('log')
            self._setup_log_decimals_labels(ax.yaxis, subs=[.2, .4])
            
    def _pws_labels(self, ax, threshold=0.1, close_tolerance=0.1, log_y=False):
        data = ax.lines[0].get_data()
        freqs, pws = data
        ax.set_xscale("log")
        ax.set_yscale("{}".format("log" if log_y else "linear"))
        ax2 = ax.twiny()
        x_ticks = sparse_major_freqs(
            freqs, pws, threshold=threshold, close_tolerance=close_tolerance)
        x_labels = [hz_to_note(x) for x in x_ticks]
        ax2.set_xlim(ax.get_xlim())
        self._setup_log_decimals_labels(ax.xaxis)
        ax2.set_xscale("log")
        ax2.set_xticks(x_ticks)
        ax2.set_xticklabels(x_labels, rotation=45, fontproperties=FONT_PROP)
        ax2.xaxis.set_minor_locator(NullLocator())
        ax2.xaxis.set_minor_formatter(NullFormatter())

    def _set_xmargins(self, ax, margin, freqs_interval, log=False):
        lim = freqs_interval
        if log:
            margin = 1 + margin
            a = lim[0] / margin
            b = lim[1] * margin
        else:
            delta = np.diff(lim) * margin
            a = lim[0] - delta
            b = lim[1] + delta
        ax.set_xlim(a, b)

    def _set_ymargins(self, ax, margin, freqs_interval, log=False):
        lim = freqs_interval
        if log:
            margin = 1 + margin
            a = lim[0] / margin
            b = lim[1] * margin
        else:
            delta = np.diff(lim) * margin
            a = lim[0] - delta
            b = lim[1] + delta
        ax.set_ylim(a, b)

    def show(
            self, wmsec=0.005,
            start=None, end=None,
            min_freq=None, max_freq=None,
            threshold=AMP_THRESHOLD,
            close_tolerance=CLOSE_LOG_LABEL_TOLERANCE,
            mode="separate",
            log_pws=False,
            savefigures=False):
        if mode == "separate":
            plotterlog.info("Creating separate figures")
            spec_figs = self._create_figures(size=figure_size_double)
            spec_axes = [f.add_subplot(111) for f in spec_figs]
            self.figures.update(
                {'spectrogram_%d' % i: f for i, f in enumerate(spec_figs)})
            signal_figs = self._create_figures()
            signal_axes = [f.add_subplot(111) for f in signal_figs]
            self.figures.update(
                {'signal_%d' % i: f for i, f in enumerate(signal_figs)})
            fft_figs = self._create_figures()
            fft_axes = [f.add_subplot(111) for f in fft_figs]
            self.figures.update(
                {'fft_%d' % i: f for i, f in enumerate(fft_figs)})
        elif mode == "single":
            plotterlog.info("Creating single figure")
            nrows, ncols = 3, self.n_figures
            fig = self.plt.figure(figsize=figure_size_full)
            spec = fig.add_gridspec(ncols=ncols, nrows=nrows)
            signal_axes = [fig.add_subplot(spec[0, c]) for c in range(ncols)]
            fft_axes = [fig.add_subplot(spec[1, c]) for c in range(ncols)]
            spec_axes = [fig.add_subplot(spec[2, c]) for c in range(ncols)]
        else:
            raise NotImplementedError('mode {} not recognized'.format(mode))
        axcolors = [next(colors) for _ in range(self.n_figures)]
        plotterlog.info("Plotting signal")
        self._plot_signal(signal_axes, axcolors=axcolors)
        plotterlog.info("Plotting power spectrum")
        self._plot_fft(fft_axes, axcolors=axcolors)
        plotterlog.info("Plotting spectrogram")
        self._plot_spectrogram(spec_axes, wmsec=wmsec)

        plotterlog.info("Setting view ranges and labels")
        if any([start, end]):
            self._set_xlim(spec_axes + signal_axes, start, end)
        if any([min_freq, max_freq]):
            self._set_ylim(spec_axes, min_freq, max_freq)
            self._set_xlim(fft_axes, min_freq, max_freq)
            for ax in fft_axes:
                self._pws_labels(
                    ax,
                    threshold=threshold,
                    close_tolerance=close_tolerance,
                    log_y=log_pws)
        else:
            for ax in fft_axes:
                min_freq, max_freq = self._lims_above_thr(
                    ax, threshold=threshold)
                self._set_xmargins(
                    ax, PLOT_MARGIN, (min_freq, max_freq), log=True)
                self._pws_labels(
                    ax,
                    threshold=threshold,
                    close_tolerance=close_tolerance,
                    log_y=log_pws)

        self.plt.tight_layout()
        if not savefigures:
            self.plt.show()
        else:
            if mode == 'single':
                self.plt.savefig('./view.png', bbox_inches='tight')
            if mode == 'separate':
                for name, figure in self.figures.items():
                    fname = 'view_' + name + '.png'
                    figure.savefig(fname, bbox_inches='tight')
