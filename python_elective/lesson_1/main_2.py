####################################################
#
#
##########  PRACTICE 1.2 ########################
#
#
######################################################

##### LESS|MORE IF-ELSE

'''
a = int(input())

if a >= 0:
    print("Correct input")
    a += 2
else:
    print("Incorrect input")
    a -= 2

print(a)
'''
########## MIN NUMBER ######

'''
a = int(input())
b = int(input())
c = int(input())


if (a < b) and (a < c):
    print("a is MIN value")
elif (b < a) and (b < c):
    print("b is MIN value")
else:
    print("c is MIN value")
'''

########## WHAT A NUMBER? ######

'''
finished_str = "GOOD JOB! THE GAME IS FINISHED!"
template_str = "THE NUMBER IS {}! THE GAME IS FINISHED!"

num_eq_str = "THE NUMBER IS {}?"

print(num_eq_str.format(3))
answer = int(input())

if answer:
    print(finished_str)
else:
    print("THE NUMBER IS  MORE THAN 3?")
    answer = int(input())
    if answer:
        print(num_eq_str.format(4))
        answer = int(input())

        if answer:
            print(finished_str)
        else:
            print(template_str.format(5))
    else:

        print(num_eq_str.format(1))
        answer = int(input())

        if answer:
            print(finished_str)
        else:
            print(template_str.format(2))
'''


