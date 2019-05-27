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


class SayApp(cmdsh.Shell):
    """A simple app with lots of hooks"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_counters()

    def reset_counters(self):
        """Set hook call counters to zero"""
        self.called_postparse = 0
        self.called_postexecute = 0

    def do_say(self, statement: cmdsh.Statement) -> cmdsh.Result:
        """Repeat back the arguments"""
        self.wout('{}\n'.format(' '.join(statement.arglist)))
        return cmdsh.Result()

    ###
    #
    # preloop and postloop hooks, some valid, some invalid
    # which share the same signature and are thus interchangable
    #
    ###
    def prepost_hook_one(self) -> None:
        """Method used for preloop or postloop hooks"""
        self.wout("one\n")

    def prepost_hook_two(self) -> None:
        """Another method used for preloop or postloop hooks"""
        self.wout("two\n")

    def prepost_hook_too_many_parameters(self, param) -> None:
        """A preloop or postloop hook with too many parameters"""

    def prepost_hook_wrong_return_annotation(self) -> bool:
        """A preloop or postloop hook with incorrect return type"""

    def prepost_hook_no_return_annotation(self):
        """A preloop or postloop hook with no return type annotation"""

    ###
    #
    # post-parse hooks, some valid, some invalid
    #
    ###
    def postparse_hook(self, statement: cmdsh.Statement) -> cmdsh.Statement:
        """A post parse hook"""
        self.called_postparse += 1
        return statement

    def postparse_hook_exception(self, statement: cmdsh.Statement) -> cmdsh.Statement:
        """A postparsing hook which raises an exception"""
        # pylint: disable=unused-argument
        self.called_postparse += 1
        raise ValueError

    def postparse_hook_not_enough_parameters(self) -> cmdsh.Statement:
        """A postparsing hook with no parameters"""

    def postparse_hook_too_many_parameters(
            self,
            statement: cmdsh.Statement,
            three: str,
    ) -> cmdsh.Statement:
        """A postparse hook with too many parameters"""
        # pylint: disable=unused-argument

    def postparse_hook_no_parameter_annotation(self, statement) -> cmdsh.Statement:
        """A postparse hook with no parameter annotation"""
        # pylint: disable=unused-argument

    def postparse_hook_wrong_parameter_annotation(self, statement: str) -> cmdsh.Statement:
        """A postparse hook with incorrect parameter annotation"""
        # pylint: disable=unused-argument

    def postparse_hook_wrong_return_annotation(self, statement: cmdsh.Statement) -> str:
        """A postparse hook with incorrect return annotation"""
        # pylint: disable=unused-argument

    def postparse_hook_no_return_annotation(self, statement: cmdsh.Statement):
        """A postparse hook with no return annotation"""
        # pylint: disable=unused-argument

    ###
    #
    # post-execute hooks, some valid, some invalid
    #
    ###
    def postexecute_hook(self, statement: cmdsh.Statement, result: cmdsh.Result) -> cmdsh.Result:
        """A post-execute hook"""
        # pylint: disable=unused-argument
        self.called_postexecute += 1
        return result

    def postexecute_hook_exception(
            self,
            statement: cmdsh.Statement,
            result: cmdsh.Result,
    ) -> cmdsh.Result:
        """A post-execute hook which raises an exception"""
        # pylint: disable=unused-argument
        self.called_postexecute += 1
        raise ZeroDivisionError

    def postexecute_hook_not_enough_parameters(self) -> cmdsh.Result:
        """A post-execute hook with no parameters"""

    def postexecute_hook_too_many_parameters(
            self,
            statement: cmdsh.Statement,
            result: cmdsh.Result(),
            four: str,
    ) -> cmdsh.Result:
        """A post-execute hook with too many parameters"""
        # pylint: disable=unused-argument
        return result

    def postexecute_hook_no_parameter_annotation(self, statement, result) -> cmdsh.Result:
        """A post-execute hook with no type annotation on the parameter"""
        # pylint: disable=unused-argument
        return result

    def postexecute_hook_partial_parameter_annotation(
            self,
            statement: cmdsh.Statement,
            result,
    ) -> cmdsh.Result:
        """A post-execute hook with partial parameter annotation"""
        # pylint: disable=unused-argument
        return result

    def postexecute_hook_wrong_parameter_annotation(
            self,
            statement: str,
            result: str
    ) -> cmdsh.Result:
        """A post-execute hook with the incorrect type annotation on the parameter"""
        # pylint: disable=unused-argument
        return result

    def postexecute_hook_no_return_annotation(
            self,
            statement: cmdsh.Statement,
            result: cmdsh.Result,
    ):
        """A post-execute hook with no type annotation on the return value"""
        # pylint: disable=unused-argument
        return result

    def postexecute_hook_wrong_return_annotation(
            self,
            statement: cmdsh.Statement,
            result: cmdsh.Result,
    ) -> cmdsh.Statement:
        """A post-execute hook with the wrong return annotation"""
        # pylint: disable=unused-argument
        return statement


@pytest.fixture
def sayapp():
    app = SayApp()
    exit_command = cmdsh.modules.ExitCommand()
    app.load_module(exit_command)
    return app


###
#
# test preloop hooks
#
###
def test_preloop_hook(sayapp, capsys):
    sayapp.register_preloop_hook(sayapp.prepost_hook_one)
    sayapp.input_queue.append('say hello')
    sayapp.input_queue.append('exit')
    sayapp.loop()
    out, err = capsys.readouterr()
    assert out == 'one\nhello\n'
    assert not err


def test_preloop_hooks(sayapp, capsys):
    sayapp.register_preloop_hook(sayapp.prepost_hook_one)
    sayapp.register_preloop_hook(sayapp.prepost_hook_two)
    sayapp.input_queue.append('say hello')
    sayapp.input_queue.append('exit')
    sayapp.loop()
    out, err = capsys.readouterr()
    assert out == 'one\ntwo\nhello\n'
    assert not err


def test_preloop_hook_too_many_parameters(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_preloop_hook(sayapp.prepost_hook_too_many_parameters)


def test_preloop_hook_wrong_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_preloop_hook(sayapp.prepost_hook_wrong_return_annotation)


def test_preloop_hook_no_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_preloop_hook(sayapp.prepost_hook_no_return_annotation)


###
#
# test postloop hooks
#
###
def test_postloop_hook(sayapp, capsys):
    sayapp.register_postloop_hook(sayapp.prepost_hook_one)
    sayapp.input_queue.append('say hello')
    sayapp.input_queue.append('exit')
    sayapp.loop()
    out, err = capsys.readouterr()
    assert out == 'hello\none\n'
    assert not err


def test_postloop_hooks(sayapp, capsys):
    sayapp.register_postloop_hook(sayapp.prepost_hook_one)
    sayapp.register_postloop_hook(sayapp.prepost_hook_two)
    sayapp.input_queue.append('say hello')
    sayapp.input_queue.append('exit')
    sayapp.loop()
    out, err = capsys.readouterr()
    assert out == 'hello\none\ntwo\n'
    assert not err


def test_postloop_hook_too_many_parameters(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postloop_hook(sayapp.prepost_hook_too_many_parameters)


def test_postloop_hook_wrong_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postloop_hook(sayapp.prepost_hook_wrong_return_annotation)


def test_postloop_hook_no_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postloop_hook(sayapp.prepost_hook_no_return_annotation)


###
#
# test post-parse hooks
#
###
def test_postparse_hook(sayapp, capsys):
    sayapp.register_postparse_hook(sayapp.postparse_hook)
    sayapp.do('say hello')
    out, err = capsys.readouterr()
    assert out == 'hello\n'
    assert not err
    assert sayapp.called_postparse == 1


def test_postparse_hooks(sayapp, capsys):
    sayapp.register_postparse_hook(sayapp.postparse_hook)
    sayapp.register_postparse_hook(sayapp.postparse_hook)
    sayapp.do('say hello')
    out, err = capsys.readouterr()
    assert out == 'hello\n'
    assert not err
    assert sayapp.called_postparse == 2


def test_postparse_hook_exception(sayapp, capsys):
    sayapp.register_postparse_hook(sayapp.postparse_hook_exception)
    sayapp.register_postparse_hook(sayapp.postparse_hook)
    with pytest.raises(ValueError):
        sayapp.do('say hello')
    # the first hook should throw an exception, and the second hook should
    # not be called, nor should there be any output
    out, err = capsys.readouterr()
    assert not out
    assert not err
    assert sayapp.called_postparse == 1


def test_postparse_hook_not_enough_parameters(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postparse_hook(sayapp.postparse_hook_not_enough_parameters)


def test_postparse_hook_too_many_parameters(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postparse_hook(sayapp.postparse_hook_too_many_parameters)


def test_postparse_hook_no_parameter_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postparse_hook(sayapp.postparse_hook_no_parameter_annotation)


def test_postparse_hook_wrong_parameter_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postparse_hook(sayapp.postparse_hook_wrong_parameter_annotation)


def test_postparse_hook_no_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postparse_hook(sayapp.postparse_hook_no_return_annotation)


def test_postparse_hook_wrong_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postparse_hook(sayapp.postparse_hook_wrong_return_annotation)


###
#
# test post-execute hooks
#
###
def test_postexecute_hook(sayapp, capsys):
    sayapp.register_postexecute_hook(sayapp.postexecute_hook)
    sayapp.do('say hello')
    out, err = capsys.readouterr()
    assert out == 'hello\n'
    assert not err
    assert sayapp.called_postexecute == 1


def test_postexecute_hooks(sayapp, capsys):
    sayapp.register_postexecute_hook(sayapp.postexecute_hook)
    sayapp.register_postexecute_hook(sayapp.postexecute_hook)
    sayapp.do('say hello')
    out, err = capsys.readouterr()
    assert out == 'hello\n'
    assert not err
    assert sayapp.called_postexecute == 2


def test_register_postexecute_hook_not_enough_parameters(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_not_enough_parameters)


def test_register_postexecute_hook_too_many_parameters(sayapp):
    sayapp = SayApp()
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_too_many_parameters)


def test_register_postexecute_hook_no_parameter_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_no_parameter_annotation)


def test_register_postexecute_hook_partial_parameter_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_partial_parameter_annotation)


def test_register_postexecute_hook_wrong_parameter_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_wrong_parameter_annotation)


def test_register_postexecute_hook_no_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_no_return_annotation)


def test_register_postexecute_hook_wrong_return_annotation(sayapp):
    with pytest.raises(TypeError):
        sayapp.register_postexecute_hook(sayapp.postexecute_hook_wrong_return_annotation)
