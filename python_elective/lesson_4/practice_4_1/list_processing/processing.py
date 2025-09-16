
def half_less(l, T):
    for i in range(len(l)):
        if l[i] < T:
            l[i] = 0

def list_add(a,b):
    c = [0]*len(a)
    for i in range(len(a)):
        c[i] = a[i] + b[i]

    return c


if __name__ == '__main__':
    pass