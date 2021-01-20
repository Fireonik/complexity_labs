from random import randint
from time import perf_counter_ns


def divide11(a, n):
    k = int(n / 2)
    a11 = [[[0] for _ in range(0, k)] for __ in range(0, k)]
    for i in range(0, k):
        for j in range(0, k):
            a11[i][j] = a[i][j]
    return a11


def divide12(a, n):
    k = int(n / 2)
    a12 = [[[0] for _ in range(0, k)] for __ in range(0, k)]
    for i in range(0, k):
        for j in range(0, k):
            a12[i][j] = a[i][j + k]
    return a12


def divide21(a, n):
    k = int(n / 2)
    a21 = [[[0] for _ in range(0, k)] for __ in range(0, k)]
    for i in range(0, k):
        for j in range(0, k):
            a21[i][j] = a[i + k][j]
    return a21


def divide22(a, n):
    k = int(n / 2)
    a22 = [[[0] for _ in range(0, k)] for __ in range(0, k)]
    for i in range(0, k):
        for j in range(0, k):
            a22[i][j] = a[i + k][j + k]
    return a22


def merge(a11, a12, a21, a22, n):
    k = int(2 * n)
    a = [[[0] for _ in range(0, k)] for __ in range(0, k)]
    for i in range(0, n):
        for j in range(0, n):
            a[i][j] = a11[i][j]
            a[i][j + n] = a12[i][j]
            a[i + n][j] = a21[i][j]
            a[i + n][j + n] = a22[i][j]
    return a


def plus(a, b, n):
    c = [[[0] for _ in range(0, n)] for __ in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            c[i][j] = a[i][j] + b[i][j]
    return c


def minus(a, b, n):
    c = [[[0] for _ in range(0, n)] for __ in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            c[i][j] = a[i][j] - b[i][j]
    return c


def strassen(a, b, n):
    k = n
    if k == 16:
        d = [[0 for _ in range(16)] for __ in range(16)]

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    d[i][j] += a[i][k] * b[k][j]

        return d
    else:
        a11 = divide11(a, n)
        a12 = divide12(a, n)
        a21 = divide21(a, n)
        a22 = divide22(a, n)
        b11 = divide11(b, n)
        b12 = divide12(b, n)
        b21 = divide21(b, n)
        b22 = divide22(b, n)
        k = int(n / 2)
        m1 = strassen(a11, minus(b12, b22, k), k)
        m2 = strassen(plus(a11, a12, k), b22, k)
        m3 = strassen(plus(a21, a22, k), b11, k)
        m4 = strassen(a22, minus(b21, b11, k), k)
        m5 = strassen(plus(a11, a22, k), plus(b11, b22, k), k)
        m6 = strassen(minus(a12, a22, k), plus(b21, b22, k), k)
        m7 = strassen(minus(a11, a21, k), plus(b11, b12, k), k)

        c11 = plus(minus(plus(m5, m4, k), m2, k), m6, k)
        c12 = plus(m1, m2, k)
        c21 = plus(m3, m4, k)
        c22 = minus(minus(plus(m5, m1, k), m3, k), m7, k)
        c = merge(c11, c12, c21, c22, k)
        return c


def generate_matrix(n):
    return [[randint(-5, 5) for _ in range(n)] for __ in range(n)]

d = 128
A = generate_matrix(d)
B = generate_matrix(d)

begin = perf_counter_ns()
C = strassen(A, B, d)
strassen_time = perf_counter_ns() - begin

for i in range(d):
    for j in range(d):
        C[i][j] = 0
begin = perf_counter_ns()
for i in range(d):
    for j in range(d):
        for k in range(d):
            C[i][j] += A[i][k] * B[k][j]
default_time = perf_counter_ns() - begin
print(strassen_time)
print(default_time)
print(strassen_time/default_time)