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
        try:
            return self[key]
        except(KeyError):
            raise AttributeError("%s class has no attribute '%s'" % \
                (self.__class__.__name__, key))


class XDictAttr(DictAttr):
    #
    # TODO: This needs to be re-checked for consistency
    # For example, if X class has def_foo method, what should happen
    # if the X.foo = 8 is typed:
    #
    # a) the get_foo method is re-defined so it returns 8 now
    # b) the get_foo method is not re-defined, but X.foo now returns 8
    # c) X.foo = 8 causes an Exception (simulation of "read-only" attr)
    # d) none of those, X.foo still returns 5 - this is the current situation
    #
    # a), b) or c) seem consistent, but d is not
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
    >>> x.three
    3
    >>> x.bar
    12
    >>> x['foo']
    5
    >>> x.get('foo', 'missing')
    5
    >>> x.get('bzz', 'missing')
    'missing'
    '''

    def __repr__(self):
        #
        # Added overload to fit the test provided
        #
        return "%s: %s" % (self.__class__.__name__, DictAttr.__repr__(self))

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, DictAttr.__str__(self))

    def __getattr__(self, key):
        #
        # I tried to simplify this part a bit, but for some reason it starts
        # falling into recursion when getattr(self, meth_name) is used
        #
        meth_name = "get_" + key
        if hasattr(self, meth_name):
            meth = getattr(self, meth_name)
            return meth()
            ## return getattr(self.__class__, meth_name)()
        else:
            return DictAttr.__getattr__(self, key)

    def __getitem__(self, key):
        #
        # Maybe the check for "get_" method deserves to be moved to a separate
        # method for DRY reasons, but i think that it'll make the result less
        # understandable
        #
        meth_name = "get_" + key
        if hasattr(self.__class__, meth_name):
            meth = getattr(self, meth_name)
            return meth()
        else:
            return DictAttr.__getitem__(self, key)

    def get(self, key, default):
        meth_name = "get_" + key
        if hasattr(self, meth_name):
            meth = getattr(self, meth_name)
            return meth()
        else:
            return DictAttr.get(self, key, default)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
