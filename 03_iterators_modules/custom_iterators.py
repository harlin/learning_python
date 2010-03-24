#!/usr/bin/python
# -*- coding: UTF-8 -*-


def cycle(some_iter):
    '''
    This function presents a cyclic version of the provided iterator.
    Instead of throwing StopIteration at the end, it returns to the first element.
    
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
    #   Текущий вариант реализации мне не нравится абслютно.
    #   Формально требования я выполнил, но такое ощущение что
    #   все можно сделать намного проще и культурнее. Полез читать.
    while True:
        #
        # Review: while 1 is deprecated variant, better use `while True`, but
        # the best is use `for` cycle :)
        #
        item_list = []
        for n in some_iter:
            item_list.append(n)
            yield n

        some_iter = iter(item_list)
    #TODO: Придумать как это написать без применения тяжелых извращений
    #
    # Review: overall idea is right, but implementation may be more cleaner
    #
    pass


def chain(*args):
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
    for some_iter in args:
    #
    # Review: why need `while` if `for x in foo` do the same thing
    # more cleaner?
    #
    # Done
    #
        for n in some_iter:
            yield n
    raise StopIteration

if __name__ == "__main__":
    import doctest
    doctest.testmod()
