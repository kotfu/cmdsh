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
import sys

from typing import Callable, Optional

from .models import Statement, Result, CommandNotFound
from .parsers import SimpleParser


# Ideas to consider:
#
#   - command queue, get input pops from the queue if there is anything present
#   - prompt class - count commands, allow variable interpolation
#

class Shell:
    """
    Instantiate or subclass CmdSh to create a new language shell
    """

    def __init__(self):
        self.parser = SimpleParser()

    def loop(self) -> None:
        """Get user input, parse it, and run the commands"""

        # preloop - call registered preloop functions

        while True:
            try:
                line = input("cmdsh: ")
            except EOFError:
                break

            if line == '':
                continue

            # Run the command along with all associated pre and post hooks
            try:
                # run pre-execute hooks
                result = self.execute(line)
                # run post-execute hooks
                if result.stop:
                    break
            except CommandNotFound:
                self.poutput("command not found")

        # postloop - call registered postloop functions

    def execute(self, line: str) -> Result:
        """Parse input and run the command, including all applicable hooks"""

        statement = self.parser.parse(line)

        func = self._command_func(statement.command)
        if func:
            result = func(statement)
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
