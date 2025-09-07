
#print("Hello, students! Welcome to our course! ")

# single comment

'''
Multi-line comments example
'''

'''
a = int(input())
print(a)
print(type(a))
'''

'''
a = 123
b = a
a = 10
print(a,b)

x,y = 'car', 2

print(x,y)
print(type(x))
print(type(y))
'''

'''
# Formatting output
a,b,=10,1000
print('The value of a is {} and b is {}'.format(a,b))
print(a, b)
print(a,b, sep='*')
'''

'''
#a = complex(input())
a = complex(0,1)
print(a)
'''

'''
#dec
a = 10
print(a)

#bin
a = 0b10
print(a)

#oct
a = 0O123
print(a)

#hex
a = 0X12A
print(a)
'''

''''
f = .3
print(f)
print(0.3)
f = .04e3
print(f)
'''

'''
flag = True
print(flag)
print(type(flag))


t = {}
print(bool(t))

s = 3 < 4
print(s)
'''

################## SET ##################################
'''
s = set((1,2,3,))
print(s)
print(type(s))
'''


################## LIST ##################################
'''
my_list1 = list((1, 2, 3))
print(my_list1)
'''

'''
# Output [1, 2, 3]

# Using square brackets[]
my_list2 = [1, 2, 3]
print(my_list2)
# Output [1, 2, 3]

# with heterogeneous items
my_list3 = [1.0, 'Jessa', 3]
print(my_list3)
# Output [1.0, 'Jessa', 3]

# empty list using list()
my_list4 = list()
print(my_list4)
# Output []

# empty list using []
my_list5 = []
print(my_list4)
'''

'''
a = [1,2,3,4]
print(a[0])
print(a[3])
print(a[-1])
print(a[-2])

print(a)
print(a[:2])
print(a[1:])


print(a[1:3])

a[2] = 10
a[1] = a[3]**3

a.append(67)

print(a)

print(sum(a))

a.append(1)
print(a)

s_a = set(a)
print(s_a)

print(len(a))
print(len(s_a))
'''

######################### DICTIONARY ##########################

'''
d = {'a': 1, 'b':2 }
print(d)
print(d['a'])
d['d'] = 10
print(d)
'''

####################### TUPLE ######################

'''
t = 12345, 54321, 'hello!'
print(t)
print(type(t))
print(t[0])
'''