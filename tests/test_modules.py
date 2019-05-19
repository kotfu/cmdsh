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
import pytest

import cmdsh

#
# DefaultResult module
#
class DefaultResultApp(cmdsh.Shell):
    """A simple app to rest the DefaultResult module"""

    def do_say(self, statement: cmdsh.Statement) -> cmdsh.Result:
        """Repeat back the arguments"""
        self.wout(' '.join(statement.arglist))
        # don't return anything here
        # we want to see if the module will do it for us


def test_no_result():
    drapp = DefaultResultApp()
    result = drapp.do('say hello')
    assert result is None


def test_default_result():
    drapp = DefaultResultApp()
    drmod = cmdsh.modules.DefaultResult()
    drapp.load_module(drmod)
    result = drapp.do('say hello')
    assert result
    assert result.exit_code == 0
    assert not result.stop


#
# ExitCommand module
#
def test_exit_command():
    app = cmdsh.Shell()
    with pytest.raises(cmdsh.CommandNotFound):
        result = app.do('exit')

    exit_command = cmdsh.modules.ExitCommand()
    app.load_module(exit_command)
    result = app.do('exit')
    assert result.exit_code == 0
    assert result.stop
