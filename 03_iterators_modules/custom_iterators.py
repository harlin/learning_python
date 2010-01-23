#!/usr/bin/python
# -*- coding: UTF-8 -*-


def cycle(some_iter):
    #TODO: Придумать как это написать
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
i1 = iter([1, 2, 3])
i2 = iter([4, 5])
c = chain(i1, i2)
for i in range(6):
    print c.next()

