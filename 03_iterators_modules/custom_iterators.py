#!/usr/bin/python
# -*- coding: UTF-8 -*-


def cycle(some_iter):
#   Текущий вариант реализации мне не нравится абслютно. 
#   Формально требования я выполнил, но такое ощущение что
#   все можно сделать намного проще и культурнее. Полез читать.
    while 1:
        item_list = []
        while 1:
            try:
                n = some_iter.next()
                item_list.append(n)
                yield n
            except StopIteration:
                break
        some_iter = iter(item_list)
    #TODO: Придумать как это написать без применения тяжелых извращений
    pass
    
def chain(*args):
    for some_iter in args:
    #TODO: Подумать как обойтись без while 1
        while 1:
            try:
                n = some_iter.next()
                yield n
            except StopIteration:
                break
    raise StopIteration
    
#test
#
# Review: write tests as doctests
#
print "Begin test #1: cycle"
i = iter([1, 2, 3])
c = cycle(i)
for i in xrange(5):
    print c.next()

print "Begin test #2: chain"
i1 = iter([1, 2, 3])
i2 = iter([4, 5])
c = chain(i1, i2)
for i in range(6):
    print c.next()
