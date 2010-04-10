#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Observable:
    '''
    >>> class X(Observable): pass
    >>> x = X(foo=1, bar=5, _bazz=12, name='Amok', props=('One', 'two'))
    >>> print x
    X(bar=5, foo=1, name='Amok', props=('One', 'two'))
    >>> x.foo
    1
    >>> x.name
    'Amok'
    >>> x._bazz
    12
    >>> x.name = 'Brian'
    >>> x.name
    'Brian'
    '''

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __repr__(self):
        custom_repr = self.__class__.__name__
        custom_repr += "("
        custom_repr += ', '.join([arg + "=" + repr(getattr(self, arg)) \
            for arg in dir(self) if arg[0] != '_'])
        custom_repr += ")"
        return custom_repr


class DictAttr(dict):
    #
    # Renewed version.
    # Old version moved to separate file for the greater good.
    #
    # I must admit that the first test (the one with __init__ used)
    # was changed by me - the reason behind this is that
    # in the requirements it is stated that the class must "replic" dict class
    # and this is how dict reacts:
    # 1. It does not take more than 1 argument in a constructor
    # 2. The order of the keys may not coincide with the order they were added
    #
    '''
    >>> x = DictAttr([('one', 1), ('two', 2), ('three', 3)])
    >>> x
    {'three': 3, 'two': 2, 'one': 1}
    >>> x['three']
    3
    >>> x.get('one')
    1
    >>> x.get('five', 'missing')
    'missing'
    >>> x.one
    1
    >>> x.five
    Traceback (most recent call last):
    ...
    AttributeError: DictAttr class has no attribute 'five'
    >>> x.update({'three': 8, 'four': 4, 'five': 5})
    >>> x.three
    8
    >>> x.get('five')
    5
    '''

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        #
        # Actually, I'm highly confused that this approach works
        # I was expecting that self[key] would call for self.__getattr__
        # again, thus creating an infinite recursion
        #
        # Review: __getattr__ is called on <dot> expanding: self.some
        # When you call self[key], there is no <dot>, only brackets.
        #
        # Yes, but self[key] does implicitly call self.__getitem__
        # Where the <dot> appears
        #
        try:
            return self[key]
        except(KeyError):
            raise AttributeError("%s class has no attribute '%s'" % \
                (self.__class__.__name__, key))


class GetMethodError(Exception):
    pass


class XDictAttr(DictAttr):
    #
    # TODO: Add more tests
    #
    # TODO: Find out why placing GetMethodError definition inside the
    # class fails
    #
    '''
    >>> class X(XDictAttr):
    ...     def get_foo(self):
    ...         return 5
    ...     def get_bar(self):
    ...         return 12

    >>> x = X({'one': 1, 'two': 2, 'three': 3})
    >>> x
    X: {'one': 1, 'three': 3, 'two': 2}
    >>> x['one']
    1
    >>> x['four']
    Traceback (most recent call last):
    ...
    KeyError: 'four'
    >>> x.three
    3
    >>> x.bar
    12
    >>> x.foobar
    Traceback (most recent call last):
    ...
    AttributeError: X class has no attribute 'foobar'
    >>> x['foo']
    5
    >>> x.get('foo', 'missing')
    5
    >>> x.get('bzz', 'missing')
    'missing'
    >>> x.foo = 8
    >>> x.get('foo', 'missing')
    8
    '''

    def __repr__(self):
        #
        # Added overload to fit the test provided
        #
        return "%s: %s" % (self.__class__.__name__, DictAttr.__repr__(self))

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, DictAttr.__str__(self))

    def _get_check(self, key):
        #
        # This inner method is used for check, if there does exist a "get_key"
        # I tried to simplify this part a bit, but for some reason it starts
        # falling into recursion when getattr(self, meth_name) is used
        #
        meth_name = "get_" + key
        if hasattr(self.__class__, meth_name):
            meth = getattr(self, meth_name)
            return meth()
        else:
            raise GetMethodError(key)

    def __getattr__(self, key):
        try:
            return DictAttr.__getattr__(self, key)
        except AttributeError:
            try:
                return self._get_check(key)
            except GetMethodError:
                raise AttributeError("%s class has no attribute '%s'" % \
                    (self.__class__.__name__, key))

    def __getitem__(self, key):
        try:
            return DictAttr.__getitem__(self, key)
        except KeyError:
            try:
                return self._get_check(key)
            except GetMethodError:
                raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


class IterableRegisterMetaClass(type):

    def __init__(cls, name, bases, dictionary):

        def counter(instance):
            instance.__class__._instances.append(instance)

        def decounter(instance):
            instance.__class__._instances.remove(instance)

        setattr(cls, '__init__', counter)
        setattr(cls, '__del__', decounter)
        setattr(cls, '_instances', [])

    def __iter__(cls):
        return iter(cls._instances)


class Reg:
    '''
    >>> x = Reg()
    >>> y = Reg()
    >>> z = Reg()
    >>> for i in Reg:
    ...     print [x, y ,z].index(i)
    0
    1
    2
    '''

    __metaclass__ = IterableRegisterMetaClass

        #
        # Review: this code should be really in metaclass.
        #
        # Yes. Actually, i was initially intending that the metaclass
        # would just add an iterator, but
        #   return iter(cls.instances)
        # actually broke this intention (and I happened be too lazy
        # to make everything consistent)
        #


if __name__ == "__main__":
    import doctest
    doctest.testmod()
