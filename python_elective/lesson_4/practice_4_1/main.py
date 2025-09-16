'''
import time

def calc_time():
    # начальное время
    # sek
    start_time = time.time()

    # код, время выполнения которого нужно измерить
    for i in range(0, 1000000):
        pass

    # конечное время
    end_time = time.time()

    # разница между конечным и начальным временем
    elapsed_time = end_time - start_time
    print('Elapsed time: ', elapsed_time)
'''


'''
import timeit

def example_func():
    for i in range(0, 1000000):
        pass


def calc_timeit(iter_count):
    # вычисление времени выполнения кода
    elapsed_time = timeit.timeit('example_func()',
                                 globals={'example_func': example_func},
                                 number=iter_count) / iter_count

    return elapsed_time


def write_exp_results():
    with open(r'results.txt', "w") as file:
        for ic in range(10, 101,20):
            file.write(str(ic) + ' '+str(calc_timeit(ic))+'\n')


def read_exp_results():
    f = open('results.txt')
    results = {}
    for line in f:
        ln = line.split()
        results[int(ln[0])] = float(ln[1])

    return results
'''

from joblib import parallel_backend

def mt_example():
    n = 100000
    dict = {}
    with parallel_backend('threading', n_jobs=4):
        for i in range(n):
            for j in range(10):
                dict[i] = i**2 + i**3 + i**4


def seq_example():
    n = 100000
    dict = {}
    for i in range(n):
        for j in range(10):
            dict[i] = i ** 2 + i ** 3 + i ** 4


import timeit

if __name__ == '__main__':
    '''

    #calc_time()

    #for i in range(10, 31,10):
    #    print(calc_timeit(i))

    #write_exp_results()
    res = read_exp_results()
    print(res)

    '''
    iter_count = 1
    print(timeit.timeit('mt_example()',
                  globals={'mt_example': mt_example},
                  number=iter_count) / iter_count)
    print(timeit.timeit('seq_example()',
                        globals={'seq_example': seq_example},
                        number=iter_count) / iter_count)
