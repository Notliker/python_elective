import time
import random
from modules import matrix_on_matrix, matrix_on_vec, matrix_trace, scal_mul_vec, histogram

def gen_matrix(n, m, l=0, h=10):
    return [[random.randint(l, h) for _ in range(m)] for __ in range(n)]

def gen_vector(n, l=0, h=10):
    return [random.randint(l, h) for _ in range(n)]

def timeit_time(func, *args, repeats=3, **kwargs):
    t0 = time.time()
    func(*args, **kwargs)
    dt = time.time() - t0
    return dt

size = [16, 32, 64, 128, 256]
lines = []
lines.append("size;matrix_on_matrix(s);matrix_on_vec(s);matrix_trace(s);scal_mul_vec(s);histogram(s)")

for n in size:
    mx_1 = gen_matrix(n, n)
    mx_2 = gen_matrix(n, n)
    vec_1 = gen_vector(n)
    vec_2 = gen_vector(n)

    t_mm = timeit_time(matrix_on_matrix, mx_1, mx_2, repeats=3)
    t_mv = timeit_time(matrix_on_vec, mx_1, vec_1, repeats=5)
    t_tr = timeit_time(matrix_trace, mx_1, repeats=10)

    t_dot = timeit_time(scal_mul_vec, vec_1, vec_2, 1, repeats=10)

    t_hist = timeit_time(histogram, vec_1, 10, repeats=5)

    lines.append(f"{n};{t_mm:.6f};{t_mv:.6f};{t_tr:.6f};{t_dot:.6f};{t_hist:.6f}")

with open("python_elective/homework_2/bench.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
for row in lines:
    print(row)

