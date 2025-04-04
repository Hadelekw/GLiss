import math
import matplotlib.pyplot as plt
import sys

sys.path.append('../')


from algorithms import temperatures, sa_settings


FUNCTIONS = ['a', 'c', 'k']


LINE_STYLES = ['k-', 'k:', 'k--']


def main() -> None:
    fig, axes = plt.subplots(ncols=2)
    axes[0].set_xlabel('Iteration number [n]')
    axes[0].set_ylabel('Temperature parameter value')
    axes[0].set_title('(a)', fontsize=16)
    axes[0].set_aspect(10)
    axes[1].set_xlabel('Iteration number [n]')
    axes[1].set_ylabel('Solution acceptance probability')
    axes[1].set_title('(b)', fontsize=16)
    axes[1].set_aspect(1000)
    x = range(sa_settings.NUMBER_OF_ITERATIONS)
    for style, function_identifier in zip(LINE_STYLES, FUNCTIONS):
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
            y = []
            ts = [func(sa_settings.INITIAL_TEMPERATURE, sa_settings.FINAL_TEMPERATURE, i, sa_settings.NUMBER_OF_ITERATIONS) for i in x]
            for t in ts:
                if t:
                    y.append(math.exp(-1/t))
                else:
                    y.append(0)
        axes[0].plot(x, ts, style)
        axes[1].plot(x, y, style)
    axes[0].legend(['A', 'B', 'C'])
    axes[1].legend(['A', 'B', 'C'])
    plt.show()


if __name__ == '__main__':
    main()
