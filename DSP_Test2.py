import numpy as np
import matplotlib.pyplot as plt

# DSP KR2 Solution generator
# Ver 0.2 beta
# tg: @imbator

changer = {'0': '1', '1': '-1'}

class Summator2:
    """Имитация блока сумматора по модулю 2."""
    def __init__(self, val1, val2=0):
        self.input1 = val1 # Значение с последовательности (по варианту)
        self.input2 = val2
    def get2sum(self):
        return (self.input1 + self.input2) % 2

class Automate:
    """ Класс описывает работу автомата - генератора кода Уолша для 16 абонентов r = 5."""
    def __init__(self, seq):
        print('Seq: ', seq)
        self.register = [0] * 8  # Сдвиговый регистр
        self.S0 = Summator2(0, 0) # Первое суммирование всегда 0
        self.S1 = Summator2(int(seq[0]))
        self.S2 = Summator2(int(seq[1]))
        self.S3 = Summator2(int(seq[2]))
        self.S4 = Summator2(int(seq[3]))
        self.active_summator = self.S1

    def setActive(self, n):
        """Устанавливает активный сумматор."""
        if n == 0:
            self.active_summator = self.S0
        elif n == 1:
            self.active_summator = self.S1
        elif n in (2, 3):
            self.active_summator = self.S2
        elif n in (4, 5, 6, 7):
            self.active_summator = self.S3
        elif n in (i for i in range(8, 16)):
            self.active_summator = self.S4

    def makeShift(self):
        """Реализация сдвига данных."""
        self.register = [self.active_summator.get2sum()] + self.register[:len(self.register) - 1] # Сдвигаем

        # Обновляем входы сумматоров:
        self.S1.input2 = self.register[0]
        self.S2.input2 = self.register[1]
        self.S3.input2 = self.register[3]
        self.S4.input2 = self.register[7]

Var_dec = int(input("Введите свой вариант по номеру в журналу: "))
Var = input("Введите свой вариант в бинарном виде (4 младшие цифры): ")


seq0 = list('0' + Var)
seq1 = list('1' + Var)

def invert(data: str):
    result = []
    for char in data:
        result.append('1') if char == '0' else result.append('0')
    return ''.join(result)

def GetWalshCode(seq: list) -> str:
    """Генерация кода Уолша по входной последовательности."""
    chunk = seq[0]
    for i in range(1, len(seq)):
        print(f"{chunk} -> ", end='')
        if seq[i] == '1':
            chunk += invert(chunk)
        else:
            chunk += chunk
    return chunk

def GetAutomateWalshCode(seq: list) -> str:
    """Генерация кода Уолша при помощи автомата."""
    AutomateCode = []
    WalshAutomate = Automate(seq)

    print('n  | T1 T2 T3 T4 T5 T6 T7 T8 | 2^x | Σ2 | M_x |  sgn')
    for n in range(16):
        WalshAutomate.setActive(n) # Устанавливаем активный сумматор
        print_n = str(n) if n > 9 else f"{n} "
        print_Walshe_byte = "-1" if changer[str(WalshAutomate.active_summator.get2sum())] == "-1" else " 1"
        print(f"{print_n} | {'  '.join(list(map(str, WalshAutomate.register)))}  |  {WalshAutomate.active_summator.input1}  |"
              f" {WalshAutomate.active_summator.input2}{WalshAutomate.active_summator.input1} |"
              f"  {WalshAutomate.active_summator.get2sum()}  |  {print_Walshe_byte}")
        AutomateCode.append(changer[str(WalshAutomate.active_summator.get2sum())])
        WalshAutomate.makeShift()

    return ','.join(AutomateCode)

def CorelatorCalculate() -> None:
    W0 = list(map(int, WalshCode0.split(',')))
    W1 = list(map(int, WalshCode1.split(',')))

    W0.reverse()
    W1.reverse()
    current_sum = 0
    sum_array = []

    for i in range(0, 16):
        current_sum += W0[i] * W0[i]
        sum_array.append(current_sum)

    sum_array.append(0)
    current_sum = 0

    for i in range(0, 16):
        current_sum += W0[i] * W1[i]
        sum_array.append(current_sum)

    x = np.arange(1, 34, 1)
    print(f"Массив данных для графика: {sum_array}")
    plt.plot(x, sum_array)
    # plt.grid()
    # plt.show()

def Butterfly(seq: list):
    """ Расчет методом бабочки фурье."""
    stage_1 = [0]*16
    CalculateButterflySection(seq, stage_1, 0, 8) # Размер берется в 2 раза меньше, так-как крест-накрест
    stage_2 = [0]*16
    for i in range(0, 16, 8):
        CalculateButterflySection(stage_1, stage_2, i, 4)
    stage_3 = [0]*16
    for i in range(0, 16, 4):
        CalculateButterflySection(stage_2, stage_3, i, 2)
    stage_4 = [0]*16
    for i in range(0, 16, 2):
        CalculateButterflySection(stage_3, stage_4, i, 1)

    # Вывод бабочки на экран
    for i in range(16):
        print(f"{seq[i]} - {stage_1[i]} - {stage_2[i]} - {stage_3[i]} - {stage_4[i]}")

    # По итогу должен получиться 1 или более максимумов. Найдем:
    values = set(filter(lambda x: x != 0, stage_4))
    for r in values:
        indices = [i for i, x in enumerate(stage_4) if x == r]
        for index in indices:
            result = ('0' if r > 0 else '1') + f"{index:04b}"[::-1]
            print(f"Получено число: {result}. В десятичной записи: {int(result, 2)}.")

def CalculateButterflySection(base_column: list, new_column: list, section_start: int, size: int):
    """ Расчет секции для бабочки фурье."""
    for i in range(section_start, section_start + size):
        new_column[i], new_column[i + size] = base_column[i] + base_column[i + size], base_column[i] -base_column[i + size]

# Main
print("Задание 1. Сгенерировать с помощью алгоритма: ")
WalshCode0 = GetWalshCode(seq0) # Получение кода Уолша для случая '0'
print(WalshCode0)
WalshCode0 = ','.join([changer[i] for i in WalshCode0])
print(f"Walsh (в '0'): {WalshCode0}")
print('')

print("Задание 2. Сгенерировать с помощью автомата. Проверить: ")
AutomateWalshCode0 = GetAutomateWalshCode(list(Var))
print(f"Walsh automate (в '0'): {AutomateWalshCode0}")

if AutomateWalshCode0 == WalshCode0:
    print("Код Уолша, созданный автоматом, совпадает с кодом уолша по алгоритму.")
else:
    print("Что - то пошло не так. Попробуйте обновить код / входные данные")

print("Задание 3. Сгенерировать код Уошла для '1': ")
WalshCode1 = GetWalshCode(seq1)
print(WalshCode1)
WalshCode1 = ','.join([changer[i] for i in WalshCode1])
print(f"Walsh (в '1'): {WalshCode1}")
print("")

print("Задание 4. Распознать с помощью коррелятора послед. Walsh(В '0'), Walsh(В '1')")
CorelatorCalculate()

print("Задание 5. Система магистральной связи (бабочки Фурье)")
Butterfly(list(map(int, WalshCode0.split(','))))
print(' ')

print("Задание 6. Вычислить с помощью алгоритма Walsh(B + 10)")
WalshCodeVar = GetWalshCode(list(f"{Var_dec:05b}"))
print(WalshCodeVar)
WalshCodeVar = ','.join([changer[i] for i in WalshCodeVar])
print(f"Walsh (ВАР): {WalshCodeVar}")

var_plus_10 = Var_dec + 10
WalshCodeVarPlus10 = GetWalshCode(list(f"{var_plus_10 :05b}"))
print(WalshCodeVarPlus10)
WalshCodeVarPlus10 = ','.join([changer[i] for i in WalshCodeVarPlus10])
print(f"Walsh (ВАР + 10): {WalshCodeVarPlus10}")

# Расчет суммы
WalshCodeVar = list(map(int, WalshCodeVar.split(',')))
WalshCodeVarPlus10 = list(map(int, WalshCodeVarPlus10.split(',')))

seq_sum = [int(WalshCodeVar[i]) + int(WalshCodeVarPlus10[i]) for i in range(len(WalshCodeVar))]
Butterfly(seq_sum)



