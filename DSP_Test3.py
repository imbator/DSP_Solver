#
# ████████╗███████╗░██████╗████████╗██████╗░
# ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝╚════██╗
# ░░░██║░░░█████╗░░╚█████╗░░░░██║░░░░█████╔╝
# ░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░░╚═══██╗
# ░░░██║░░░███████╗██████╔╝░░░██║░░░██████╔╝
# ░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═════╝░
import matplotlib.pyplot
# Test 3 solution generator for MIET DSP Course
# Ver 0.1 (beta)
# tg : @imbator

import matplotlib.pyplot as plt
from math import cos, sin
import numpy as np
import sympy
from scipy import interpolate
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys
import textwrap

x, y = 20, 19900 # Параметры для записи в pdf
plt.max_open_warning = True
pdfmetrics.registerFont(TTFont('ArialUnicode', 'C:\Windows\Fonts\Arial.ttf'))
pagesize = (letter[0], 20000)
c = canvas.Canvas(f"report{3}.pdf", pagesize=pagesize)
page_width, page_height = letter
c.setFont('ArialUnicode', 12)
out = StringIO()
sys.stdout = out

f_1 = 300 # Частота 1
f_2 = 600 # Частота 2
f_3 = 2400 # Частота дискретизации

# Расчет варианта:
# var = (input("Введите вариант в двоичной системе: ")) # Для отладки берем 18
# fi_1 = sympy.pi
# fi_2 = sympy.pi

print(f"Вариант: {3}")

fi_1 = 3 * sympy.pi / 4
fi_2 = 0 * sympy.pi / 2

LAST_FIGURE_NUMBER = 0

def new_page(c):
    """ Создание новой страницы"""
    c.showPage()
    c.setFont('ArialUnicode', 12)
    c.setFillColorRGB(0, 0, 0)

def make_figure() -> plt.figure:
    """Возвращает объект для нового графика."""
    global LAST_FIGURE_NUMBER
    LAST_FIGURE_NUMBER += 1
    return plt.figure(LAST_FIGURE_NUMBER)

def write_to_pdf():
    """Помещает текст в pdf."""
    global x, y, out, c

    text = out.getvalue()
    for line in text.split('\n'):
        c.drawString(x, y , line.strip())
        y -= 20
    out.truncate(0)
    out.seek(0)

def save_plot(fig, filename, width=300):
    global x, y # Используются для определения текущей позиции текста
    fig.savefig(filename, format='png', dpi=300)
    c.drawImage(filename, x, y - 250, width, 250)
    y -= 250

def cos_function(_f_1 , _fi_1, _f_2, _fi_2) -> None:
    """ Возвращает две функции сигнала на основе заданных параметров."""

    # Формирование сигналов s1, s2
    s1 = sympy.Expr(f'cos({2*sympy.pi*_f_1}*t + %s)' % _fi_1)
    s2 = sympy.Expr(f'cos({2*sympy.pi*_f_2}*t + %s)' % _fi_2)
    print(f"s1 = {str(s1).strip('Expr')}")
    print(f"s2 = {str(s2).strip('Expr')}")
    print(f"s1 + s2 = {str(s1).strip('Expr')} + {str(s2).strip('Expr')}")

def plot_graphs_after_DPF(data):
    """Функция изображает результаты работы 4 задания в виде графиков."""

    global LAST_FIGURE_NUMBER

    # Re
    fig = make_figure()
    for i in range(8):
        plt.vlines(i, 0,sympy.re(data[i]), colors='r')
    plt.title("Re new")
    write_to_pdf()
    save_plot(fig, "plot5.png")

    # Im
    fig = make_figure()
    for i in range(8):
        plt.vlines(i, 0, sympy.im(data[i]), colors='r')
    plt.title("Im new")
    write_to_pdf()
    save_plot(fig, "plot6.png")

    # A = sqrt(Im^2Z + Re^2Z)
    fig = make_figure()
    for i in range(8):
        plt.vlines(i, 0, sympy.sqrt(sympy.im(data[i])**2 + sympy.re(data[i])**2), colors='r')
    plt.title("A new")
    write_to_pdf()
    save_plot(fig, "plot7.png")

    # Fi
    fig = make_figure()
    points = np.angle(list(map(complex, data)))
    for i in range(4):
        plt.vlines(i, 0, abs(points[i]), colors='r')
    for i in range(4, 8):
        plt.vlines(i, 0, -abs(points[i]), colors='r')

    plt.title("Im new")
    write_to_pdf()
    save_plot(fig, "plottg.png")

def plot_graphs_after_ODPF(data):
    """Завершающее построение"""
    print("Полученная кривая: ")
    print(data)
    fig = make_figure()


    plt.plot(np.arange(0, 8), data, 'o', color='r')
    f = interpolate.interp1d(np.arange(0, 8), data, kind='cubic')
    xnew = np.linspace(0, 7, 1000)
    plt.plot(xnew, f(xnew), '-', label='интерполированная кривая')
    plt.title("ODFP Result")
    write_to_pdf()
    save_plot(fig, f"Final.png", 400)


def task_1() -> int:
    """ Задание 1. Обосновать выбор N."""
    N = f_3 / f_1

    print(f"Определим количество точек N. Нужно, чтобы частота целое количество раз умещалось в \n"
          f"периоде. Так как  f_1 = 300, N = {f_3} / {f_1} = {f_3 / f_1}")
    return int(N)

def task_2(N: int) -> None:
    """Предсказание спектра для (S1 + S2), A, phi, Re, Im"""

    global f_1, f_2, f_3

    t = sympy.symbols('t')

    cos_function(f_1, fi_1, f_2, fi_2)

    # На каких отсчетах получатся максимумы?
    x1 = int(f_1 * N / f_3)
    x2 = int(f_2 * N / f_3)
    print(f"Отсчеты максимумов:")
    print(f"x1 = {f_1} * {N} / {f_3} = {x1}")
    print(f"x1 = {f_2} * {N} / {f_3} = {x2}")

    # Расчет амплитуд максимумов:
    # Важно! Опускается, что идет домножение на T.
    A1 = N / 2
    A2 = N / 2

    print(f"Амплитуды максимумов: A1: {A1}*T, A2: {A2}*T")

    dots = {x1: (A1, fi_1), x2: (A2, fi_2)}

    # Построим амплитудный спектр:

    fig1 = make_figure()
    for i in range(7):
        if i in dots.keys():
            plt.vlines(i, 0, dots[i][0], colors='r')
            plt.vlines(-i + N, 0, dots[i][0], colors='r')
    plt.title("Amplutude spectrum")

    write_to_pdf()
    save_plot(fig1, "plot.png")

    # Построим фазовый спектр

    fig2 = make_figure()
    for i in range(7):
        if i in dots.keys():
            plt.vlines(i, 0, dots[i][1], colors='r')
            plt.vlines(-i + N, 0, -dots[i][1], colors='r')
    plt.title("Phase spectum")

    write_to_pdf()
    save_plot(fig2, "plot1.png")

    # Построим Re часть числа
    print('Re = A*cos(phi)')
    fig3 = make_figure()
    for i in range(7):
        if i in dots.keys():
            plt.vlines(i, 0, cos(dots[i][1]) * dots[i][0], colors='r')
            plt.vlines(-i + N, 0, cos(dots[i][1]) * dots[i][0], colors='r')
    plt.title("Re part of signal")
    write_to_pdf()
    save_plot(fig3, "plot2.png")

    # Построим Im часть числа
    print('Im = A*sin(phi)')
    fig4 = make_figure()
    for i in range(7):
        if i in dots.keys():
            plt.vlines(i, 0, sin(dots[i][1]) * dots[i][0], colors='r')
            plt.vlines(-i + N, 0, -sin(dots[i][1]) * dots[i][0], colors='r')
    plt.title("Im part of signal")
    write_to_pdf()
    save_plot(fig4, "plot3.png")

def task_3(f1, fi1, f2, fi2) -> tuple:
    """Продискретизировать и упростить сумму сигналов s1(f1, fi1) + s2(f2, fi2)."""
    global LAST_FIGURE_NUMBER

    print(f"s1 + s2 = cos({2*f1} * pi * t + {fi1} + cos({2*f2} * pi * t + {fi2})")
    print("t->nT")
    print(f"s1 + s2 = cos({2*f1} * pi * (1 / {f_3}) * n+ {fi1}) + cos({2*f2} * pi * (1 / {f_3}) * n+ {fi2})")
    n = sympy.symbols('n')
    sum_signal = sympy.cos(2 * f1 * sympy.pi * (1 / f_3) * n + fi1) + sympy.cos(2 * f2 * sympy.pi * (1 / f_3) * n+ fi2)
    s1_new = sympy.cos(2 * f1 * sympy.pi * (1 / f_3) * n + fi1)
    s2_new = sympy.cos(2 * f2 * sympy.pi * (1 / f_3) * n+ fi2)
    print(sympy.cos(2 * f1 * sympy.pi * (1 / f_3) * n + fi1))
    print(f"s1 + s2 = {sum_signal}")
    # s1_plus_s2 = sympy.cos(2 * sympy.pi * f * t + fi) + sympy.cos(2 * sympy.pi * f * t + fi)

    results = []
    for i in range(8):
        result = sum_signal.subs(n, i)
        results.append(result)

    fig5 = make_figure()
    plt.plot(np.arange(0, 8), results, 'o', color='r')
    f = interpolate.interp1d(np.arange(0, 8), results, kind='cubic')
    xnew = np.linspace(0, 7, 1000)
    plt.plot(xnew, f(xnew), '-', label='интерполированная кривая')
    plt.title("Discretted s1 + s2")
    print(f"Получены точки: {results}")
    write_to_pdf()
    save_plot(fig5, "plot4.png")

    return results, sum_signal, (s1_new, s2_new)

def task_4(points, sum_signal, s1_s2):
    """Вычислить и графически изобразить ДПФ(s1 + s2). Построить Re, Im, A, fi. Сравнить с п.2 (!)"""

    print(f"ΩT = 2 * pi / N = {2 * sympy.pi / N}")
    print(f"W = e^(i * {2 * sympy.pi / N}) - оператор единичного поворота вектора на угол {2 * sympy.pi / N}.")
    print(f"S(mΩ) = Σ(0-7) {sum_signal} * W ^ -nm")
    print(s1_s2)

    j = sympy.I # Определяем комплексную единицу

    getted_data = []

    for m in range(8):
        text_to_print = [] # Сюда складываем числа для вывода суммы
        fig = make_figure()
        sum_for_signal = 0 # Cюда суммируем
        print(f"m = {m}:")
        print("Расчет: ")
        for n in range(8):
            print(f"n = {n}, W^{m*n%8}")

            E = sympy.exp(-1 * j * (sympy.pi / 4) * n * m)

            term1 = s1_s2[0] * E # Попробуем сложить так
            term2 = s1_s2[1] * E
            S = sum_signal * E

            result = S.subs(sympy.symbols('n'), n) # Тут хранится результирующая точка

            term1_result = term1.subs(sympy.symbols('n'), n)
            term2_result = term2.subs(sympy.symbols('n'), n)

            term_sum = term1_result + term2_result
            # print(f"term_sum = {term_sum}")

            real_part1, imag_part2 = term_sum.as_real_imag()
            # print(f"So, {real_part1}, {imag_part2}")

            # print(f"result: {result}")

            r = np.abs(complex(result))
            theta = np.angle(complex(result))
            plt.polar([0, theta], [0, r],  marker='o')
            plt.text(theta, r, f"n = {n}")

            real_part, imag_part = result.as_real_imag()
            sum_for_signal += (real_part1 + imag_part2*j)

            text_to_print.append(str(sympy.simplify(result)))
            # print(f"sum: {real_part} + {imag_part*j}")

        # Выводим на экран формулу суммы:
        result_string = ' + '.join(text_to_print)

        wrapped_lines = textwrap.wrap(f"S({m}*Ω) = {result_string} = {sympy.simplify(sum_for_signal)}", width=90)
        for line in wrapped_lines:
            print(line)  # вывести каждую подстроку на отдельной строке

        # print(f"S({m}*Ω) = {result_string} = {sum_for_signal}")
        result_string = ""

        getted_data.append(sympy.simplify(sum_for_signal))
        write_to_pdf()
        save_plot(fig, f"polarplot{m}.png", 400)

    plt.close('all')

    print(f"Получены данные: {getted_data}")
    # print(getted_data[1].simplify(), type(getted_data[1]))

    plot_graphs_after_DPF(getted_data)

    return getted_data

def task_5(dfp_data):
    """Вычислить ОДПФ"""

    print(f"S(nT) = 1 / N * S(m * Ω * W ^ -nm")
    j = sympy.I  # Определяем комплексную единицу
    getted_data = []
    for n in range(8):
        text_to_print = []  # Сюда складываем числа для вывода суммы
        fig = make_figure()
        sum_for_signal = 0 # Cюда суммируем
        print(f"n = {n}:")
        print("Расчет:")
        for m in range(8):

            E = sympy.exp(j * (sympy.pi / 4) * n * m)
            S = dfp_data[m] * E

            print(f"m= {m}, W^{m * n}")

            result = S.subs(sympy.symbols('n'), m)  # Тут хранится результирующая точка


            r = np.abs(complex(result))
            theta = np.angle(complex(result))
            plt.polar([0, theta], [0, r],  marker='o')
            plt.text(theta, r, f"n = {m}")
            # print(f'result: {result}')

            real_part, imag_part = result.as_real_imag()
            sum_for_signal += (real_part + imag_part * j)

            # print(f"Принт:: {sum_for_signal}")
            text_to_print.append(str(sympy.simplify(result)))



        wrapped_lines = textwrap.wrap(f"{n}T = ({'+'.join(text_to_print)} ) / 8 = {(1 / 8) * sympy.simplify(sum_for_signal)}", width=90)
        for line in wrapped_lines:
            print(line)  # вывести каждую подстроку на отдельной строке

        # print(f"{n}T = ({'+'.join(text_to_print)}) = {(1 / 8) * sum_for_signal}")
        getted_data.append((1 / 8) * sympy.simplify(sum_for_signal))

        write_to_pdf()
        save_plot(fig, f"polarplot{n+8}.png", 400)

    print(f"Полученные итоговые данные: {list(map(lambda x: round(x, 2), getted_data))}")

    # print(f"Getted data: {getted_data}")
    plot_graphs_after_ODPF(getted_data)


# Задание 1. Обосновать выбор N.

print("Задание 1:")
N = task_1()
print('')

# Задание 2. Предсказать спектр для (S1 + S2), A, phi, Re, Im
print("Задание 2:")
task_2(N)
print('')

print("Задание 3:")
points_from_discrete_conversion, s1_plus_s2, cortege = task_3(f_1, fi_1, f_2, fi_2)
print('')

print("Задание 4:")
data_array_from_dpf = task_4(points_from_discrete_conversion, s1_plus_s2, cortege)
print('')

print("Задание 5:")
task_5(data_array_from_dpf)
print('')

print(LAST_FIGURE_NUMBER)

# plt.show() # Все полученные результаты.

# sys.stdout = sys.__stdout__
# text = out.getvalue()

write_to_pdf()
# put_image_to_pdf()
sys.stdout = sys.__stdout__

c.save()