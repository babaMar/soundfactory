import numpy as np
import time
from numba import jit
import matplotlib.pyplot as plt

TIME_DOMAIN = np.linspace(0., 1., 44100, endpoint=False)


@jit(nopython=True)
def wn(n, freq):
    # Return the w_n angular frequency
    omega_n = (2 * np.pi * n) * freq
    return omega_n


@jit(nopython=True)
def alternate_minus_odd(x): 
    return (-1.)**((x - 1)/2)


@jit(nopython=True)
def BN(x):
    return alternate_minus_odd(x) * (8./(np.pi * x)**2) if x % 2 != 0 else 0


@jit(nopython=True)
def _sum_sync(x, freq, N=100):
    t = 0
    n = 1
    while n < N + 1:
        t += BN(n)*np.sin(wn(n, freq) * x)
        n += 1
    return t


@jit
def _signal(freq, N=100, samples=44100):
    real_time = time.time()
    time_range = np.linspace(0., 1., samples, endpoint=False)
    res = [_sum_sync(_t, freq, N=N) for _t in time_range]
    real_time = (time.time() - real_time)
    print("Sum for {} terms. Elapsed time: {} s".format(N, round(real_time), 3))
    return np.asarray(res, dtype=np.float32)


if __name__ == '__main__':
    for n_terms in (100, 1000, 10000, 100000):
        s =  _signal(2., N=n_terms)
        plt.plot(TIME_DOMAIN, s)
    plt.show()

