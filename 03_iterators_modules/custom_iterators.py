#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
>>> i = iter([1, 2, 3])
>>> c = cycle(i)
>>> c.next()
1
>>> c.next()
2
>>> c.next()
3
>>> c.next()
1

'''

def cycle(some_iter):
#   Текущий вариант реализации мне не нравится абслютно. 
#   Формально требования я выполнил, но такое ощущение что
#   все можно сделать намного проще и культурнее. Полез читать.
    while 1:
        #
        # Review: while 1 is deprecated variant, better use `while True`, but
        # the best is use `for` cycle :)
        #
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
    #
    # Review: overall idea is right, but implementation may be more cleaner
    #
    pass
    

#
# Review: better make doctests for single function inside docstring of this
# function
#
'''
>>> i1 = iter([1, 2, 3])
>>> i2 = iter([4, 5])
>>> c = chain(i1, i2)
>>> c.next()
1
>>> c.next()
2
>>> c.next()
3
>>> c.next()
4
>>> c.next()
5
>>> c.next()
Traceback (most recent call last):
  File ...
StopIteration
'''    
def chain(*args):
    for some_iter in args:
    #TODO: Подумать как обойтись без while 1
    #
    # Review: why need `while` if `for x in foo` do the same thing
    # more cleaner?
    #
        while 1:
            try:
                n = some_iter.next()
                yield n
            except StopIteration:
                break
    raise StopIteration
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

