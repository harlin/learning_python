#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Property(object):
    '''
    >>> class Image(object):
    ...    height = Property(0)
    ...    width = Property(0)
    ...    path = Property('tmp')
    ...    size = Property(0)
    >>> img = Image()
    >>> img.height = 340
    >>> img.height
    340
    >>> img.path = '/tmp/x00.jpeg'
    >>> img.path
    '/tmp/x00.jpeg'
    >>> img.path = 320
    Traceback (most recent call last):
    ...
    TypeError
    '''

    def __init__(self, value=None):
        self._value = value

    def __set__(self, instance, value):
        if type(self._value) is type(value):
            self._value = value
        else:
            raise TypeError

    def __get__(self, instance, owner):
        return self._value


class TypeFixerMeta(type):

    def __init__(cls, name, bases, dictionary):
        def setter(instance, key, value):
            if not hasattr(instance, key):
                raise AttributeError("%s class has no attribute '%s'" % \
                    (instance.__class__.__name__, key))
            else:
                if type(getattr(instance, key)) is not type(value):
                    raise TypeError
                else:
                    object.__setattr__(instance, key, value)

        setattr(cls, '__setattr__', setter)


class Object:
    '''
    >>> class Image(Object):
    ...    height = 0
    ...    width = 0
    ...    path = '/tmp'
    ...    size = 0
    >>> img = Image()
    >>> img.height = 340
    >>> img.height
    340
    >>> img.path = '/tmp/x00.jpeg'
    >>> img.path
    '/tmp/x00.jpeg'
    >>> img.path = 320
    Traceback (most recent call last):
    ...
    TypeError
    '''
    __metaclass__ = TypeFixerMeta


if __name__ == "__main__":
    import doctest
    doctest.testmod()
