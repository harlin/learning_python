#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Observable:
    def __init__(self,**kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]
    def __repr__(self):
#        custom_repr = self.__name__
#   TODO:  Придумать, как сюда закинуть имя класса
#   TODO:  Подумать над списком публичных атрибутов
        custom_repr = ""
        custom_repr += "("
        for arg in self.__dict__.keys():
            if arg[0] != '_':
                custom_repr += arg
                custom_repr += "="
                custom_repr += repr(self.__dict__[arg])
                custom_repr += ", "
        custom_repr = custom_repr[:-2]
        custom_repr += ")"
        return custom_repr
        

# test
print "Begin test #1: Observable: "

class X(Observable):
    pass
x = X(foo=1, bar=5, _bazz=12, name='Amok', props=('One', 'two'))
print x
print x.foo
print x.name
print x._bazz
