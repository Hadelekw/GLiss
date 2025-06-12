import math
import random
import numpy as np


def emg(x : float,
        m : float,
        s : float,
        l : float) -> float:
    return (l / 2) * math.exp((l / 2) * (2 * m  + l * s**2 - 2 * x)) *\
        erfc((m + l * s**2 - x) / (math.sqrt(2) * s))


def alt_emg(x : float,
            m : float,
            s : float,
            t : float) -> float:
    return (s / t) * math.sqrt(math.pi / 2) * math.exp((s / t)**2 / 2 - ((x - m) / t)) *\
        erfc((1 / math.sqrt(2)) * (s / t - (x - m) / s))


def erf(x) -> float:
    def func(x) -> float:
        return 1 - 1 / ((1 + 0.278393 * x + 0.230389 * x**2 + 0.000972 * x**3 + 0.078108 * x**4)**4)
    return func(x) if x > 0 else -func(-x)


# def erf(x) -> float:
#     def func(x) -> float:
#         a1 = 0.0705230784
#         a2 = 0.0422820123
#         a3 = 0.0092705272
#         a4 = 0.0001520143
#         a5 = 0.0002765672
#         a6 = 0.0000430638
#         return 1 - 1 / ((1 + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4 + a5 * x**5 + a6 * x**6))
#     return func(x) if x > 0 else -func(x)


def erfc(x) -> float:
    return 1 - erf(x)


def get_reaction_time_probability(t : float) -> float:
    return alt_emg(t, 4, 0.5, 1.5)


def sample_reaction_times(n : int,
                          boundary : float = 10) -> list:
    x = np.arange(1, boundary)
    # Probabilities from (Whelan, 2008)
    p = np.array([alt_emg(i, 4, 0.5, 1.5) for i in x])
    result = np.random.choice(x, p=p)
    return [0, result]
