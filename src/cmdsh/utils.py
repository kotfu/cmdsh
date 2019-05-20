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


def validate_callable_argument(func, argnum, typ):
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


def validate_callable_return(func, typ):
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
