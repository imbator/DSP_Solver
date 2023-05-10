import numpy as np
import sympy
import matplotlib.pyplot as plt
from dsp_tools import  make_figure, butterfly_left, butterfly_right
# Test 6 solution generator.
# Telegram: @imbator
# Version from 09.05.23.

# Данные по варианту:
N = 8
dF_T = 0.43
filter_selection = [0, 1, 1, 1, 0, -1 ,-1 ,-1, 0]

# Служебные переменные
I = complex(0, 1)
pi = np.pi
x_axis_range = np.arange(0, 8)
filter_obpf_order = [0, 4, 2, 6, 1, 5, 3, 7]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['blue'])

def order_filter(filter_values) -> list:
    filter_values_ordered = []
    for order_index in filter_obpf_order:
        filter_values_ordered.append(filter_values[order_index])
    return filter_values_ordered


def amplitude_phase_characteristic_approximate(filter_sel) -> None:
    """Задание 1.
    Аппроксимация амплитудно-частотной характеристики."""
    print("+=====================================+")
    print("Задание 1. Аппроксимация амплитудно-частотной характеристики.")
    make_figure()
    plt.plot()
    print(filter_selection)
    for i in range(len(x_axis_range)):
        plt.vlines(x_axis_range[i], 0, filter_sel[i])
    plt.title(f"{filter_selection} Re характеристика")
    plt.grid('on')
    print("График Im части - все нули для всех X при любом типе фильтра.")


def filter_obpf_calculate(filter_sel) -> list:
    """Вычисление обпф для заданного фильтра (прореживание слева)."""
    print("+=====================================+")
    print("Задание 2. Вычисление обпф для заданного фильтра (прореживание слева).")
    filter_obpf = []

    for order_index in filter_obpf_order:
        filter_obpf.append(filter_sel[order_index])
    obpf_filter_result = butterfly_left(filter_obpf)
    obpf_filter_result = np.array(obpf_filter_result) / 8
    print(f"Результат ОБПФ: {list(obpf_filter_result)}")

    make_figure()
    plt.plot(x_axis_range, [value.real for value in obpf_filter_result], '-o')
    plt.title("Импульсная характеристика")
    plt.grid('on')

    return obpf_filter_result


def calculate_n_f(filter_values):
    """Расчет N_f и построение обратной бабочки с занулением."""
    print("+=====================================+")
    print("Задание 3. Расчет N_f и построение обратной бабочки с занулением.")
    N_f = 7 # lol
    v_zero = 4 # lol [2]
    filter_values[v_zero] = 0
    updated_obpf_filter = butterfly_right(list(filter_values))
    print(f"Результат БПФ после зануления: {list(updated_obpf_filter)}")

    filter_obpf_ordered = []

    for order_index in filter_obpf_order:
        filter_obpf_ordered.append(updated_obpf_filter[order_index])

    print(f"Результат ОБПФ (упорядоченный): {list(filter_obpf_ordered)}")


    make_figure()
    plt.plot(x_axis_range, [value.real for value in filter_obpf_ordered], '-o')
    plt.title(f"Обновленный фильтр с зануленным отсчетом v = {v_zero}")
    plt.grid('on')


def time_cycle_shift(filter_values) -> list:
    """Задание 4. Сдвиг оси времени. Смещение по циклу."""
    print("+=====================================+")
    print("Задание 4. Сдвиг оси времени. Смещение по циклу.")

    v_zero = 4
    filter_values.copy()[v_zero] = 0

    shifted_obpf_filter = []
    shift_orded = [3, 2, 1, 0, 7, 6, 5, 4]
    for order_index in shift_orded:
        shifted_obpf_filter.append(filter_values[order_index])

    print(f"Сдвинутый массив: {list(shifted_obpf_filter)}")

    make_figure()
    plt.plot(x_axis_range, [value.real for value in shifted_obpf_filter])
    plt.title("Фильтр после цикличного сдвига")
    plt.grid('On')

    # TODO: добавить фазовый график
    k = sympy.symbols('k')
    dF = -k * 3 * pi / 4
    phase_values = []
    for i in range(4):
        phase_values.append(dF.subs(k, i))
    phase_values.append(0)

    make_figure()
    plt.plot(np.arange(0, 5), phase_values)
    reversed_spectre = [-phase_value for phase_value in phase_values]
    reversed_spectre.reverse()
    plt.plot(np.arange(4, 9), reversed_spectre)

    plt.title("ФЧХ (задание 4)")
    plt.grid("on")

    # TODO: перенести в функцию
    shifted_obpf_butterfly_values = butterfly_right(shifted_obpf_filter)
    shifted_obpf_butterfly_values_ordered = []
    for order_index in filter_obpf_order:
        shifted_obpf_butterfly_values_ordered.append(shifted_obpf_butterfly_values[order_index])

    re_sh_obpf = [round(value.real, 3) for value in shifted_obpf_butterfly_values_ordered]
    im_sh_obpf = [round(value.imag, 3) for value in shifted_obpf_butterfly_values_ordered]
    amp_shifted_obpf_butterfly_values = [round(np.sqrt(re_sh_obpf[i]**2 + im_sh_obpf[i]**2), 3) for i in range(8)]
    print(f"Re values: {list(re_sh_obpf)}")
    print(f"Im values: {list(im_sh_obpf)}")
    print(f"Amp values: {list(amp_shifted_obpf_butterfly_values)}")

    make_figure()
    plt.plot(x_axis_range, amp_shifted_obpf_butterfly_values, '-o')
    plt.title("A(kf) (Task 4)")
    plt.grid('on')

    return shifted_obpf_filter


def hemming_window_converion(cycled_filter_values) -> None:
    """Преобразование через окно Хемминга"""
    print("+=====================================+")
    print("Задание 5. Домножение h(v) на окно Хемминга g(v).")

    print(f"g(V) = 0.54 - 0.46*cos(2pi * V / Nф - 1), V = 0, 1 ... Nф - 1 (Nф = 7)")

    N_f = 7
    v = sympy.symbols('v')
    g = 0.54 - 0.46*sympy.cos(2*pi * v / (N_f - 1))
    g_func_values = []
    for i in range(8):
        g_func_values.append(round(g.subs(v, i), 3))
    print(f"Значения функции g: {g_func_values}")
    print(f"Значения сдвинутого фильтра: {cycled_filter_values}")

    h_w = []
    for i in range(8):
        h_w.append(round(g_func_values[i] * cycled_filter_values[i], 3))

    print(f"Результат почленного умножения: {h_w}")

    mul_result_butterfly = butterfly_right(h_w)

    mul_result_butterfly_ordered = order_filter(mul_result_butterfly)
    re_sh_obpf = [round(value.real, 3) for value in mul_result_butterfly_ordered]
    im_sh_obpf = [round(value.imag, 3) for value in mul_result_butterfly_ordered]
    amp_shifted_obpf_butterfly_values = [round(np.sqrt(re_sh_obpf[i] ** 2 + im_sh_obpf[i] ** 2), 3) for i in range(8)]

    print(f"Re values: {list(re_sh_obpf)}")
    print(f"Im values: {list(im_sh_obpf)}")
    print(f"Amp values: {list(amp_shifted_obpf_butterfly_values)}")

    make_figure()
    plt.plot(x_axis_range, amp_shifted_obpf_butterfly_values, '-o')
    plt.title("A(kf) (Task 5)")
    plt.grid('on')


def check_all() -> None:
    """Задание 6. Проверка Ачх и Фчх."""
    print(f"Если |Im| <= |Re|, alpha = arct(Im / Re)")
    print(f"Если |Im| >  |Re|, alpha = pi/2 - arctg(Re / Im)")

    # TODO: оптимизировать (возможно)
    k = sympy.symbols('k')
    dF = -k * 3 * pi / 4
    # ...
    make_figure()
    plt.ylim([-2.5*pi, 2.5*pi])
    plt.yticks(np.arange(-4 * np.pi, 5 * np.pi, np.pi), [str(i) + "π" for i in range(-4, 5)])
    plt.plot([0, 1, 2, 3, 4], [dF.subs(k, i) for i in range(5)])
    amp_up = abs(dF.subs(k, 4)) * 2
    print(amp_up)
    plt.vlines(4, dF.subs(k, 4),  dF.subs(k, 4) + amp_up)
    plt.plot([4, 5, 6 ,7, 8], [dF.subs(k, i) + amp_up for i in range(4, 9)])
    plt.title("ФЧХ")
    plt.grid('on')


if __name__ == "__main__":
    amplitude_phase_characteristic_approximate(filter_selection) # Task 1
    obpf_filter_result_values = filter_obpf_calculate(filter_selection) # Task 2
    calculate_n_f(obpf_filter_result_values) # Task 3
    cycled_filter = time_cycle_shift(obpf_filter_result_values) # Task 4
    hemming_window_converion(cycled_filter ) # Task 5
    check_all()

    plt.show()

