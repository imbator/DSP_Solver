# КР 2 ЦОС

change = {'1': '0', '0': '1'}

Var = str(input("Введите вариант: "))

seq1 = "1" + Var
seq0 = "0" + Var

def WalsheCode(seq: str) -> str:
    """ Возвращает код Уолша"""
    data = list(seq)
    result = data[0]
    print(data)
    for i in data:
        result += result
        if i == '1':
            new_seq = []
            for j in range(len(result)):
                new_seq.append(change[result[j]])
            result = ''.join(new_seq)
            print(result)
    return result

print(f"Walshe code: {WalsheCode(seq0)}")
