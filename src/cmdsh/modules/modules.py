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
"""

import types

import cmdsh


class DefaultResult:
    """Create a default result if a do_command() method doesn't return one"""
    allow_multiple_loads = False

    def load(self, shell):
        """Load and iniitalize this module"""

        # this is the incantation that binds a method from an instance of
        # the module to an instance of the shell
        shell._default_result_hook = types.MethodType(self._default_result_hook.__func__, shell)
        shell.register_postexecute_hook(shell._default_result_hook)

    #
    # bound methods
    #
    # these methods end up bound to the shell, not to the module
    def _default_result_hook(
            self,
            statement: cmdsh.Statement,
            result: cmdsh.Result,
    ) -> cmdsh.Result:
        """Generate a default result if one was not generated"""
        if not result:
            result = cmdsh.Result(exit_code=0, stop=False)
        return result
