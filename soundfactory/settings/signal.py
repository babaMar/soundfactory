import numpy as np

alternate_minus_odd = lambda x: (-1.0) ** ((x.astype(complex) - 1) / 2)

real_part_or_zero_otherwise = lambda x: np.where(np.isreal(x), x, 0).real


B_N_COEFF_MAP = {
    "sine": lambda x: np.where(x == 1, 1.0, 0),
    "sawtooth": lambda x: -2.0 / (np.pi * x),
    "square": lambda x: np.where(x % 2 == 1, 4.0 / (np.pi * x), 0),
    "triangle": lambda x: real_part_or_zero_otherwise(alternate_minus_odd(x))
    * (8.0 / (np.pi * x) ** 2),
}
