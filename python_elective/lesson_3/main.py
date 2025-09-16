
'''
def func():
    pass

func()


'''

'''
def func_welcome():
    print("Quick start!")


func_welcome()
'''

'''

import random

b = 3

def func_rand_value():
    val = random.uniform(0,1)
    # b = random.uniform(0,1)
    return val


a = func_rand_value()
print(a)
print(b)
'''

'''
import random

def f1():
    print("I'm function 1!")
    return 1

def f2():
    print("I'm function 2!")
    return 2

def func_choise():
    val = random.uniform(0, 1)
    if val < 0.5:
        return f1()
    else:
        return f2()

f = func_choise()
print(f)
'''

'''
def func_max(a, b):
    a += 1
    b += 1
    return max(a,b)

a = 0.5
b = 0.7
print(func_max(a,b))
print(a)
print(b)
'''

'''
def calculation(a, b, op):
    return op(a,b)

def op_sum(a,b):
    return a+b

def op_mult(a,b):
    return a*b

print( calculation(3,4,op_sum))

print( calculation(2,5,op_mult))
'''
'''
def func_many_args(*argv):
    for arg in argv:
        print(arg, type(arg))

func_many_args(3,5,'study',(1,2), {1:2, 4:5})
print('-------------------')
func_many_args('good', 'job')
'''

'''
def func_named_args(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

func_named_args(one = 1, two = 2.0, three  ='three')

params = {'one':1, 'two':2.0, 'three': 'three'}
func_named_args(**params)
'''
                
'''
def func_one_plus_argv(a, *argv):
    if a > 0:
        for arg in argv:
            print(arg, type(arg))
    else:
        print('Change negative on positive')

func_one_plus_argv(1,2,3)
'''

'''
def fill_list(a, l=None):
    if l is None:
        l = []
    l.append(a)
    return l

l = [1,2,3]
fill_list(3)
print(l)
'''

'''
def f1():
    print('F1 is called')

    def f2():
        print('F2 is called')

    f2()

f1()
'''

# recursion
'''
def fact(n):
    if(n <= 1): return 1
    else: return n*fact(n-1)

print(fact(5))
'''

'''
def op_sum(a,b):
    return a + b

def op_diff(a,b):
    return a - b

def op_mult(a,b):
    return a * b

def inform_result(a,b,op_func):
    print("Result is ", op_func(a,b))

def processing():
    a = input().split()
    while len(a) > 1:
        f = op_sum
        if a[1] == '*':
            f = op_mult
        elif a[1] == '-':
            f = op_diff

        inform_result(int(a[0]),
                      int(a[2]),
                      f )

        print("Input new line")
        a = input().split()


processing()
'''

#####
##### LIST
#####

'''
import random

l = [random.uniform(-1,1) for i in range(100)]

def print_list(l):
    for i in range(10):
        print(l[i: i*10])

def processing(l, a, b):
    sum = 0
    count = 0

    for val in l:
        if val >= a and val <=b:

            sum += val
            count += 1

    av = sum / count
    for i in range(len(l)):

        if l[i] < a  or l[i] > b:
            l[i] = av



print_list(l)
processing(l, -0.5, -0.4)
print("--------------------------------")
print_list(l)

'''

'''
import random



def func_choise():
    val = random.uniform(0, 1)

    def f1():
        print("I'm function 1!")
        return 1

    def f2():
        print("I'm function 2!")
        return 2

    if val< 0.5:
        return f1
    else:
        return f2

f = func_choise()
print(f())

'''
'''

def sum(a,b):
    return a+b

def mult(a,b):
    return a*b

def decorator_math_scalar(func):
    def wrapper(*argv):
        result = func(argv[0],argv[1])* argv[2]
        return result
    return wrapper

print(decorator_math_scalar(mult)(1,2,0.5))


@decorator_math_scalar
def diff(a,b):
    return a-b

print(diff(3,4,0.5,5))
print(sum(3,4))

'''



def decorator_math_scalar(c):

    def decorator(func):

        def wrapper(*argv):
            result = func(argv[0],argv[1])*c
            return result

        return wrapper

    return decorator

@decorator_math_scalar(0.5)
def diff(a,b):
    return a-b


@decorator_math_scalar(0.1)
def sum(a,b):
    return a + b

print(sum(5,7))
