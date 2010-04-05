#!/usr/bin/python
# -*- coding: UTF-8 -*-


def cycle(some_iter):
    '''
    This function presents a cyclic version of the provided iterator.
    Instead of throwing StopIteration at the end, it
    goes back to the first element.

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
    # Renewed realization with memory leak fixed
    # Also minor bug fixed

    item_list = []
    for n in some_iter:
        item_list.append(n)
        yield n

    i = 0
    n = len(item_list)
    while True:
        yield item_list[i % n]
        i += 1


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
        for n in some_iter:
            yield n

    return

if __name__ == "__main__":
    import doctest
    doctest.testmod()
