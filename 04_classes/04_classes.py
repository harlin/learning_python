#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Observable:
    def __init__(self,**kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
    def __repr__(self):
        custom_repr = self.__class__.__name__
        custom_repr += "("
        custom_repr += ', '.join( [arg + "=" + repr(getattr(self, arg)) for arg in dir(self) if arg[0] != '_'] )
        custom_repr += ")"
        return custom_repr
        

class DictAttr:
    def __init__(self, *args, **kwargs):
        self.__keys = []
        for pair in args:
            setattr(self, pair[0], pair[1])
            if not pair[0] in self.__keys:
                self.__keys.append(pair[0])
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
            if not key in self.__keys:
                self.__keys.append(key)

    def __contains__(self, key):
        return key in self.__keys
        
    def __delitem(self, key):
        delattr(self, key)
        self.__keys.remove(key)

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

    def __setitem__(self, key, value):
        setattr(self, key, value)
        if key not in self.__keys:
            self.__keys.append(key)

    def __str__(self):
        custom_repr = "{"
        custom_repr += ', '.join( [repr(key) + ": " + repr(getattr(self, key)) for key in self.__keys] )
        custom_repr += "}"
        return custom_repr

    def clear(self):
        for key in self.__keys:
            delattr(self, key)
        self.__keys = []
    
    def copy(self):
    #TODO:
    #   A bit scary, but i think this'll work
        D = DictAttr.fromkeys(self.keys(), self.values())
        return D
    
    def fromkeys(keys, values = []):
    #TODO:
    #   This realisation is awful
        values.append( [None] * (len(keys) - len(values)) )
        D = DictAttr()
        for i in xrange(len(keys)):
            D.__setitem__(keys[i], values[i])
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
    
    def iteritems(self):
    #TODO:
    #   I'm not sure whether this realization satisfies the conditions
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
            self.__keys.remove(key)
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
            self.__keys.remove(key)
            return key, value            

    def setdefault(self, key, default_value = None):
        if key in self.__keys:
            return getattr(self, key)
        else:
            setattr(self, key, default_value)
            self.__keys.append(key)
            return default_value

    def update(self, some_container, **kwargs):
    #TODO:
    #   I don't like how the check is done
        if 'keys' in dir(some_container):
            for key in some_container.keys():
                setattr(self, key, some_container[key])
                if not key in self.__keys:
                    self.__keys.append(key)
        else:
            for pair in some_container:
                setattr(self, pair[0], pair[1])
                if not pair[0] in self.__keys:
                    self.__keys.append(pair[0])
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])    
            if not key in self.__keys:
                self.__keys.append(key)    
    
    def values(self):
        return [getattr(self, key) for key in self.keys()]

# test
print "Begin test #1: Observable: "

class X(Observable):
    pass
x = X(foo=1, bar=5, _bazz=12, name='Amok', props=('One', 'two'))
print x
print x.foo
print x.name
print x._bazz


print "Begin test #2: DictAttr: "

x = DictAttr(('one', 1), ('two', 2), ('three', 3))
print x
print x['three']
print x.get('one')
print x.get('five', 'missing')
print x.one
print x.five
