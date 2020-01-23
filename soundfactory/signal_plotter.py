import numpy as np
from matplotlib.ticker import (NullFormatter,
                               LogLocator,
                               NullLocator)

from .signal_base import Signal
from .utils.helpers import above_thr_mask
from .settings.plot import (
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
from .settings.logging_settings import plotterlog
from .utils.labels import (sparse_major_freqs,
                           hz_to_note,
                           log_khz_formatter)


class SignalPlotter(Signal):

    def __init__(self,
                 plotting_interface,
                 input_file,
                 with_envelope=False,
                 fname='view'):
        super().__init__(input_file, with_envelope)

        self.y_label = "{} Channel (t)".format("Mono" if self.MONO else "Left")
        self.x_label = "t [sec]"
        self.plt = plotting_interface
        self.plot_envelope = with_envelope
        self.save_img_prefix = fname
        self.n_figures = 1 if self.MONO else 2
        self.figures = dict()
        self.time_range = np.linspace(0., self.duration, self.samples)

    def _create_figures(self, size=figure_size_single, n_figures=None):
        number_of_figures = self.n_figures if not n_figures else n_figures
        return [next(figure_generator(size=size)) for _ in
                range(number_of_figures)]

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

    @staticmethod
    def _margins(left, right, padding, log=False):
        if log:
            padding = 1 + padding
            a = left / padding
            b = right * padding
        else:
            delta = np.diff([left, right]) * padding
            a = left - delta
            b = right + delta
        return a, b

    def _set_xmargins(self, ax, interval, padding, log=False):
        a, b = self._margins(*interval, padding, log=log)
        ax.set_xlim(a, b)

    def _set_ymargins(self, ax, interval, padding, log=False):
        a, b = self._margins(*interval, padding, log=log)
        ax.set_ylim(a, b)

    def _plot_signal(self, axes, axcolors=None):
        if not axcolors:
            axcolors = [next(colors) for _ in range(self.n_figures)]
        for ax, channel_id, c in zip(axes, self.CHANNELS.keys(), axcolors):
            ax.plot(self.time_range, self.CHANNELS[channel_id], c + '--', lw=0.1)
            if self.plot_envelope:
                envelope_id = channel_id + self.ENVELOPE_SUFFIX
                ax.plot(
                    self.time_range, self.ENVELOPES[envelope_id], 'k-', lw=0.1)
            ax.set_xlim(self.time_range[0], self.time_range[-1])
            ax.set_ylabel(self.y_label, fontproperties=FONT_PROP)
            ax.set_xlabel(self.x_label, fontproperties=FONT_PROP)
            self.y_label = self.y_label.replace('Left', 'Right')

    def _plot_fft(self, axes, axcolors=None):
        if not axcolors:
            axcolors = [next(colors) for _ in range(len(axes))]
        for ax, fft_info, c in zip(axes, self.SPECTRA.values(), axcolors):
            ax.plot(fft_info[self.FREQUENCIES], fft_info[self.POWERS], c + "-")
            ax.set_xlabel("Frequency [kHz]", fontproperties=FONT_PROP)
            ax.set_ylabel("Power(f)", fontproperties=FONT_PROP)

    def _plot_spectrogram(self, axes, wmsec=0.005):
        npoints = int(self.sampling_rate * wmsec)
        overlap = int(self.sampling_rate * wmsec / 2.)
        for ax, channel, in zip(axes, self.CHANNELS.values()):
            Pxx, freqs, bins, im = ax.specgram(
                channel, NFFT=npoints, Fs=self.sampling_rate,
                noverlap=overlap, cmap=self.plt.cm.jet)
            ax.set_xlabel(self.x_label, fontproperties=FONT_PROP)
            ax.set_ylabel("Frequency [kHz]", fontproperties=FONT_PROP)
            ax.set_ylim(20., 20000.)
            ax.set_yscale('log')
            self._setup_log_decimals_labels(ax.yaxis, subs=[.2, .4])

    def _get_ticks_labels(self, ax, threshold=0.1, close_tolerance=0.1):
        data = ax.lines[0].get_data()
        freqs, pws = data
        major_freqs = sparse_major_freqs(
            freqs, pws, threshold=threshold, close_tolerance=close_tolerance)
        major_labels = {hz_to_note(x): x for x in major_freqs[::-1]}
        x_labels = list(major_labels.keys())
        x_ticks = list(major_labels.values())
        return x_ticks, x_labels

    def _pws_labels(
            self, ax, x_ticks, x_labels, log_y=False):
        ax.set_xscale("log")
        ax.set_yscale("{}".format("log" if log_y else "linear"))
        ax2 = ax.twiny()

        ax2.set_xlim(ax.get_xlim())
        self._setup_log_decimals_labels(ax.xaxis)
        self.plt.setp(ax.get_xticklabels() +
                      ax.xaxis.get_minorticklabels(), rotation=45)
        ax2.set_xscale("log")
        ax2.set_xticks(x_ticks)
        ax2.set_xticklabels(x_labels, rotation=45, fontproperties=FONT_PROP)
        ax2.xaxis.set_minor_locator(NullLocator())
        ax2.xaxis.set_minor_formatter(NullFormatter())

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
            fig = self._create_figures(size=figure_size_full, n_figures=1)[0]
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
                x_ticks, x_labels = self._get_ticks_labels(
                    ax,
                    threshold=threshold,
                    close_tolerance=close_tolerance
                )
                self._pws_labels(
                    ax, x_ticks, x_labels,
                    log_y=log_pws)
        else:
            for ax in fft_axes:
                x_ticks, x_labels = self._get_ticks_labels(
                    ax,
                    threshold=threshold,
                    close_tolerance=close_tolerance
                )
                self._set_xmargins(
                    ax, (min(x_ticks), max(x_ticks)), PLOT_MARGIN, log=True)
                self._pws_labels(
                    ax, x_ticks, x_labels,
                    log_y=log_pws)

        self.plt.tight_layout()
        if not savefigures:
            self.plt.show()
        else:
            if mode == 'single':
                img_file_name = './' + self.save_img_prefix + '.png'
                self.plt.savefig(img_file_name, bbox_inches='tight')
            if mode == 'separate':
                for name, figure in self.figures.items():
                    img_file_name = './' + self.save_img_prefix + '_' + name + '.png'
                    figure.savefig(img_file_name, bbox_inches='tight')
