import random
import list_processing.print as lp
import list_processing.processing as lpp
#from list_processing import *


if __name__ == '__main__':
    #l = [random.random() for val in range(100)]
    #lp.printing(l)

    a = [random.random() for val in range(10)]
    b = [random.random() for val in range(10)]
    print("Init arrays")
    print(a)
    print(b)

    #lpp.half_less(a, 0.5)
    #lpp.half_less(b, 0.1)
    print("Thresholded arrays")
    print(a)
    print(b)

    c = lpp.list_add(a,b)
    print("Sum of arrays")
    print(c)
