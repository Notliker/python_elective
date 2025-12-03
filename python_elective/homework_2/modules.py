def matrix_on_matrix(matrix1, matrix2):
    res=[]
    for row in range(len(matrix1)):
        res.append([])
        for column in range(len(matrix2[0])):
            row_sum=0
            for ind in range(len(matrix1[0])):
                row_sum+=matrix1[row][ind] * matrix2[ind][column]
            res[row].append(row_sum)
    return res

matrix1 = [[0,1,2],[1,0,2],[2,1,0],[0,0,1]]
matrix2 = [[0,1],[1,0],[1,1]]
print(matrix_on_matrix(matrix1,matrix2))

def matrix_on_vec(matrix, vec):
    res=[]
    for i in range(len(matrix)):
        row_sum=0
        for j in range(len(matrix[i])):
            row_sum+=matrix[i][j]*vec[j]
        res.append(row_sum)
    return res

def matrix_trace(matrix):
    res=0
    for i in range(len(matrix)):
        res+=matrix[i][i]
    return res
print(matrix_trace([[1,2,3],[4,5,6],[7,8,9]]))

def scal_mul_vec(vec1, vec2, cos=None):
    res=0
    for i in range(len(vec1)):
        res += vec1[i]*vec2[i]
    res*=cos
    return res

def histogram(data, bins):
    r=max(data)
    l=min(data)
    b_size=(r-l)/bins
    hist=[""]*bins
    for num in data:
        b_ind = int((num - l) / b_size)
        if b_ind==bins:
            b_ind=bins-1
        hist[b_ind]+='*'
    return hist

import random
data = [random.randint(0,15) for _ in range(5)]
print(data, '\n',histogram(data, 2))

def grad_conv(matrix):
    kernel=[-1, 0, 1]
    res=[]
    for i in range(len(matrix)-len(kernel)+1):
        row_sum=0
        for j in range(len(kernel)):
            row_sum+=matrix[i+j]*kernel[j]
        res.append(row_sum)
    return res

print(grad_conv( [1, 4, 2, 3, 2])) # [1, -1, 0]

def write2file(file, data):
    try:
        with open(file, 'w') as f:
            f.write(str(data))
    except:
        raise ValueError("There is no file on this path")

def readfile(file):
    try:
        with open(file, 'r') as f:
            f.read()
    except:
        raise ValueError("There is no file on this path")