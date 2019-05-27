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
"""Parser classes to turn user input into Statement objects

You can use any class as a parser, as long is it implements the following methods:

parse(self, statement: Statement) -> Statement

The statement object passed into the parse method will only have the ``.raw``
attribute set. The parse method must parse that line and return a new statement
object with both ``.raw`` and ``.argv`` attributes set. ``.argv`` is a list
of arguments similar to ``sys.argv``.

Any exceptions thrown by the parse method prevent the shell from executing
the statement.
"""
# pylint: disable=no-self-use

import shlex

from .models import Statement


class SimpleParser:
    """A simple parser which break the input arguments by whitespace

    Quoted arguments are properly handled
    """
    # pylint: disable=too-few-public-methods
    def parse(self, stmt: Statement) -> Statement:
        """Split the input on whitespace"""
        stmt.argv = list(shlex.shlex(stmt.raw, posix=False))
        return stmt


class PosixShellParser:
    """Parse using POSIX shell rules

    - Quoted strings are properly handled, but
    - Quotes do not separate words
    - Escape sequences are interpreted
    - Everything after an unquoted/unescaped # is treated as a comment
    """
    # pylint: disable=too-few-public-methods
    def parse(self, stmt: Statement) -> Statement:
        """Posix split the input"""
        stmt.argv = list(shlex.shlex(stmt.raw, posix=True, punctuation_chars=True))
        return stmt
