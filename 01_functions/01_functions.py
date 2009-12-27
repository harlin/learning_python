#!/usr/bin/python
# -*- coding: UTF-8 -*-

print "-"*60

# Задача1: написать функцию, складыющую аргументы, передаваемые по очереди, либо в виде списка/кортежа


def list_sum(*list_arg):
    list_to_add = []
    for l in list_arg:
        if( isinstance(l, (list, tuple)) ):
            list_to_add.extend(l)
        else :
            list_to_add.append(l)

    result = list_to_add[0]
    for x in list_to_add[1:]:
        result += x

#    return sum(list_to_add[1:], list_to_add[0])
    return result

print "Task1. Results:"
print list_sum(1,2,3)
print list_sum('1','2','3')
print list_sum([1,2,3])
print list_sum((1,2,3))
print list_sum([1,2,3], (1,2,3), 4)
print "-"*60


# Задача2: Написать функцию-фабрику, возвращающую функцию сложения с аргументом

def addition_embedded(x): # вариант с внутренним определением искомой функции
    def addX(y):
        return x+y
    return addX

def addition_lambda(x): # вариант с анонимной лямбда-функцией
    return (lambda y: x+y)

print "Task2. Results:"

add5 = addition_embedded(5)
print add5(3)

add7 = addition_lambda(7)
print add7(3)

print "-"*60

# Задача3: Написать функцию-фабрику, возвращающую список функций сложения с аргументом

def add_range_lambda(x, y): # вариант с лямбда-выражениями
    return [addition_lambda(t) for t in range(x, y+1)]


print "Task3. Results:"


addListL = add_range_lambda(2, 8)
add4 = addListL[2]
print add4(9)

print "-"*60


# Задача4: Написать аналог функции map

def my_map(func_list, arg_list):
    if not isinstance(func_list, list): # предварительное условие, на случай если передан не список функций
        myfunc_list = [func_list]
    else:
        myfunc_list = func_list

    if not isinstance(arg_list, list): # предварительное условие, на случай если передан не список аргументов
        myarg_list = [arg_list]
    else:
        myarg_list = arg_list

    return [ tuple( [ func(x) for x in myarg_list ] ) for func in myfunc_list ]

print "Task4. Results:"

print my_map([add5,add7], [1,2,3])

print my_map(add_range_lambda(3,7), [1,2,3])

print "-"*60

