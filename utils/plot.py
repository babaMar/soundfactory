from settings.plot import plt, default_size


def time_domain_signal(time_array, signal_arrays, tmin=0., tmax=1.):
    if not isinstance(signal_arrays, list):
        raise Exception('Second positional argument must be list of arrays')
    fig = plt.figure(figsize=default_size)
    ax = fig.add_subplot(111)
    for signal_array in signal_arrays:
        ax.plot(time_array, signal_array, lw=1)
    ax.set_ylabel(r"$\mathrm{Audio~Mono}~(t)$")
    ax.set_xlabel(r"$t~~\mathrm{[sec]}$")
    ax.set_xlim(tmin, tmax)
    plt.show()
