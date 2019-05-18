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
from .personalities import StandardLibraryPersonality


class Shell:
    """
    Instantiate or subclass Shell to create a new language shell

    Attributes:

    cmdqueue a list of commands. The cmdloop pops items from this list before reading
        stdin parser the parser class to use to parse input into a Statement object

    Methods and attributes on this class which don't start with an underscore are
    considered part of the public api of this class. Changes to these methods and
    attributes are reflected in the version number according to `Semantic Versioning
    <https://semver.org>`_.

    """

    def __init__(self, personality=StandardLibraryPersonality()):
        # hooks
        self._preloop_hooks = []
        self._postloop_hooks = []
        # public attributes get sensible defaults
        self.cmdqueue = []
        self.personality = personality
        self.prompt = 'cmdsh: '

    def cmdloop(self) -> Result:
        """Get user input, parse it, and run the commands

        Returns the result of the last command
        """

        # set a default result in case we exit before generating an actual result
        result = Result(exit_code=0, stop=True)

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
                    line = input(self.render_prompt())
                except EOFError:
                    break

            if line == '':
                continue

            # Run the command along with all associated pre and post hooks
            try:
                result = self.execute(line)
                if result.stop:
                    break
            except CommandNotFound as err:
                self.werr("{}: command not found".format(err.statement.command))

        # run all the registered postloop hooks
        for func in self._postloop_hooks:
            func()

        return result

    def execute(self, line: str) -> Result:
        """Parse input and run the command, including all applicable hooks"""
        statement = self.personality.parser.parse(line)
        func = self._command_func(statement.command)
        if func:
            # run pre-execute hooks
            result = func(statement)
            # run post-execute hooks
            if not result:
                # they didn't return a result, so let's create the default one
                result = Result()
            return result

        raise CommandNotFound(statement)

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
    def wout(self, data: str) -> None:
        """write data to stdout"""
        sys.stdout.write('{}\n'.format(data))

    def werr(self, data: str) -> None:
        """write data to stderr"""
        sys.stderr.write('{}\n'.format(data))

    def render_prompt(self) -> str:
        """Generate the prompt which is displayed before user input.

        Rather than access the prompt attribute directly, we call this method so that
        subclasses can over-ride it to create a dynamic prompt.
        """
        return self.prompt

    #
    # built in commands
    #
    def do_exit(self, statement: Statement) -> Result:
        """Exit the shell"""
        return Result(exit_code=0, stop=True)
