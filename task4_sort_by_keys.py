from random import randint


class NumberWithAKey:
    def __init__(self):
        self.key = 0
        self.number = 0


def generate_list(length_):
    list_ = []
    for j in range(length_):
        list_.append(NumberWithAKey())
        list_[j].key = randint(0, 1)
        list_[j].number = randint(-999, 999)
    return list_


# используется алгоритм pigeonhole sort (один из вариантов count sort).
# Время: О(n), пространство: О(n). Технически, pigeonhole имеет сложность O(n + N), где N - количество разных ключей
# (в нашем случае 2: 0 и 1) однако N - константа, => ею можно пренебречь, как и обычной С
# Значения эл-в с одинаковыми ключами перемещаются во временный словарь и назад из него в том же порядке,  в котором они
# хранились в изначальном списке, следовательно их относительный порядок остаётся неизменным => алгоритм стабилен.
# Следовательно, все три критерия удовлетворены.

length = 100
list_to_be_sorted = generate_list(length)

C = {}  # временный словарь
for i in range(2):  # 2 операции
    C[i] = []

for i in range(length):  # n операций
    C[list_to_be_sorted[i].key].append(list_to_be_sorted[i].number)

for i in range(len(C[0])):  # эти два цикла вместе совершают n итераций
    list_to_be_sorted[i].key = 0
    list_to_be_sorted[i].number = C.get(0)[i]
for i in range(len(C[1])):
    list_to_be_sorted[i + len(C[0])].key = 1
    list_to_be_sorted[i + len(C[0])].number = C.get(1)[i]
del C  # временный словарь больше не нужен


for element in list_to_be_sorted:  # демонстрация результата
    print(str(element.key) + ' : ' + str(element.number))
