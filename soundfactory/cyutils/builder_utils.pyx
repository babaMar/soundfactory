#cython: language_level=3
import numpy as np
cimport numpy as np

# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.int
DTYPEI = np.int64
DTYPEF = np.float64

# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.int_t DTYPE_t
ctypedef np.int64_t DTYPEI_t
ctypedef np.float64_t DTYPE_f

cpdef double wn(int n, double freq):
    """Compute the angular frequency"""
    cdef double pi = np.pi
    return (2 * pi * n) * freq


cpdef np.ndarray wn_arr(np.ndarray[DTYPE_t, ndim=1] nterms, double freq):
    cdef int N = nterms.shape[0]
    cdef np.ndarray res = np.zeros([N], dtype=DTYPEF)
    for i in range(N):
        res[i] = wn(i + 1, freq)
    return res


cpdef double to_radians(double degrees):
    cdef double pi = np.pi
    return degrees * (pi / 180)


cpdef double fourier_sum(
        double x,
        np.ndarray[DTYPE_f, ndim=1] coefficients,
        double freq,
        double phase,
        np.ndarray[DTYPE_t, ndim=1] nterms
):
    """Partial sum of the fourier series up to nterms"""
    partial_sums = np.sum(
        coefficients * np.sin(wn_arr(nterms, freq) * x + nterms * to_radians(phase))
    )
    return partial_sums


cpdef np.ndarray upsample_component(
        double amp,
        double phase,
        double duration,
        np.ndarray[DTYPE_f, ndim=1] times,
        np.ndarray[DTYPE_f, ndim=1] coefficients,
        np.ndarray[DTYPE_t, ndim=1] nterms
):
    cdef int N = times.shape[0]
    cdef np.ndarray res = np.zeros([N], dtype=DTYPEF)
    cdef double frequency = 1. / duration
    for i in range(N):
        res[i] = amp * fourier_sum(times[i], coefficients, frequency, phase, nterms)
    return res


cpdef np.ndarray single_component(
        double freq,
        double duration,
        np.ndarray[DTYPE_f, ndim=1] upsampled,
        int samples
):
    cdef double cycles = freq * duration
    cdef np.ndarray sample_range = np.arange(0, samples)
    cdef np.ndarray indexes = np.zeros([samples], dtype=DTYPEI)
    for i in range(samples):
        indexes[i] = round(sample_range[i] * cycles) % samples

    return upsampled[indexes]
