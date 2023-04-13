import numpy as np
import sympy
import matplotlib.pyplot as plt

# Служебные переменные
LAST_FIGURE_NUMBER = 0

# Константы
i = complex(0, 1)
pi = np.pi

# Данные по варианту
t_0 = 0.25
T = 0.25
t_i = 1.25
t_p = 2
f = 1
fi_0 = 7 * np.pi/ 4

n_i = t_i / T
n_p = t_p / T
n_0 = t_0 / T

# Построение фигуры
def make_figure() -> plt.figure:
    """Возвращает объект для нового графика."""
    global LAST_FIGURE_NUMBER
    LAST_FIGURE_NUMBER += 1
    return plt.figure(LAST_FIGURE_NUMBER)

# Расчет бабочки в номере 3
def butterfly_right(seq):
    """ Расчет методом бабочки фурье при прореживании справа."""
    print("============ Расчет бабочки при прореживании справа (задание 3) ============")
    i = complex(0, 1)
    E = np.exp(-1 * i * (np.pi / 4))
    e_values = [E**0, E**1, E**2, E**3]
    print(f"Stage 0:")
    print(seq)

    stage_1 = [0]*8
    calculate_butterfly_section_right(seq, stage_1, 0, 4, e_values, 0) # Размер берется в 2 раза меньше, так-как крест-накрест
    stage_1_rounded = np.real_if_close(np.around(stage_1, decimals=3), tol=10)
    print("stage 1 results:")
    print(stage_1_rounded)

    stage_2 = [0]*8
    e_values = [E**0, E**2, E**0, E**2]

    for i in range(0, 8, 4):
        calculate_butterfly_section_right(stage_1, stage_2, i, 2, e_values, int(i/2))
    stage_2_rounded = np.real_if_close(np.around(stage_2, decimals=3), tol=10)
    print("stage 2 results:")
    print(stage_2_rounded)


    stage_3 = [0]*8
    e_values = [E ** 0, E ** 0, E ** 0, E ** 0]
    for i in range(0, 8, 2):
        calculate_butterfly_section_right(stage_2, stage_3, i, 1, e_values, int(i/2))
    stage_3_rounded = np.real_if_close(np.around(stage_3, decimals=3), tol=10)
    print("stage 3 results:")
    print(stage_3_rounded)

    return stage_3_rounded

def butterfly_left(seq):
    """ Расчет методом бабочки фурье при прореживании слева."""
    print("============ Расчет бабочки при прореживании слева (задание 4) ============")
    i = complex(0, 1)
    E = np.exp(-1 * i * (np.pi / 4))
    print(f"Stage 0:")
    print(seq)

    stage_1 = [0] * 8
    e_values = [E ** 0, E ** 0, E ** 0, E ** 0]
    for i in range(0, 8, 2):
        calculate_butterfly_section_left(seq, stage_1, i, 1, e_values, int(i/2))
    stage_1_rounded = np.real_if_close(np.around(stage_1, decimals=3), tol=10)
    print("stage 1 results:")
    print(stage_1_rounded)

    stage_2 = [0] * 8
    e_values = [E ** 0, E ** -2, E ** 0, E ** -2]
    for i in range(0, 8, 4):
        calculate_butterfly_section_left(stage_1, stage_2, i, 2, e_values, int(i / 2))
    stage_2_rounded = np.real_if_close(np.around(stage_2, decimals=3), tol=10)
    print("stage 2 results:")
    print(stage_2_rounded)

    stage_3 = [0]*8
    e_values = [E ** 0, E ** -1, E ** -2, E ** -3]
    calculate_butterfly_section_left(stage_2, stage_3, 0, 4, e_values, 0)
    stage_3_rounded = np.real_if_close(np.around(stage_3, decimals=3), tol=10)
    print("stage 3 results:")
    print(stage_3_rounded)

    return stage_3_rounded


def calculate_butterfly_section_right(base_column: list, new_column: list,
                                      section_start: int, size: int, e_values:list, cntr):
    """ Расчет секции для бабочки фурье при прореживании справа."""
    e_counter = cntr
    for i in range(section_start, section_start + size):
        new_column[i] = base_column[i] + base_column[i + size]
        new_column[i + size] = (base_column[i] - base_column[i + size])*e_values[e_counter]
        e_counter += 1

def calculate_butterfly_section_left(base_column: list, new_column: list,
                                      section_start: int, size: int, e_values:list, cntr):
    """ Расчет секции для бабочки фурье при прореживании слева."""
    e_counter = cntr
    for i in range(section_start, section_start + size):
        print(i)
        new_column[i] = (base_column[i] + base_column[i + size] *  e_values[e_counter])
        new_column[i + size] = base_column[i] - base_column[i + size] *  e_values[e_counter]
        e_counter += 1


if __name__ == '__main__':
    # Task 3
    n = sympy.symbols('n')
    sg = sympy.cos(2*pi*f*n*T + fi_0) + i * sympy.sin(2*pi*f*n*T + fi_0)
    zeros = (0, 6, 7)
    data = []
    for i in range(8):
        if i in zeros:
            data.append(0)
        else:
            value = sg.subs(n, i)
            Re, Im = value.as_real_imag()
            data.append(complex(round(Re, 3), round(Im, 3)))

    bpf_result_no_ordered = butterfly_right(data)
    order = [0, 4, 2, 6, 1, 5, 3, 7]
    bpf_result = []
    print(f"Неотсортированные данные: {bpf_result_no_ordered}")
    for order_index in order:
        bpf_result.append(bpf_result_no_ordered[order_index])
    print(f"Упорядоченные данные: {bpf_result}")

    re_values = []
    im_values = []
    amps = []

    for value in bpf_result:
        re_values.append(value.real)
        im_values.append(value.imag)
        amps.append(np.sqrt(value.real**2 + value.imag**2))
    phases = np.angle(list(map(complex, bpf_result)))

    print(f"Re values: {re_values}")
    print(f"Im values: {im_values}")
    print(f"Amps: {list(map(lambda x: round(x, 2), amps))}")
    print(f"Phases: {phases}")
    fig = make_figure()
    plt.plot(np.arange(0, 8), re_values)
    plt.title("Re part of signal")

    fig1 = make_figure()
    plt.plot(np.arange(0, 8), im_values)
    plt.title("Im part of signal")

    fig2 = make_figure()
    for i in range(8):
        plt.vlines(i, 0, amps[i], colors='r')

    fig3 = make_figure()
    for i in range(8):
        plt.vlines(i, 0, phases[i], colors='r')
    plt.yticks(np.arange(-1 * np.pi, 2 * np.pi, np.pi), [str(i) + "π" for i in range(-1, 2)])

    print(bpf_result_no_ordered)
    obpf_result = butterfly_left(bpf_result_no_ordered)

    re_values.clear()
    im_values.clear()
    for value in obpf_result:
        re_values.append(value.real)
        im_values.append(value.imag)

    print(f"Re values: {re_values}")
    print(f"Im values: {im_values}")

    fig4 = make_figure()
    for i in range(8):
        plt.vlines(i, 0, re_values[i], colors='r')
    plt.title("Re values after OBPF")

    fig5 = make_figure()
    for i in range(8):
        plt.vlines(i, 0, im_values[i], colors='r')
    plt.title("Im values after OBPF")

    plt.show()




