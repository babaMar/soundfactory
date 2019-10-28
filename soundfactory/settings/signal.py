from numpy import pi, where, complex, isreal

alternate_minus_odd = lambda x: (-1.)**((x.astype(complex) - 1)/2)

real_part_or_zero_otherwise = lambda x: where(isreal(x), x, 0).real


B_N_COEFF_MAP = {
    'sine': lambda x: where(x == 1, 1., 0),
    'sawtooth': lambda x: - 2./(pi * x),
    'square': lambda x: where(x % 2 == 1, 4./(pi * x), 0),
    'triangle': lambda x: where(x % 2 == 1, real_part_or_zero_otherwise(alternate_minus_odd(x)) * (8./(pi * x)**2), 0)
}
