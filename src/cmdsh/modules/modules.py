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

A module can be any object that has a ``load(self, shell)`` method.
When you request the shell to load some object as a module, it calls the load
method on that object.

Module Writing Conventions
--------------------------

- When adding attributes to the shell, prefix them with an underscore and the
  name of your module. This is bad:

      shell.histfile = []

  This is good:

      shell._history_file


- Use the bind_attribute() function to hook the attribute to the shell, it has
  the benefit of raising an exception if the attribute already exists. This
  prevents collisions between modules who want to use the same attribute naame


- When defining methods which will be bound to the shell to be registered as
  hooks, prefix them with an underscore and the name of your module. This is
  bad:

      def result_hook():

  This is good:

      def _default_result_hook():

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
    # that means `self` references the shell object, not the module
    # object
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
    # that means `self` references the shell object, not the module
    # object
    def do_exit(self, _statement: Statement) -> Result:
        """Exit the shell"""
        return Result(exit_code=0, stop=True)


class History:
    """Add a history of entered commands"""
    def __init__(self, file="history.txt"):
        self._history_file = file

    def load(self, shell):
        """Load and initialize this module"""
        shell._history = []
        shell._history_file = self._history_file

        # bind the hist command to the shell
        rebind_method(self.do_hist, shell)
        # bind the hook method to the shell
        rebind_method(self._add_to_history, shell)
        shell.register_postparse_hook(shell._add_to_history)

    #
    # rebound methods
    #
    # these methods end up bound to the shell, not to the module
    # that means `self` references the shell object, not the module
    # object
    def do_hist(self, statement: Statement) -> Result:
        """Show the history"""
        self.wout('\n'.join(self._history))
        return Result(exit_code=0, stop=False)

    def _add_to_history(self, statement: Statement) -> Statement:
        """postparsing hook to add the statement to history"""
        self._history.append(statement.raw)
        return statement
