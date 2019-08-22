import numpy as np
from settings.plot import (plt,
                           figure_size_single,
                           figure_size_double,
                           figure_generator,
                           colors,
                           TONE_FREQ_MAP)


class SignalPlotter(object):

    def __init__(self, l_signal,
                 l_signal_envelope=(),
                 r_signal=(),
                 r_signal_envelope=(),
                 sampling_rate=44100,
                 plot_envelope=False):

        # Mono signal is treated as left only
        self.left_raw = l_signal
        self.plot_envelope = plot_envelope
        self.y_label = "Mono~Channel (t)"
        self.x_label = "[sec]"

        if any(l_signal_envelope):
            self.left_envelope = l_signal_envelope
            self.envelopes = [self.left_envelope]
            self.i_env = 0

        self.n_figures = 1
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

    def _plot_signal(self):
        figures = self._create_figures()
        axes = [f.add_subplot(111) for f in figures]

        for ax, channel in zip(axes, self.channels):
            c = next(colors)
            ax.plot(self.time_range, channel, c + '--', lw=0.1)
            if self.plot_envelope:
                ax.plot(self.time_range, self.envelopes[self.i_env], 'k-', lw=0.1)
                self.i_env += 1
            ax.set_ylabel(self.y_label)
            ax.set_xlabel(self.x_label)
            self.y_label = self.y_label.replace('Left', 'Right')

    def _plot_spectrogram(self, wmsec=0.005):
        figures = self._create_figures(size=figure_size_double)
        axes = [f.add_subplot(111) for f in figures]
        npoints = int(self.sampling_rate * wmsec)
        overlap = int(self.sampling_rate * wmsec / 2.)
        tone_freqs = [v for v in TONE_FREQ_MAP.values()]
        tone_names = [k for k in TONE_FREQ_MAP.keys()]
        for ax, channel, in zip(axes, self.channels):
            Pxx, freqs, bins, im = \
                ax.specgram(channel, NFFT=npoints, Fs=self.sampling_rate, noverlap=overlap, cmap=plt.cm.jet)
            ax.set_xlabel(self.x_label)
            ax.set_ylabel("Frequency [Hz]")
            ax.set_ylim(20., 20000.)
            ax.set_yscale('log')
            # TODO only label ticks for values that are present in the spectrum, not readable otherwise
            # Calculate FFT and pass find dominant frequencies
            ax.set_yticks(tone_freqs)
            ax.set_yticklabels(tone_names)

    def _set_xlim(self, left=None, right=None):
        figures = list(map(plt.figure, plt.get_fignums()))
        for fig in figures:
            axes = fig.get_axes()
            for ax in axes:
                ax.set_xlim(left, right)

    def show(self, wmsec=1, start=None, end=None):
        # TODO define figures here and pass to class methods
        self._plot_signal()
        self._plot_spectrogram(wmsec=wmsec)
        if any([start, end]):
            self._set_xlim(start, end)
        plt.show()
