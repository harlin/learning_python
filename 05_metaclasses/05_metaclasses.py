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


class LengthError(Exception):
    pass


class Integer(object):

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError
        else:
            self._value = value

    def __get__(self, instance, owner):
        return self._value


class Str(object):

    def __init__(self, length):
        self._length = length

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError
        elif len(value) > self.__length:
            raise LengthError
        else:
            self.__value = value

    def __get__(self, instance, owner):
        return self.__value

    def getlength(self):
        return self._length


class Table(type):
    #
    # I somehow like this implementation better, although it still
    # uses almost the same principle
    # I was wondering whether i can use some "registry" to store
    # table fields, but failed to find out how to intercept
    #   "width = Integer()"
    # inside a class definition
    #
    '''
    >>> class Image():
    ...    __metaclass__ = Table
    ...    height = Integer()
    ...    width = Integer()
    ...    path = Str(128)
    >>> print Image.sql()
    CREATE TABLE image (
        width integer,
        height integer,
        path varchar(128)
    )
    '''
    def __new__(metacls, name, bases, dictionary):

        fields = {}
        for key in dictionary:
            if not key[:2] is '__':
                value = dictionary[key]
                if isinstance(value, Integer):
                    fields[key] = 'integer'
                if isinstance(value, Str):
                    fields[key] = 'varchar(%i)' % value.getlength()

        dictionary['field_registry'] = fields

        return super(Table, metacls).__new__(metacls, name, bases, dictionary)

    def sql(cls):
        schema = "CREATE TABLE "
        schema += cls.__name__.lower()
        schema += " (\n"
        for key, value in cls.field_registry.items():
            schema += "    %s %s,\n" % (key, value)

        schema = schema[:-2]
        schema += "\n)"
        return schema


if __name__ == "__main__":
    import doctest
    doctest.testmod()
