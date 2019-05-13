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

import pytest

from cmdsh.models import CommandNotFound


INVALID_COMMAND = 'thisisnotacommand'


#
# tests
#
def test_command_func(shell):
    assert shell._command_func('exit')


def test_command_func_not_found(shell):
    assert not shell._command_func(INVALID_COMMAND)


def test_command_func_attribute(shell):
    # make sure we won't try and call an attribute
    # that happens to be named do_*
    shell.do_attribute = True
    assert not shell._command_func('attribute')


#
# test prompt
#
def test_default_prompt(shell):
    assert shell.render_prompt() == 'cmdsh: '


def test_custom_prompt(shell):
    prompt = 'static-prompt: '
    shell.prompt = prompt
    assert shell.render_prompt() == prompt


#
# test built-in commands and command loop related behavior
#
def test_mocked_input(shell, mocker):
    """test typed input by mocking up the input call"""
    mock_input = mocker.patch('builtins.input', return_value='exit')
    last_result = shell.cmdloop()
    assert last_result.stop
    assert last_result.exit_code == 0
    assert mock_input.call_count == 1


def test_mocked_input_eof(shell, mocker):
    """test EOF as typed input by mocking up the input call"""
    mock_input = mocker.patch('builtins.input')
    mock_input.side_effect = EOFError()
    last_result = shell.cmdloop()
    assert last_result.stop
    assert last_result.exit_code == 0
    assert mock_input.call_count == 1


def test_empty_input_no_output(shell, capsys):
    shell.cmdqueue.append('')
    shell.cmdqueue.append('exit')
    last_result = shell.cmdloop()
    out, err = capsys.readouterr()
    assert not out
    assert not err
    assert last_result.stop
    assert last_result.exit_code == 0


def test_command_no_returned_result(talker):
    # the say command in the talker app doesn't return a result
    # we want to make sure that cmdsh creates a default one
    result = talker.execute('say hello')
    assert result
    assert not result.stop
    assert result.exit_code == 0


def test_command_not_found_execute(shell):
    with pytest.raises(CommandNotFound):
        shell.execute(INVALID_COMMAND)


def test_command_not_found_errmsg(shell, capsys):
    shell.cmdqueue.append(INVALID_COMMAND)
    shell.cmdqueue.append('exit')
    shell.cmdloop()
    out, err = capsys.readouterr()
    assert 'command not found' in err


def test_exit(shell):
    result = shell.execute('exit')
    assert result.stop
    assert result.exit_code == 0
