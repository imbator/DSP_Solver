def do_filtration(data: str, ref_data: str, task_number:int) -> list:
    """Функция для 3-6 задачи, построение фильтра"""

    is_sum = 1 if len(data.split(',')) == 8 else 0 # Длина входных данных на 1 больше если на вход идет сумма

    print(f"Task {task_number}.")
    var = list(map(int, data.split(',')))
    var.reverse()

    reference = list(map(int, ref_data.split(','))) # Опорный вектор. На него умножаем
    reference.reverse()

    print(f"Ref: {reference}")

    sequence = [0, 0, 0, 0, 0, 0, 0, *var, 0, 0, 0, 0, 0, 0, 0]

    print(f"Sequence: {sequence}")

    sum_array = [] # Значения арифметической суммы для графика

    for i in range(15 + is_sum):
        current_chunk = sequence[14 + is_sum : 21 + is_sum]
        current_star_chunk = [current_chunk[i] * reference[i] for i in range(7)] # То, что суммируется

        # Вывод инфы на экран (возможно, потом оптимизировать

        for j in range(14 + is_sum):
            print(f" {sequence[j]}", end=' ') if sequence[j] >=0 else print(f"{sequence[j] }", end=' ')
        print('|', end=' ')
        for j in range(14 + is_sum, 21 + is_sum):
            print(f" {sequence[j]}", end=' ') if sequence[j] >= 0 else print(f"{sequence[j]}", end=' ')
        print('|', end=' ')
        for j in current_star_chunk:
            print(f" {j}", end=' ') if j >= 0 else print(f"{j}", end=' ')
        print('|', end='')

        print(f" {sum(current_star_chunk)}") if sum(current_star_chunk) >= 0 else print(f"{sum(current_star_chunk)}")

        sequence = [0, *sequence[0:20 + is_sum]]
        sum_array.append(sum(current_star_chunk))


    print(f"Points: {sum_array}", end='\n')

    return sum_array

m1_m2 = [[0b011, 0b101], [0b101, 0b011]]


def from_t3_to_m(t1_t2_t3):
    if int(t1_t2_t3):
        return "-1"
    else:
        return "1"


def get_task(number):
    variant = number[1]
    phase = number[2:5]

    if phase == "000":
        phase = "001"

    print(f"Ваш вариант: M1 и M2 = {m1_m2[int(variant)]}, фаза = {phase}")

    return m1_m2[int(variant)], phase


def get_m1_m2(t1_t2_t3: str, m1_m2: int):
    m = ""
    if m1_m2 == 5:
        t1_t2_t3 += str(int(t1_t2_t3[0]) ^ int(t1_t2_t3[2])) + from_t3_to_m(t1_t2_t3[2])
        m += t1_t2_t3[4:] + ", "
        print(0, t1_t2_t3)

        for i in range(1, 7):
            t1_t2_t3 = str(t1_t2_t3[3]) + str(t1_t2_t3[0]) + str(t1_t2_t3[1])
            t1_t2_t3 += str(int(t1_t2_t3[0]) ^ int(t1_t2_t3[2])) + from_t3_to_m(t1_t2_t3[2])
            m += t1_t2_t3[4:] + ", "
            print(i, t1_t2_t3)
    elif m1_m2 == 3:
        t1_t2_t3 += str(int(t1_t2_t3[1]) ^ int(t1_t2_t3[2])) + from_t3_to_m(t1_t2_t3[2])
        m += t1_t2_t3[4:] + ", "
        print(0, t1_t2_t3)

        for i in range(1, 7):
            t1_t2_t3 = str(t1_t2_t3[3]) + str(t1_t2_t3[0]) + str(t1_t2_t3[1])
            t1_t2_t3 += str(int(t1_t2_t3[1]) ^ int(t1_t2_t3[2])) + from_t3_to_m(t1_t2_t3[2])
            if i <= 8:
                m += t1_t2_t3[4:] + ", "
            print(i, t1_t2_t3)
    return m[:-2]


def sum_m1_m2(m1, m2):
    sum = ""

    m1_list = list(map(int, m1.split(",")))
    m2_list = list(map(int, m2.split(",")))

    m1_list.insert(8, 0)
    m2_list.insert(0, 0)

    for i in range(0, 8):
        sum += str(m1_list[i] + m2_list[i] * (-1)) + ", "

    return sum[:-2]

if __name__ == "__main__":
    task = get_task("10011")

    print("M1")
    m1 = get_m1_m2(task[1], task[0][0])

    print("M2")
    m2 = get_m1_m2(task[1], task[0][1])

    print(f"M1 = {m1} | M2 = {m2}")

    print("M1 + M2 =", sum_m1_m2(m1, m2))


    # Задание 3
    do_filtration(m1, m1, 3)

    # Задание 4
    do_filtration(m1, m2, 4)

    # Задание 5
    do_filtration(sum_m1_m2(m1, m2), m1, 5)

    # Задание 6
    do_filtration(sum_m1_m2(m1, m2), m2, 6)


