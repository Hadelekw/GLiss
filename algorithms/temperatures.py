import sys
import math
import matplotlib.pyplot as plt


def temperature_update_a(current_temperature : float,
                         cooling_rate : float) -> float:
    return current_temperature * cooling_rate


def temperature_update_b(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return initial_temperature - step * ((final_temperature - initial_temperature) / total_steps)


def temperature_update_c(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return initial_temperature * (final_temperature / initial_temperature)**(step / total_steps)


def temperature_update_d(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    A = ((initial_temperature - final_temperature) * (total_steps + 1)) / total_steps
    return A / (step + 1) + initial_temperature - A


def temperature_update_e(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    A = math.log(initial_temperature - final_temperature) / math.log(total_steps)
    return initial_temperature + step**A


def temperature_update_f(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return (initial_temperature - final_temperature) / (1 + math.exp(0.3 * (step - total_steps // 2))) + final_temperature


def temperature_update_g(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return 0.5 * (initial_temperature - final_temperature) * (1 + math.cos(step * math.pi // total_steps)) + final_temperature


def temperature_update_h(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return 0.5 * (initial_temperature - final_temperature) * (1 - math.tanh(10 * step // total_steps - 5)) + final_temperature


def temperature_update_i(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return (initial_temperature - final_temperature) / (math.cosh(10 * step // total_steps)) + final_temperature


def temperature_update_j(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return initial_temperature * math.exp(-(step/total_steps) * math.log(initial_temperature/final_temperature))


def temperature_update_k(initial_temperature : float,
                         final_temperature : float,
                         step : int,
                         total_steps : int) -> float:
    return initial_temperature * math.exp(-(step/total_steps)**2 * math.log(initial_temperature/final_temperature))


TEMPERATURE_UPDATE_MAP = {
    'a': temperature_update_a,
    'b': temperature_update_b,
    'c': temperature_update_c,
    'd': temperature_update_d,
    'e': temperature_update_e,
    'f': temperature_update_f,
    'g': temperature_update_g,
    'h': temperature_update_h,
    'i': temperature_update_i,
    'j': temperature_update_j,
    'k': temperature_update_k,
}


def main(method_identifier : str) -> None:
    values = range(101)
    if method_identifier == 'all':
        for i, func in enumerate(list(TEMPERATURE_UPDATE_MAP.values())):
            if not i:
                plt.plot(values, [math.exp(-1/func(100, 0.9)) for v in values], label=func.__name__[-1])
            else:
                plt.plot(values, [math.exp(-1/func(100, 1, v, 100)) for v in values], label=func.__name__[-1])
        plt.legend()
    else:
        func = TEMPERATURE_UPDATE_MAP[method_identifier]
        if method_identifier == 'a':
            plt.plot(values, [math.exp(-1/func(100, 0.9)) for v in values])
        else:
            plt.plot(values, [math.exp(-1/func(100, 1, v, 100)) for v in values])
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1])
