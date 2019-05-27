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
# pylint: disable=too-many-instance-attributes

import inspect
import sys

from typing import Any, Callable, Optional

from . import utils
from .models import Statement, Result, Record, CommandNotFound
from .personalities import SimplePersonality


class Shell:
    """
    Instantiate or subclass Shell to create a new language shell

    Attributes:

    input_queue
        a list of input, as if it came from the user. The cmdloop pops items
        from this list before reading stdin parser the parser class to use
        to parse input into a Statement object

    prompt
        a static prompt to output before accepting user input

    Methods:

    eof()
        Called when the end of the input stream is reached.


    Methods and attributes on this class which don't start with an underscore are considered part of
    the public api of this class. Changes to these methods and attributes are reflected in the
    version number according to `Semantic Versioning <https://semver.org>`_.

    """

    def __init__(self, personality=SimplePersonality()):
        # initialize private variables
        self._preloop_hooks = []
        self._postloop_hooks = []
        self._postparse_hooks = []
        self._postexecute_hooks = []
        self._modules = {}

        # public attributes get sensible defaults
        self.input_queue = []
        self.history = []
        self.prompt = 'cmdsh: '

        # set and bind the personality
        self._personality = personality
        self._personality.bind(self)

    def loop(self) -> Result:
        """Get user input, parse it, and run the commands

        Returns the result of the last command
        """

        # run all the registered preloop hooks
        for func in self._preloop_hooks:
            func()

        # enter the command loop
        while True:
            if self.input_queue:
                # we have enqueued commands, use the first one
                line = self.input_queue.pop(0)
            else:
                try:
                    line = input(self.render_prompt())
                except EOFError:
                    result = self.eof()
                    if result.stop:
                        break
                    else:
                        continue

            if line == '':
                continue

            # Run the command along with all associated pre and post hooks
            try:
                result = self.do(line)
                if result.stop:
                    break
            except CommandNotFound as err:
                self.werr("{}: command not found\n".format(err.statement.command))

        # run all the registered postloop hooks
        for func in self._postloop_hooks:
            func()

        return result

    def do(self, line: str) -> Result:
        """Parse input and execute the statement, including all applicable hooks.

        Raises any exceptions thrown by hook methods or by the command function
        """
        # pylint: disable=invalid-name

        # for func in self._preparse_hooks:
        #     line = func(line)

        stmt = Statement(line)
        stmt = self._personality.parser.parse(stmt)
        for func in self._postparse_hooks:
            stmt = func(stmt)

        record = Record(statement=stmt)

        func = self._command_func(stmt.command)
        if func:
            result = func(stmt)

            for func in self._postexecute_hooks:
                result = func(stmt, result)

            self.history.append(record)

            return result
        raise CommandNotFound(stmt)

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
    # modules
    #
    def is_module_loaded(self, module: Any) -> bool:
        """Return true if a module has previously been loaded

        Since the shell processes modules that have been instantiated, we check for
        the name of the class of the passed module.
        """
        if inspect.isclass(module):
            klass = module
        else:
            klass = module.__class__
        return klass in self._modules.keys()

    def load_module(self, module: Any) -> None:
        """Load an instantiated module object

        If the module has already been loaded, it will not be loaded again
        """
        if inspect.isclass(module):
            module = module()
        if not self.is_module_loaded(module):
            module.load(self)
            self._modules[module.__class__] = module

    #
    # hooks
    #
    def register_preloop_hook(self, func: Callable[[None], None]) -> None:
        """Register a function to be called before the command loop starts."""
        utils.validate_callable_param_count(func, 0)
        utils.validate_callable_return(func, None)
        self._preloop_hooks.append(func)

    def register_postloop_hook(self, func: Callable[[None], None]) -> None:
        """Register a function to be called after the command loop finishes."""
        utils.validate_callable_param_count(func, 0)
        utils.validate_callable_return(func, None)
        self._postloop_hooks.append(func)

    def register_postparse_hook(self, func: Callable[[Statement], Statement]) -> None:
        """Register a method to be called after parsing input but before the command execution."""
        utils.validate_callable_param_count(func, 1)
        utils.validate_callable_argument(func, 1, Statement)
        utils.validate_callable_return(func, Statement)
        self._postparse_hooks.append(func)

    def register_postexecute_hook(self, func: Callable[[Statement, Result], Result]) -> None:
        """Register a function to be called after command execution completes."""
        utils.validate_callable_param_count(func, 2)
        utils.validate_callable_argument(func, 1, Statement)
        utils.validate_callable_argument(func, 2, Result)
        utils.validate_callable_return(func, Result)
        self._postexecute_hooks.append(func)

    #
    # output handling
    #
    def wout(self, data: str) -> None:
        """write data to stdout"""
        # pylint: disable=no-self-use
        sys.stdout.write(data)

    def werr(self, data: str) -> None:
        """write data to stderr"""
        # pylint: disable=no-self-use
        sys.stderr.write(data)

    def render_prompt(self) -> str:
        """Generate the prompt which is displayed before user input.

        Rather than access the prompt attribute directly, we call this method so that
        subclasses, modules, or personalities can over-ride it to create a dynamic prompt.
        """
        return self.prompt

    #
    # behaviors - a personality or module may over-ride these methods
    # to customize the behavior of the shell
    #
    def eof(self) -> Optional[Result]:
        """This method is called when and end of file is encountered.

        If you choose to over-ride this method, you need to consider behavior when
        input is a tty and when it is not. If you don't exit when input isn't a tty,
        the shell will hang when piped input runs out.
        """
        if sys.stdin.isatty():
            result = Result(exit_code=0, stop=False)
            self.wout('\n')
        else:
            result = Result(exit_code=0, stop=True)
        return result
