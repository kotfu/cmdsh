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
"""Classes with essentially no functionality, they are data containers."""

from typing import List

import attr


class CommandNotFound(Exception):
    """Raised when the user inputs a command which is not valid"""

@attr.s(frozen=True)
class Statement():
    """The result of parsing user input

    Instances of this class are created by ``StatementParser.parse()`` methods. These
    instances should not be modified after parsing, so we use ``attr`` to freeze them.

    Here's some suggestions and best practices for how to use the attributes of this
    object:

    argv - this is a list of arguments in the style of ``sys.argv``. The first element of
           the list is the command. Subsequent elements of the list contain any additional
           arguments, with quotes removed, just like bash would. This is very useful if
           you are going to use ``argparse.parse_args()``:
           ```
           def do_mycommand(stmt):
               mycommand_argparser.parse_args(stmt.argv)
               ...
            ```

    command - the name of the command, same as ``statement.argv[0]``

    arglist - the arguments to the command, same as ``statement.argv[1:]``

    raw - if you want full access to exactly what the user typed at the input prompt you
          can get it, but you'll have to parse it on your own
    """

    # string containing exactly what was input by the user
    raw = attr.ib(default='', validator=attr.validators.instance_of(str))

    # the list of arguments in the user input
    argv = attr.ib(default=[], validator=attr.validators.instance_of(list))

    @property
    def command(self) -> str:
        """The name of the command."""
        cmd = ''
        if self.argv:
            cmd = self.argv[0]
        return cmd

    @property
    def arglist(self) -> List:
        """The list of arguments to the command."""
        return self.argv[1:]


@attr.s(frozen=True)
class Result():
    """The result of running a command"""
    stop = attr.ib(default=False, validator=attr.validators.instance_of(bool))
