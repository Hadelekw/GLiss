import math
import matplotlib.pyplot as plt
import sys

sys.path.append('../')


from algorithms import temperatures, sa_settings


FUNCTIONS = ['a', 'c', 'k']


def main() -> None:
    x = range(sa_settings.NUMBER_OF_ITERATIONS)
    for function_identifier in FUNCTIONS:
        func = temperatures.TEMPERATURE_UPDATE_MAP[function_identifier]
        if function_identifier == 'a':
            ts = []
            for i in x:
                if ts:
                    ts.append(func(ts[-1], sa_settings.COOLING_RATE))
                else:
                    ts.append(func(sa_settings.INITIAL_TEMPERATURE, sa_settings.COOLING_RATE))
            y = [math.exp(-1/t) for t in ts]
        else:
            y = [math.exp(-1/func(sa_settings.INITIAL_TEMPERATURE, sa_settings.FINAL_TEMPERATURE, i, sa_settings.NUMBER_OF_ITERATIONS)) for i in x]
        plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()
