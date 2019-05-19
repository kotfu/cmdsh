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
"""A personality provides a container for all command shell classes and settings

It must provide the following methods and attributes:

parser - a parser as defined in parsers.py

"""

import types

from .parsers import SimpleParser


#
# bound methods
#
# def render_prompt(self) -> str:
#     """attempt to dynamically bind a method to the class"""
#     return '{}render: '.format(self.prompt)


class StandardLibraryPersonality:
    """Closely (but not perfectly) emulates the behavior of the standard library"""
    def __init__(self):
        self.parser = SimpleParser()

    def bind(self, shell):
        """The shell calls this method and passes itself in so that we can
        do any dynamic binding we want

        Any methods on this class that you bind to shell will have shell as
        self when they are called


        """

        # WARNING: dynamically binding in this way supercedes any methods
        # defined in the cmdsh.Shell() or any subclass thereof

        # to bind a bare function to the shell, use this incantation
        # shell.render_prompt = types.MethodType(render_prompt, shell)

        # this is the incantation that binds a method from an instance of
        # the personality to the instance of the shell
        # shell.render_prompt = types.MethodType(self.render_prompt.__func__, shell)

        # once the methods are bound to the shell, you can register them with any hooks

    #
    # bound methods
    #
    # these methods end up bound to the shell, not to the personality
    # they are mixed in dynamically by the bind() method, which the shell
    # calls on initialization

    # def render_prompt(self) -> str:
    #     """attempt to dynamically bind"""
    #     # pylint: disable=no-member
    #     return '{}'.format(self.prompt)
