#!/usr/bin/python
# -*- coding: UTF-8 -*-

print "-"*60

# Задача1: написать функцию, складыющую аргументы, передаваемые по очереди, либо в виде списка/кортежа
"""
# мой первоначальный вариант был такой 
# (опустим тот факт что он работает только с целыми/вещественными числами, но не со строками)
# однако, такая штука не работает на списках и кортежах, 
# поэтому пришлось усложнять. 
# Подозреваю, что таки можно сделать проще
# текущий вариант мне не очень нравится
def listSum(*listArg):
	res = 0
	for x in listArg:
		res += x
	return res
"""

def listSum(*listArg):
	listToAdd = []
	for L in listArg :
		if( isinstance(L, (list, tuple)) ):
			listToAdd.extend(L)
		else :
			listToAdd.append(L)

#	result = listToAdd[0]
#	for x in listToAdd[1:]:
#		result += x

	return sum(listToAdd[1:],listToAdd[0])

print "Task1. Results:"
print listSum(1,2,3)
print listSum('1','2','3')
print listSum([1,2,3])
print listSum((1,2,3))
print listSum([1,2,3],(1,2,3),4)
print "-"*60


# Задача2: Написать функцию-фабрику, возвращающую функцию сложения с аргументом

def additionEmbedded(x) : # вариант с внутренним определением искомой функции
	def addX(y):
		return x+y
	return addX

def additionLambda(x): # вариант с анонимной лямбда-функцией
	return (lambda y: x+y)

print "Task2. Results:"

add5 = additionEmbedded(5)
print add5(3)

add7 = additionLambda(7)
print add7(3)

print "-"*60

# Задача3: Написать функцию-фабрику, возвращающую список функций сложения с аргументом
# TODO: Понять, почему мои изначальные варианты не работают.
"""
# Я предполагаю, что должно работать только для целых чисел. 
# Не могу придумать логичного метода работы на других типах
"""


def addRangeLambda(x,y) : # вариант с лямбда-выражениями
#	return [(lambda s: s+t) for t in range(x,y+1)]
# TODO: Понять, почему такой вариант не работает так как я от него ожидаю
	return [additionLambda(t) for t in range(x,y+1)]


print "Task3. Results:"


addListL = addRangeLambda(2,8)
add4 = addListL[2]
print add4(9)

print "-"*60


# Задача4: Написать аналог функции map

def myMap(funcList,argList):
	if type(funcList) != type([]): # предварительное условие, на случай если передан не список функций
		myfuncList = [funcList]
	else:
		myfuncList = funcList

	if type(argList) != type([]): # предварительное условие, на случай если передан не список аргументов
		myargList = [argList]
	else:
		myargList = argList

	return [ tuple( [ func(x) for x in myargList ] ) for func in myfuncList ]

print "Task4. Results:"

print myMap([add5,add7],[1,2,3])

print myMap(addRangeLambda(3,7),[1,2,3])

print "-"*60

