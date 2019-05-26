#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Jared Crapo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
Utility functions (not classes)
"""
import inspect
import types

from typing import Callable


def validate_callable_param_count(func: Callable, count: int) -> None:
    """Ensure a function has the given number of parameters."""
    signature = inspect.signature(func)
    # validate that the callable has the right number of parameters
    nparam = len(signature.parameters)
    if nparam != count:
        raise TypeError('{} has {} positional arguments, expected {}'.format(
            func.__name__,
            nparam,
            count,
        ))


def validate_callable_argument(func, argnum, typ) -> None:
    """Validate that a certain argument of func is annotated for a specific type"""
    signature = inspect.signature(func)
    paramname = list(signature.parameters.keys())[argnum-1]
    param = signature.parameters[paramname]
    if param.annotation != typ:
        raise TypeError('argument {} of {} has incompatible type {}, expected {}'.format(
            argnum,
            func.__name__,
            param.annotation,
            typ.__name__,
        ))


def validate_callable_return(func, typ) -> None:
    """Validate that func is annotated to return a specific type"""
    signature = inspect.signature(func)
    if typ:
        typname = typ.__name__
    else:
        typname = 'None'
    if signature.return_annotation != typ:
        raise TypeError("{} must declare return a return type of '{}'".format(
            func.__name__,
            typname,
        ))


def rebind_method(method, obj) -> None:
    """Rebind method from one object to another

    Call it something like this:

        rebind_method(obj1, obj2.do_command)

    This rebinds the ``do_command`` method from obj2 to obj1. Meaning
    after this function call you can:

        obj1.do_command()

    This works only on instantiated objects, not on classes.
    """
    #
    # this is dark python magic
    #
    # if we were doing this in a hardcoded way, we might do:
    #
    #     obj.method_name = types.MethodType(self.method_name.__func__, obj)
    #
    # TODO add force keyword parameter which defaults to false. If false, raise an
    # exception if the method already exists on obj
    method_name = method.__name__
    setattr(obj, method_name, types.MethodType(method.__func__, obj))


def bind_function(func, obj) -> None:
    """Bind a function to an object

    You must define func with a ``self`` parameter, which is gonna look wierd:

        def myfunc(self, param):
            return param

        shell = cmdsh.Shell()
        utils.bind_function(myfunc, shell)

    You can use this function to bind a function to a class, so that all future
    objects of that class have the method:

        cmdsh.utils.bind_function(cmdsh.parsers.SimpleParser.parse, cmdsh.Shell)

    """
    #
    # this is dark python magic
    #
    # if we were doing this in a hardcoded way, we would:
    #
    #     obj.method_name = types.Methodtype(func, obj)
    #
    func_name = func.__name__
    setattr(obj, func_name, types.MethodType(func, obj))


# TODO write bind_attribute()
