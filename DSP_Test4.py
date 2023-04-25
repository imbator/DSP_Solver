import numpy as np
import sympy
import matplotlib.pyplot as plt
import time

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

class ShiftRegister:
    """ Описание класса сдвигового регистра."""
    def  __init__(self, size):
        self.size = size # Установка размера регистра
        self.reg = [0] * size # Хранилище регистра
        self.output = self.reg[-1] # На выход всегда поступает последний элемент

    def make_shift(self, add_value):
        """Имитация сдвига регистра, ex: 0 1 0 (clk)--> 0 0 1"""
        # print(f"add value: {add_value}")
        self.reg[1:] = self.reg[0:len(self.reg) - 1] # Сдвиг
        self.reg[0] = add_value # Добавление в начало

class Switch:
    """ Описание класса свича."""
    def __init__(self, update_frequency):
        self.update_frequency = update_frequency # Частота обновления
        self.input_1 = self.input_2 = self.output_1 = self.output_2 = 0
        self.inverted_output = False
        self.update_frequency = update_frequency
        self.update_counter = 0

    def set_input_values(self, value_1, value_2):
        """Установка входных значений и получение выходных"""
        if self.update_counter == self.update_frequency:
            self.inverted_output = not self.inverted_output
            self.update_counter = 0


        self.input_1 = value_1
        self.input_2 = value_2
        if not self.inverted_output:
            self.output_1 = self.input_1
            self.output_2 = self.input_2
        else:
            self.output_1 = self.input_2
            self.output_2 = self.input_1

        self.update_counter += 1

class BPFThreadAutomate:
    """ Описывает автомат, работаюший по поточной реализации."""

    E = np.exp(-1 * i * (np.pi / 4))
    BUTTERFLY_1_M_VALUES = [E**0, E**1, E**2, E**3]
    BUTTERFLY_2_M_VALUES = [E**0, E**2, E**0, E**2]
    BUTTERFLY_3_M_VALUES = [E**0, E**0, E**0, E**0]
    MAX_CODE_LENGHT = 8
    MAX_BUTTERFLY_MULTIPLUER = 4

    def __init__(self, signal_data):
        self.signal_data = signal_data # Входные данные
        self.reg_0 = ShiftRegister(4)  # Регистр на входе
        self.reg_1 = ShiftRegister(2)  # Регистр снизу после первой бабочки
        self.reg_2 = ShiftRegister(2)  # Регистр сверху после свича и первой бабочки
        self.reg_3 = ShiftRegister(1)  # Регистр снизу после второй бабочки
        self.reg_4 = ShiftRegister(1)  # Регистр сверху после свича и второй бабочки
        self.SW1 = Switch(2) # Первый свитч
        self.SW2 = Switch(1) # Второй свитч
        self.current_butterfly_multiplier_index = 0 # Множитель бабочки
        self.n = 0 # Регулятор ключа

        # Интерфейс ввода-вывода
        self.bpf_input_1 = 0
        self.bpf_input_2 = 0
        self.bpf_output_1 = 0 # Первый выход из автомата
        self.bpf_output_2 = 0 # Второй выход из автомата

    def __str__(self):
        return ", ".join(self.__dict__)

    def check_n(self):
        if self.n == self.MAX_CODE_LENGHT:
            self.n = 0

    def check_current_butterfly_index(self):
        if self.current_butterfly_multiplier_index == self.MAX_BUTTERFLY_MULTIPLUER:
            self.current_butterfly_multiplier_index = 0


    def update(self):
        """ Обновление состояния автомата. Здесь же происходит нативная связка всех
            элементов автомата друг с другом."""

        # Множители для бабочки
        self.check_current_butterfly_index()
        current_butterfly_1_mul = self.BUTTERFLY_1_M_VALUES[self.current_butterfly_multiplier_index]
        current_butterfly_2_mul = self.BUTTERFLY_2_M_VALUES[self.current_butterfly_multiplier_index]
        current_butterfly_3_mul = self.BUTTERFLY_3_M_VALUES[self.current_butterfly_multiplier_index]

        self.current_butterfly_multiplier_index += 1

        # Ввод-вывод:
        if 0 <= self.n <= 3:
            self.bpf_input_1 = self.signal_data[self.n]
            self.bpf_input_2 = 0
        elif 3 < self.n <= 7:
            self.bpf_input_1 = 0
            self.bpf_input_2 = self.signal_data[self.n]
        else:
            self.bpf_input_1 = 0
            self.bpf_input_2 = 0

        # Обновление состояния первого регистра
        last_reg_0_value = self.reg_0.reg[-1]
        last_reg_1_value = self.reg_1.reg[-1]
        last_reg_2_value = self.reg_2.reg[-1]
        last_reg_3_value = self.reg_3.reg[-1]
        last_reg_4_value = self.reg_4.reg[-1]

        # Обновлeние состояния нулевого регистра:
        self.reg_0.make_shift(self.bpf_input_1)

        # Обновление состояния 1 регистра
        self.reg_1.make_shift((last_reg_0_value - self.bpf_input_2) * current_butterfly_1_mul)

        # Обновление состояния первого свича:
        self.SW1.set_input_values(self.bpf_input_2 + last_reg_0_value, last_reg_1_value)

        #Увеличиваем счетчик
        self.n += 1

        # Обновление состояния второго регистра:
        self.reg_2.make_shift(self.SW1.output_1)

        # Обновление состояния третьего регистра:
        self.reg_3.make_shift((last_reg_2_value - self.SW1.output_2) * current_butterfly_2_mul)

        # Обновление состояния второго свича:
        self.SW2.set_input_values(self.SW1.output_2 + last_reg_2_value, last_reg_3_value)

        # Обновление пятого регистра:
        self.reg_4.make_shift(self.SW2.output_1)

        # Значения на выходе автомата:
        self.bpf_output_1 = last_reg_4_value + self.SW2.output_2
        self.bpf_output_2 = (last_reg_4_value - self.SW2.output_2) * current_butterfly_3_mul


def threads_bpf_realisation(signal_discretes) -> list:
    """Поточный метод расчета БПФ."""
    result = []
    print(f"Входные данные поточной реализации: {signal_discretes}")
    automate = BPFThreadAutomate(signal_discretes) # Создаем автомат для работы
    clk_cycles = 0
    while clk_cycles != 12:
        automate.update()
        print(f"Automate updated. Current cycle: {clk_cycles}")

        print(f"input 1: {automate.bpf_input_1}")
        print(f"input 2: {automate.bpf_input_2}")
        print(f"Reg 0 value: {automate.reg_0.reg}")
        print(f"Reg 1 value: {automate.reg_1.reg}")
        print(f"SW 1: input 1: {automate.SW1.input_1}, input 2: {automate.SW1.input_2},"
              f" output 1: {automate.SW1.output_1}, output 2: {automate.SW1.output_2}, "
              f"is inverted: {automate.SW1.inverted_output}")
        print(f"Reg 2 value: {automate.reg_2.reg}")
        print(f"Reg 3 value: {automate.reg_3.reg}")
        print(f"SW 2: input 1: {automate.SW2.input_1}, input 2: {automate.SW2.input_2},"
              f" output 1: {automate.SW2.output_1}, output 2: {automate.SW2.output_2}, "
              f"is inverted: {automate.SW2.inverted_output}")
        print(f"Reg 4 value: {automate.reg_4.reg}")
        print("|================DATA OUTPUT=================|")
        print(f"Data getted from J: {automate.bpf_output_1}")
        print(f"Data geteed from K: {automate.bpf_output_2}")
        print(" ")

        clk_cycles += 1
        time.sleep(0.1)

    return result

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

    threads_bpf_realisation(data)


    # plt.show()

