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
"""Modules are dynamically loaded into an instantiated shell to add
additional functionality.

Modules can provide functionality in several ways:

- bind module methods to an instance of the shell. For example, a module might
  bind a "do_history" method to the shel.
- create and manage a data store private to the module
- register hooks with the shell
"""
# pylint: disable=no-self-use

import types

from ..models import Statement, Result
from ..utils import rebind_method

class DefaultResult:
    """Create a default result if a do_command() method doesn't return one"""
    def load(self, shell):
        """Load and iniitalize this module"""

        # bind our hook to the shell
        rebind_method(self._default_result_hook, shell)
        # register the hook we just added to the shell
        shell.register_postexecute_hook(shell._default_result_hook)

    #
    # rebound methods
    #
    # these methods end up bound to the shell, not to the module
    def _default_result_hook(
            self,
            _statement: Statement,
            result: Result,
    ) -> Result:
        """Generate a default result if one was not generated"""
        if not result:
            result = Result(exit_code=0, stop=False)
        return result


class ExitCommand:
    """Add an exit command to a shell"""
    def load(self, shell):
        """Load and initialize this module"""
        # bind the command method to the shell
        rebind_method(self.do_exit, shell)

    #
    # rebound methods
    #
    # these methods end up bound to the shell, not to the module
    def do_exit(self, _statement: Statement) -> Result:
        """Exit the shell"""
        return Result(exit_code=0, stop=True)


class History:
    """Add a history of entered commands"""
    def load(self, shell):
        """Load and initialize this module"""
        shell._history = []
        # bind the hist command to the shell
        rebind_method(self.do_hist, shell)
        # bind the hook method to the shell
        rebind_method(self._add_to_history, shell)
        shell.register_postparse_hook(shell._add_to_history)

    #
    # rebound methods
    #
    # these methods end up bound to the shell, not to the module
    def do_hist(self, statement: Statement) -> Result:
        """Show the history"""
        self.wout('\n'.join(self._history))
        return Result(exit_code=0, stop=False)

    def _add_to_history(self, statement: Statement) -> Statement:
        """postparsing hook to add the statement to history"""
        self._history.append(statement.raw)
        return statement
