import numpy as np
import sympy
import matplotlib.pyplot as plt
import time

# Служебные переменные
LAST_FIGURE_NUMBER = 0

def make_figure() -> plt.figure:
    """Возвращает объект для нового графика."""
    global LAST_FIGURE_NUMBER
    LAST_FIGURE_NUMBER += 1
    return plt.figure(LAST_FIGURE_NUMBER)

# Константы
I = complex(0, 1)
pi = np.pi

# Данные по варианту
fi_0 = pi
f_dp_T = 0.125
df_T = 0.5
N_i = 4

# fi_0 = 7 * pi / 4
# f_dp_T = 0.125
# df_T = 0.5
# N_i = 4

def round_comlex_values_array(data_array: list) -> list:
    """Округляет значения массива."""
    rounded_data_array = []
    for sample in data_array:
        Re, Im = sample.as_real_imag()
        rounded_data_array.append(round(Re, 3) +  round(Im * I, 3))
    return rounded_data_array

def butterfly_right(seq):
    """ Расчет методом бабочки фурье при прореживании справа."""
    print("===============Butterfly started.=================")
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

    print("===============Butterfly ended.=================")

    return stage_3_rounded

def butterfly_left(seq):
    """ Расчет методом бабочки фурье при прореживании слева."""
    print("===============Butterfly started.=================")
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

    print("===============Butterfly ended.=================")

    return stage_3_rounded

def calculate_butterfly_section_right(base_column: list, new_column: list,
                                      section_start: int, size: int, e_values:list, cntr):
    """ Расчет секции для бабочки фурье при прореживании справа."""
    e_counter = cntr
    for index in range(section_start, section_start + size):
        new_column[index] = (base_column[index] + base_column[index + size]).evalf()
        new_column[index + size] = ((base_column[index] - base_column[index + size])*e_values[e_counter]).evalf()
        e_counter += 1
def calculate_butterfly_section_left(base_column: list, new_column: list,
                                      section_start: int, size: int, e_values:list, cntr):

    """ Расчет секции для бабочки фурье при прореживании слева."""
    e_counter = cntr
    for index in range(section_start, section_start + size):
        new_column[index] = (base_column[index] + base_column[index + size] *  e_values[e_counter])
        new_column[index + size] = base_column[index] - base_column[index + size] *  e_values[e_counter]
        e_counter += 1

if __name__ == "__main__":
    # Task 1
    n = sympy.symbols('n')
    A = (df_T / N_i)
    B = 2 * f_dp_T - df_T
    C = - f_dp_T * N_i + fi_0 / pi
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"C = {C}")
    An2_Bn_C = A*n**2 + B*n + C
    An2_Bn_C_data = []

    for i in range(4):
        An2_Bn_C_data.append(round(An2_Bn_C.subs(n, i), 5))
    print(f"An^2 + Bn + C data: {An2_Bn_C_data}")
    mul_pi_data = []

    for data in An2_Bn_C_data:
        mul_pi_data.append(round(data * sympy.pi, 2))
    print(f"*pi data: {mul_pi_data}")

    signal_cos_data = []
    signal_sin_data = []
    for data in mul_pi_data:
        signal_cos_data.append(round(sympy.cos(data), 2))
        signal_sin_data.append(round(sympy.sin(data), 2))
    print(f"Cos data: {signal_cos_data}")
    print(f"Sin data: {signal_sin_data}")

    # Опорная функция
    f_dp_T = 0
    fi_0 = 0
    v = sympy.symbols('v')
    A = df_T / N_i
    B = - df_T
    C = 0
    print(f"A: {A}, B: {B}, C: {C}")
    Av2_Bv = A*v**2 + B*v
    Av2_Bv_s_data = []
    for i in range(4):
        Av2_Bv_s_data.append(round(Av2_Bv.subs(v, i), 3))

    mul_pi_Av2_Bv_s_data = []
    for data in Av2_Bv_s_data:
        mul_pi_Av2_Bv_s_data.append(round(data * pi, 3))

    h_cos_data = []
    h_sin_data = []

    for data in mul_pi_Av2_Bv_s_data:
        h_cos_data.append(round(sympy.cos(data), 2))
        h_sin_data.append(-round(sympy.sin(data), 2))

    print(f"Av2_Bv data: {Av2_Bv_s_data}")
    print(f"*pi data: {mul_pi_Av2_Bv_s_data}")
    print(f"cos data: {h_cos_data}")
    print(f"sin data: {h_sin_data}")

    # Task 4
    signal_data_to_butterfly = []
    h_data_to_butterfly = []

    for data_index in range(4):
        signal_data_to_butterfly.append(signal_cos_data[data_index] + I * signal_sin_data[data_index])
        h_data_to_butterfly.append(h_cos_data[3 - data_index] + I * h_sin_data[3 - data_index])
    for _ in range(4):
        signal_data_to_butterfly.append(0) # Заполняем оставшиеся отсчеты нулями
        h_data_to_butterfly.append(0)

    print(f"Данные в бабочку 1: {signal_data_to_butterfly}")
    signal_data_butterfly_result = butterfly_right(signal_data_to_butterfly)

    print(f"Данные в бабочку 2: {h_data_to_butterfly}")
    h_data_butterfly_result = butterfly_right(h_data_to_butterfly)

    multiplied_array = round_comlex_values_array([signal_data_butterfly_result[i] * h_data_butterfly_result[i] for i in range(8)])
    print(f"Результат умножения: {multiplied_array}")

    # indexes = [0, 4, 2, 6, 1, 5, 3, 7]

    # obpf_data_input = []
    # for index in indexes:
    #     obpf_data_input.append(multiplied_array[index])

    print(f"Данные на вход ОБПФ: {multiplied_array}")

    obpf_result = np.array(butterfly_left(multiplied_array)) / 8
    print(obpf_result)

    obpf_amps_result = [] # Найдем амплитуды сигнала
    for obpf_data_sample in obpf_result:
        Re, Im = obpf_data_sample.as_real_imag()
        print(Re**2 + Im**2)
        obpf_amps_result.append(sympy.sqrt(Re**2 + Im**2))

    print(f"Результирующие амплитуды: {obpf_amps_result}")