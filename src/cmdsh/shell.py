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
cmdsh
-----

A python library for creating interactive language shells.
"""
import inspect
import sys

from typing import Callable, Optional

from .models import Statement, Result, CommandNotFound
from .parsers import SimpleParser


# Ideas to consider:
#
#   - prompt class - count commands, allow variable interpolation
#

class Shell:
    """
    Instantiate or subclass Shell to create a new language shell

    Attributes:

    cmdqueue
        a list of commands. The cmdloop pops items from this list before reading stdin
    parser
        the parser class to use to parse input into a Statement object
    """

    def __init__(self):
        # hooks
        self._preloop_hooks = []
        self._postloop_hooks = []
        # public attributes get sensible defaults
        self.cmdqueue = []
        self.parser = SimpleParser()

    def cmdloop(self) -> None:
        """Get user input, parse it, and run the commands"""

        # run all the registered preloop hooks
        for func in self._preloop_hooks:
            func()

        # enter the command loop
        while True:
            if self.cmdqueue:
                # we have enqueued commands, use the first one
                line = self.cmdqueue.pop(0)
            else:
                try:
                    line = input("cmdsh: ")
                except EOFError:
                    break

            if line == '':
                continue

            # Run the command along with all associated pre and post hooks
            try:
                result = self.execute(line)
                if result.stop:
                    break
            except CommandNotFound:
                self.poutput("command not found")

        # run all the registered postloop hooks
        for func in self._postloop_hooks:
            func()

    def execute(self, line: str) -> Result:
        """Parse input and run the command, including all applicable hooks"""

        statement = self.parser.parse(line)

        func = self._command_func(statement.command)
        if func:
            # run pre-execute hooks
            result = func(statement)
            # run post-execute hooks
            return result

        raise CommandNotFound(line)

    def _command_func(self, command: str) -> Optional[Callable]:
        """Find the function to call for a given command"""
        func_name = 'do_' + command
        func = None
        try:
            func = getattr(self, func_name)
            if not callable(func):
                func = None
        except AttributeError:
            pass
        return func

    #
    # hooks
    #
    @classmethod
    def _validate_callable_param_count(cls, func: Callable, count: int) -> None:
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

    @classmethod
    def _validate_prepostloop_callable(cls, func: Callable[[None], None]) -> None:
        """Check parameter and return types for preloop and postloop hooks."""
        cls._validate_callable_param_count(func, 0)
        # make sure there is no return notation
        signature = inspect.signature(func)
        if signature.return_annotation is not None:
            raise TypeError("{} must declare return a return type of 'None'".format(
                func.__name__,
            ))

    def register_preloop_hook(self, func: Callable[[None], None]) -> None:
        """Register a function to be called before the command loop starts."""
        self._validate_prepostloop_callable(func)
        self._preloop_hooks.append(func)

    def register_postloop_hook(self, func: Callable[[None], None]) -> None:
        """Register a function to be called after the command loop finishes."""
        self._validate_prepostloop_callable(func)
        self._postloop_hooks.append(func)

    #
    # output handling
    #
    def poutput(self, output: str):
        """Print output"""
        sys.stdout.write('{}\n'.format(output))

    #
    # built in commands
    #
    def do_exit(self, statement: Statement) -> Result:
        """Exit the shell"""
        result = Result(stop=True)
        return result
