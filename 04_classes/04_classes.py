#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Observable:
    def __init__(self,**kwargs):
        for key in kwargs.keys():
            #
            # Review: __dict__ is not public interface, use setattr instead
            #
            self.__dict__[key] = kwargs[key]
    def __repr__(self):
#        custom_repr = self.__name__
#   TODO:  Придумать, как сюда закинуть имя класса
#   TODO:  Подумать над списком публичных атрибутов
        #
        # Review: see PEP-8, comments should have the same indent as code
        #
        # 1. class name you may retrieve from self.__class__.__name__
        # 2. public means 'public by name convention', so its name
        # is not started from '_'
        #
        custom_repr = ""
        custom_repr += "("
        #
        # Review: use dir(ob), because now will only iterate over instance
        # attrs only, but not class one.
        #
        for arg in self.__dict__.keys():
            if arg[0] != '_':
                custom_repr += arg
                custom_repr += "="
                #
                # Review: why not use getattr, but __dict__?
                #
                custom_repr += repr(self.__dict__[arg])
                custom_repr += ", "
        #
        # Review: ', '.join(<generator expression for iteration over attrs>)
        # will help you
        #
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
