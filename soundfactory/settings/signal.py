from numpy import pi, where


alternate_minus_odd = lambda x: (-1.)**((x - 1)/2)


alternate_minus = lambda x: (-1.)**(x + 1)


B_N_COEFF_MAP = {
    'sine': lambda x: where(x == 1, 1., 0),
    'sawtooth': lambda x: - 2./(pi * x),
    'square': lambda x: where(x % 2 == 1, 4./(pi * x), 0),  # if x % 2 != 0 else 0,
    'triangle': lambda x: where(x % 2 == 1, alternate_minus_odd(x) * (8./(pi * x)**2), 0)  # if x % 2 != 0 else 0,
}
