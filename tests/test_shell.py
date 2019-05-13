#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 Jared Crapo
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
from cmdsh.models import CommandNotFound


INVALID_COMMAND = 'thisisnotacommand'

#
# fixtures
#
@pytest.fixture
def shell():
    return cmdsh.Shell()

#
# tests
#
def test_command_func(shell):
    assert shell._command_func('exit')

def test_command_func_not_found(shell):
    assert not shell._command_func(INVALID_COMMAND)

def test_command_func_attribute(shell):
    shell.do_attribute = True
    assert not shell._command_func('attribute')

#
# test the loop
#
def test_cmdqueue():
    # TODO
    pass

#
# test built-in commands and behavior
#
def test_empty_input_no_output(shell, capsys):
    shell.cmdqueue.append('')
    shell.cmdqueue.append('exit')
    shell.cmdloop()
    out, err = capsys.readouterr()
    assert not out
    assert not err

def test_command_not_found_execute(shell):
    with pytest.raises(CommandNotFound):
        result = shell.execute(INVALID_COMMAND)

def test_command_not_found_errmsg(shell, capsys):
    shell.cmdqueue.append(INVALID_COMMAND)
    shell.cmdqueue.append('exit')
    shell.cmdloop()
    out, err = capsys.readouterr()
    assert 'command not found' in err

def test_exit(shell):
    result = shell.execute('exit')
    assert result.stop
