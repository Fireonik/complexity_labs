from random import randint
from time import perf_counter_ns
import math


def readc(char):  # interface to work with binary text
    return chr(char) if isinstance(char, int) else char


def naive(tested_string, seeked_pattern):
    if len(tested_string) < len(seeked_pattern):
        return False

    for i in range(len(tested_string) - len(seeked_pattern) + 1):
        if readc(tested_string[i:i+len(seeked_pattern)]) == seeked_pattern:
            return True

    return False


def horspool(tested_string, seeked_pattern):
    pattern_size,  text_size = len(seeked_pattern), len(tested_string)
    head = pattern_size - 1
    bad_match_table = {readc(seeked_pattern[i]): pattern_size - (i + 1) for i in range(pattern_size - 1)}  # символ : смещение
    while head < text_size:
        index_ = -1   # индекс текущего сравниваемого элемента из искомой строки, соответствуюий текущему положению головки
        counter = 0  # записываем смещение головки назад в рамках итерации
        while readc(tested_string[head]) == readc(seeked_pattern[index_]):
            counter += 1
            head -= 1
            index_ -= 1
            if counter == pattern_size:
                return True
        head += counter + bad_match_table.get(readc(tested_string[head]), pattern_size)  # двигаем головку соответственно таблице
    return False


def boyer_moore(tested_string, seeked_pattern):
    def bad_character_preprocessing():
        return {readc(seeked_pattern[ind]): ind for ind in range(len(seeked_pattern))}

    def good_suffix_preprocessing():
        s = [0] * (len(seeked_pattern) + 1)
        f = [0] * (len(seeked_pattern) + 1)

        def case_1():
            ind = len(seeked_pattern)
            k = ind + 1
            f[ind] = k
            while ind > 0:
                while k <= len(seeked_pattern) and readc(seeked_pattern[ind - 1]) != readc(seeked_pattern[k - 1]):
                    if s[k] == 0:
                        s[k] = k - ind
                    k = f[k]
                ind -= 1
                k -= 1
                f[ind] = k

        def case_2():
            k = f[0]
            for ind in range(len(seeked_pattern) + 1):
                if s[ind] == 0:
                    s[ind] = k
                if ind == k:
                    k = f[k]
        case_1()
        case_2()
        return s

    bad_char_table = bad_character_preprocessing()
    good_suffix_table = good_suffix_preprocessing()
    i, text_length, pattern_length = 0, len(tested_string), len(seeked_pattern)
    while i <= text_length - pattern_length:
        j = pattern_length - 1
        while j >= 0 and readc(seeked_pattern[j]) == readc(tested_string[i+j]):
            j -= 1
        if j < 0:
            i += good_suffix_table[0]
            return True
        else:
            suffix = good_suffix_table[j + 1]
            bad_char = j - bad_char_table.get(readc(tested_string[i+j]), -1)

            i += suffix if suffix >= bad_char else bad_char

    return False


def knuth_morris_pratt(tested_string, seeked_pattern):
    pattern_length, shift = len(seeked_pattern), 1  # preprocessing
    shift_table = [1] * (pattern_length + 1)
    for pos in range(pattern_length):
        while shift <= pos and readc(seeked_pattern[pos]) != readc(seeked_pattern[pos - shift]):
            shift += shift_table[pos - shift]
        shift_table[pos + 1] = shift

    start_pos, chars_matched = 0, 0  # search
    for ind in range(len(tested_string)):
        while chars_matched == pattern_length or chars_matched >= 0 and readc(seeked_pattern[chars_matched]) != readc(tested_string[ind]):
            start_pos += shift_table[chars_matched]
            chars_matched -= shift_table[chars_matched]
        chars_matched += 1
        if chars_matched == pattern_length:
            return True
    return False


def rabin_karp(tested_string, seeked_pattern):
    text_length, pattern_length = len(tested_string), len(seeked_pattern)
    q, p, t, h = 12, 0, 0, 1
    for _ in range(pattern_length-1):
        h = (h * 256) % q
    for i in range(pattern_length):
        p = (256 * p + ord(readc(seeked_pattern[i]))) % q
        t = (256 * t + ord(readc(tested_string[i]))) % q

    for i in range(text_length - pattern_length):
        if p == t:
            counter = 0
            for j in range(pattern_length):
                if readc(tested_string[i + j]) == readc(seeked_pattern[j]):
                    counter += 1
            if counter == pattern_length:
                return True
        if i < text_length - pattern_length:
            t = (256 * (t - ord(readc(tested_string[i])) * h) + ord(readc(tested_string[i + pattern_length]))) % q
            if t < 0:
                t = (t + q)
    return False


def generate_binary_text(length):
    return [randint(32, 126) for _ in range(length)]


def generate_text(length):
    return [chr(randint(32, 126)) for _ in range(length)]


def check_efficiency(algorithm_, mode_, results_):
    if mode_ == 1:
        results_.append(0)
        for _ in range(10):
            begin = perf_counter_ns()
            text_ = generate_binary_text(1000)
            index_ = randint(0, 991)
            word = text_[index_:index_ + 10]
            algorithm_(text_, word)
            results_[-1] += perf_counter_ns() - begin
        results_[-1] /= 10

    if mode_ == 2:
        results_.append(0)
        for _ in range(10):
            begin = perf_counter_ns()
            text_ = generate_text(1000)
            index_ = randint(0, 991)
            word = text_[index_:index_+10]
            algorithm_(text_, word)
            results_[-1] += perf_counter_ns() - begin
        results_[-1] /= 10


algorithms = [naive, horspool, boyer_moore, knuth_morris_pratt, rabin_karp]
modes = ['Binary text(1000 symbols, 10-letter word from it):', 'Regular text(1000 symbols, 10-letter word from it):']

for mode in modes:
    results = []
    for algorithm in algorithms:
        check_efficiency(algorithm, 1, results)
    for index in range(len(results)):
        results[index] = math.trunc((results[index] / 1_000_000_000) * 10000) / 10000
    print(mode)
    print('Naive             ', str(results[0]), ' seconds')
    print('Horspool          ', str(results[1]), ' seconds')
    print('Boyer-Moore       ', str(results[2]), ' seconds')
    print('Knuth-Morris_Pratt', str(results[3]), ' seconds')
    print('Rabin-Karp        ', str(results[4]), ' seconds')
