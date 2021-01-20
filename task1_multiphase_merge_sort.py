import random
import math  # для округления .ceil()
import os  # для работы с файлами


def merge_sort(array):  # сортировка слиянием для последовательностей, количество элементов которых <= допустимому
    if len(array) > 1:

        middle = len(array) // 2

        left = array[:middle]
        right = array[middle:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1


def create_sequence(length, file_name, min_value=-99999, max_value=99999):
    with open(file_name + '.bin', 'wb') as file:
        random.seed()
        for i in range(length):  # генерируем случайные целые числа из указанного диапазона и записываем в файл
            file.write(((str(random.randint(min_value, max_value))) + '\n').encode())


def cut_sequence_into_sorted_manageable_parts(file_name, memory_capacity, pieces_needed):
    with open(file_name + '.bin', 'rb') as sequence:
        for i in range(1, pieces_needed + 1):  # пока не исчерпаем последовательность
            storage_for_sorting = []
            try:
                for index in range(memory_capacity):  # берём столько элементов последовательности сколько можем
                    storage_for_sorting.append(int(sequence.readline().decode()))
            except ValueError:
                pass  # если последовательность закончилась раньше, прекращаем читать
            merge_sort(storage_for_sorting)  # сортируем получившуюся подпоследовательность
            with open(str(i) + '.bin', 'wb') as curr_file:  # создаём файл для неё
                for number in storage_for_sorting:  # и записываем в него
                    curr_file.write((str(number) + '\n').encode())


def merge_two_files(file_one, file_two):
    with open(file_one, 'rb') as first, open(file_two, 'rb') as second, open('result.bin', 'wb') as result:
        buffer = ['empty', 'empty']
        while True:  # производим слияние до тех пор пока один из файлов не будет исчерпан
            try:
                if buffer[0] == 'empty':  # пополняем буфер
                    buffer[0] = int(first.readline().decode())
                if buffer[1] == 'empty':
                    buffer[1] = int(second.readline().decode())
            except ValueError:  # этот блок исполняется, когда один из файлов исчерпан
                non_empty_buffer_element = 0 if buffer[0] != 'empty' else 1
                non_empty_file = first if non_empty_buffer_element == 0 else second
                result.write((str(buffer[non_empty_buffer_element]) + '\n').encode())  # не забываем про элемент в буфере
                for number in non_empty_file:
                    result.write(number)  # записываем остаток неисчерпанного файла в конец результата
                return
            else:
                the_smaller_one = 0 if buffer[0] <= buffer[1] else 1  # выбираем меньший из двух элементов
                result.write((str(buffer[the_smaller_one]) + '\n').encode())  # записываем в результат
                buffer[the_smaller_one] = 'empty'  # опустошаем соответствующую ячейку буфера


def phase(parts_to_process):  # одна фаза сортировки
    iterator = 1
    while iterator < parts_to_process:
        file_1 = str(iterator) + '.bin'  # берём по две отсортированных последовательности
        file_2 = str(iterator + 1) + '.bin'
        merge_two_files(file_1, file_2)  # производим их слияние в одну
        os.remove(file_1)  # удаляем файлы которые больше не нужны
        os.remove(file_2)
        os.rename('result.bin', str(math.ceil(iterator/2)) + '.bin')  # учитываем это и нумеруем их заново
        iterator += 2  # за раз мы обрабатываем по два файла, так что и шаг итератора должен быть равен двум
    if parts_to_process % 2 == 1:  # если файлов нечётное количество, последний найдёт себе пару на следующей итерации
        os.rename(str(parts_to_process) + '.bin', str(math.ceil(parts_to_process/2)) + '.bin')
    return math.ceil(parts_to_process/2)  # частей последовательности которые надо слить вместе стало меньше


def count_numbers_in_sequence(file_name):
    with open(file_name + '.bin', 'rb') as sequence:
        counter = 0
        for _ in sequence:
            counter += 1
    return counter


def multiphase_merge_sort(file_name, max_list_size):
    sequence_length = count_numbers_in_sequence(file_name)
    parts_to_process = math.ceil(sequence_length / max_list_size)  # <-- столько необходимо обработать вмещающихся в память частей
    cut_sequence_into_sorted_manageable_parts(file_name, max_list_size, parts_to_process)
    while parts_to_process > 1:
        parts_to_process = phase(parts_to_process)  # собственно, многофазная сортировка слиянием
    try:
        os.remove(file_name + '_sorted.bin')  # обработка повторных запусков
    except FileNotFoundError:
        pass
    os.rename('1.bin', file_name + '_sorted.bin')


def check_if_algorithm_works(file_name):
    with open(file_name + '_sorted.bin', 'rb') as result:
        check = int(result.readline().decode())
        for number in result:
            temp = int(number.decode())
            if temp < check:
                return 'FAILURE'
            check = temp
        return 'SUCCESS'


create_sequence(21764, 'sequence', -999999, 999999)  # длина, имя, минимальное и максимальное значения случайных чисел.
multiphase_merge_sort('sequence', 1000)  # имя последовательности, максимально допустимое количество элементов списка, хранимых одновременно в памяти
print(check_if_algorithm_works('sequence'))  # выводит SUCCESS в случае успеха, FAILURE в случае неудачи
