
#────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#─████████████───██████████████─██████████████────██████████████─██████████████─██████████████─██████─────────██████████████─
#─██░░░░░░░░████─██░░░░░░░░░░██─██░░░░░░░░░░██────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─
#─██░░████░░░░██─██░░██████████─██░░██████░░██────██████░░██████─██░░██████░░██─██░░██████░░██─██░░██─────────██░░██████████─
#─██░░██──██░░██─██░░██─────────██░░██──██░░██────────██░░██─────██░░██──██░░██─██░░██──██░░██─██░░██─────────██░░██─────────
#─██░░██──██░░██─██░░██████████─██░░██████░░██────────██░░██─────██░░██──██░░██─██░░██──██░░██─██░░██─────────██░░██████████─
#─██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██────────██░░██─────██░░██──██░░██─██░░██──██░░██─██░░██─────────██░░░░░░░░░░██─
#─██░░██──██░░██─██████████░░██─██░░██████████────────██░░██─────██░░██──██░░██─██░░██──██░░██─██░░██─────────██████████░░██─
#─██░░██──██░░██─────────██░░██─██░░██────────────────██░░██─────██░░██──██░░██─██░░██──██░░██─██░░██─────────────────██░░██─
#─██░░████░░░░██─██████████░░██─██░░██────────────────██░░██─────██░░██████░░██─██░░██████░░██─██░░██████████─██████████░░██─
#─██░░░░░░░░████─██░░░░░░░░░░██─██░░██────────────────██░░██─────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─
#─████████████───██████████████─██████────────────────██████─────██████████████─██████████████─██████████████─██████████████─
#────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

import numpy as np
import sympy
import matplotlib.pyplot as plt

# Made for dsp tests
# Current version: 09.05.23

# Константы
I = complex(0, 1)
pi = np.pi

# Служебные переменные
LAST_FIGURE_NUMBER = 0

def make_figure() -> plt.figure:
    """Возвращает объект для нового графика."""
    global LAST_FIGURE_NUMBER
    LAST_FIGURE_NUMBER += 1
    return plt.figure(LAST_FIGURE_NUMBER)


def round_comlex_values_array(data_array: list) -> list:
    """Округляет значения массива."""
    rounded_data_array = []
    for sample in data_array:
        re = float(complex(sample).real)
        im = float(complex(sample).imag)
        rounded_data_array.append(round(re, 3) +  I*round(im , 3))
    return rounded_data_array


def calculate_butterfly_section_right(base_column: list, new_column: list,
                                      section_start: int, size: int, e_values:list, cntr):
    """ Расчет секции для бабочки фурье при прореживании справа."""
    e_counter = cntr
    for index in range(section_start, section_start + size):
        new_column[index] = base_column[index] + base_column[index + size]
        new_column[index + size] = (base_column[index] - base_column[index + size])*e_values[e_counter]
        e_counter += 1

def calculate_butterfly_section_left(base_column: list, new_column: list,
                                      section_start: int, size: int, e_values:list, cntr):

    """ Расчет секции для бабочки фурье при прореживании слева."""
    e_counter = cntr
    for index in range(section_start, section_start + size):
        new_column[index] = (base_column[index] + base_column[index + size] *  e_values[e_counter])
        new_column[index + size] = base_column[index] - base_column[index + size] *  e_values[e_counter]
        e_counter += 1

def butterfly_left(seq):
    """ Расчет методом бабочки фурье при прореживании слева."""
    print("===============Left butterfly started.=================")
    i = complex(0, 1)
    E = np.exp(-1 * i * (np.pi / 4))
    print(f"Stage 0:")
    print(seq)

    stage_1 = [0] * 8
    e_values = [E ** 0, E ** 0, E ** 0, E ** 0]
    for i in range(0, 8, 2):
        calculate_butterfly_section_left(seq, stage_1, i, 1, e_values, int(i/2))
    stage_1_rounded = round_comlex_values_array(stage_1)
    print("stage 1 results:")
    print(stage_1_rounded)

    stage_2 = [0] * 8
    e_values = [E ** 0, E ** -2, E ** 0, E ** -2]
    for i in range(0, 8, 4):
        calculate_butterfly_section_left(stage_1, stage_2, i, 2, e_values, int(i / 2))
    stage_2_rounded = round_comlex_values_array(stage_2)
    print("stage 2 results:")
    print(stage_2_rounded)

    stage_3 = [0]*8
    e_values = [E ** 0, E ** -1, E ** -2, E ** -3]
    calculate_butterfly_section_left(stage_2, stage_3, 0, 4, e_values, 0)
    stage_3_rounded = round_comlex_values_array(stage_3)
    print("stage 3 results:")
    print(stage_3_rounded)

    print("===============Left butterfly ended.=================")

    return stage_3_rounded


def butterfly_right(seq):
    """ Расчет методом бабочки фурье при прореживании справа."""
    print("===============Right butterfly started.=================")
    E = sympy.exp(-1 * I* (np.pi / 4))
    e_values = [E**0, E**1, E**2, E**3]
    print(f"Stage 0:")
    print(seq)

    stage_1 = [0]*8
    calculate_butterfly_section_right(seq, stage_1, 0, 4, e_values, 0) # Размер берется в 2 раза меньше, так-как крест-накрест
    stage_1_rounded = round_comlex_values_array(stage_1)
    print("stage 1 results:")
    print(stage_1_rounded)

    stage_2 = [0]*8
    e_values = [E**0, E**2, E**0, E**2]

    for i in range(0, 8, 4):
        calculate_butterfly_section_right(stage_1, stage_2, i, 2, e_values, int(i/2))
    stage_2_rounded = round_comlex_values_array(stage_2)
    print("stage 2 results:")
    print(stage_2_rounded)


    stage_3 = [0]*8
    e_values = [E ** 0, E ** 0, E ** 0, E ** 0]
    for i in range(0, 8, 2):
        calculate_butterfly_section_right(stage_2, stage_3, i, 1, e_values, int(i/2))
    stage_3_rounded = round_comlex_values_array(stage_3)
    print("stage 3 results:")
    print(stage_3_rounded)

    print("===============Right butterfly ended.=================")

    return stage_3_rounded


