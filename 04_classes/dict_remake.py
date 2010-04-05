#!/usr/bin/python
# -*- coding: UTF-8 -*-


class DictAttr:
    #
    # I learned a lot from this realization and comments on it
    # I may return to it later - because a total rework is needed here
    #
    '''
    >>> x = DictAttr(('one', 1), ('two', 2), ('three', 3))
    >>> x
    {'one': 1, 'two': 2, 'three': 3}
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
    AttributeError: DictAttr instance has no attribute 'five'
    '''
    def __init__(self, *args, **kwargs):
        self.__keys = []
        #
        # Review: dict supports both pairs and dict:
        # dict([('x', 1), ('y', 2)])
        # dict({'x': 1, 'y': 2})
        #
        for pair in args:
            setattr(self, pair[0], pair[1])
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __contains__(self, key):
        return key in self.__keys
        
    def __delattr__(self, key):
        self.__dict__.pop(key)
        self.__keys.remove(key)
    
    def __delitem__(self, key):
        delattr(self, key)

    def __getitem__(self, key):
        if key in self.__keys:
            return getattr(self, key)
        else:
            raise KeyError, key
       
    def __eq__(self, other):
        if not isinstance(other, DictAttr):
            return False
        if self.__keys != other.__keys:
            return False
        for key in self.__keys:
            if self.get(key) != other.get(key):
                return False
        return True

    def __len__(self):
        return len(self.__keys)

    def __ne__(self, other):
        return not self.__eq__(self. other)

    def __repr__(self):
        custom_repr = "{"
        custom_repr += ', '.join( [repr(key) + ": " + repr(getattr(self, key)) for key in self.__keys] )
        custom_repr += "}"
        return custom_repr

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        #
        # Review: Try to do reverse logic: make setitem default action, but
        # setattr (exclude non-public attr [remebmer convention about '_X'
        # names]) as setitem alias. See. Try it, and you'll see how code will
        # look better.
        #
        # It's common sence to use some non-public dict attr as storage for
        # custom keys, instead of use __dict__ as common storage and
        # self.__keys as "keys filtering".
        if key not in self.__keys and key != '_DictAttr__keys':
        #TODO: Think how bad it is    
            self.__keys.append(key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        custom_repr = "{"
        #
        # Review: too long line, try to keep 80 cols limit
        #
        custom_repr += ', '.join( [repr(key) + ": " + repr(getattr(self, key)) for key in self.__keys] )
        custom_repr += "}"
        return custom_repr

    def clear(self):
        for key in self.__keys:
            delattr(self, key)
    
    def copy(self):
    #TODO:
    #   A bit scary, but i think this'll work
        #
        # Review: scary is reasonable for "generic dict", but both .keys() and
        # .values() are controlled by you and they keep right order, so you
        # may sleep quietly.
        #
        D = DictAttr(zip(self.keys(), self.values()))
        return D
    
    def fromkeys(keys, values = []):
        values.append( [None] * (len(keys) - len(values)) )
        D = DictAttr(zip(keys, values))
        return D
    
    def get(self, key, default_value = None):
        if key in self.__keys:
            return getattr(self, key)
        else:
            return default_value

    def has_key(key):
        return key in self.__keys

    def items(self):
        return [(key, getattr(self, key)) for key in self.__keys]
    
    #
    # Review: WRONG indent for comment. Comment MUST have the same indent
    # as code. After `def f():` indent should have NEXT level.
    #
    def iteritems(self):
    #TODO:
    #   I'm not sure whether this realization satisfies the conditions
        #
        # Review: better use generator expression inside iteritems and
        # list(self.iteritems()) inside items :)
        #
        return iter(self.items())
        
    def iterkeys(self):
        return iter(self.keys())
        
    def itervalues(self):
        return iter(self.values())
    
    def keys(self):
        return self.__keys
            
    def pop(self, key, default_value = None):
    #TODO: 
    #   Current realization has a flaw: it will raise an exception if None
    #   is passed as a default value
        if key in self.__keys:
            value = getattr(self, key)
            delattr(self,key)
            return value
        else:
            if default_value == None:
                raise KeyError, key
            else:
                return default_value

    def popitem(self):
        if not filter((lambda x: x[0] != '_'), dir(self)):
            raise KeyError
        else:
            key = filter((lambda x: x[0] != '_'), dir(self))[0]
            value = getattr(self, key)
            delattr(self,key)
            return key, value            

    def setdefault(self, key, default_value = None):
        if key in self.__keys:
            return getattr(self, key)
        else:
            setattr(self, key, default_value)
            return default_value

    def update(self, some_container, **kwargs):
    #TODO:
    #   I don't like how the check is done
        if 'keys' in dir(some_container):
            for key in some_container.keys():
                setattr(self, key, some_container[key])
        else:
            for pair in some_container:
                setattr(self, pair[0], pair[1])
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])    
    
    def values(self):
        return [getattr(self, key) for key in self.keys()]


