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
        self.called_postexecute = 0

    def do_say(self, statement: cmdsh.Statement) -> cmdsh.Result:
        """Repeat back the arguments"""
        self.wout(' '.join(statement.arglist))
        return cmdsh.Result()

    ###
    #
    # preloop and postloop hooks, some valid, some invalid
    # which share the same signature and are thus interchangable
    #
    ###
    def prepost_hook_one(self) -> None:
        """Method used for preloop or postloop hooks"""
        self.wout("one")

    def prepost_hook_two(self) -> None:
        """Another method used for preloop or postloop hooks"""
        self.wout("two")

    def prepost_hook_too_many_parameters(self, param) -> None:
        """A preloop or postloop hook with too many parameters"""

    def prepost_hook_wrong_return_annotation(self) -> bool:
        """A preloop or postloop hook with incorrect return type"""

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
            three: str,
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


###
#
# test preloop hooks
#
###
def test_preloop_hook(capsys):
    app = SayApp()
    app.register_preloop_hook(app.prepost_hook_one)
    app.cmdqueue.append('say hello')
    app.cmdqueue.append('exit')
    app.cmdloop()
    out, err = capsys.readouterr()
    assert out == 'one\nhello\n'
    assert not err


def test_preloop_hooks(capsys):
    app = SayApp()
    app.register_preloop_hook(app.prepost_hook_one)
    app.register_preloop_hook(app.prepost_hook_two)
    app.cmdqueue.append('say hello')
    app.cmdqueue.append('exit')
    app.cmdloop()
    out, err = capsys.readouterr()
    assert out == 'one\ntwo\nhello\n'
    assert not err


def test_register_preloop_hook_too_many_parameters():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_preloop_hook(app.prepost_hook_too_many_parameters)


def test_register_preloop_hook_wrong_return_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_preloop_hook(app.prepost_hook_wrong_return_annotation)


###
#
# test postloop hooks
#
###
def test_postloop_hook(capsys):
    app = SayApp()
    app.register_postloop_hook(app.prepost_hook_one)
    app.cmdqueue.append('say hello')
    app.cmdqueue.append('exit')
    app.cmdloop()
    out, err = capsys.readouterr()
    assert out == 'hello\none\n'
    assert not err


def test_postloop_hooks(capsys):
    app = SayApp()
    app.register_postloop_hook(app.prepost_hook_one)
    app.register_postloop_hook(app.prepost_hook_two)
    app.cmdqueue.append('say hello')
    app.cmdqueue.append('exit')
    app.cmdloop()
    out, err = capsys.readouterr()
    assert out == 'hello\none\ntwo\n'
    assert not err


def test_register_postloop_hook_too_many_parameters():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postloop_hook(app.prepost_hook_too_many_parameters)


def test_register_postloop_hook_wrong_return_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postloop_hook(app.prepost_hook_wrong_return_annotation)


###
#
# test post-execute hooks
#
###
def test_postexecute_hook(capsys):
    app = SayApp()
    app.register_postexecute_hook(app.postexecute_hook)
    app.do('say hello')
    out, err = capsys.readouterr()
    assert out == 'hello\n'
    assert not err
    assert app.called_postexecute == 1


def test_postexecute_hooks(capsys):
    app = SayApp()
    app.register_postexecute_hook(app.postexecute_hook)
    app.register_postexecute_hook(app.postexecute_hook)
    app.do('say hello')
    out, err = capsys.readouterr()
    assert out == 'hello\n'
    assert not err
    assert app.called_postexecute == 2


def test_register_postexecute_hook_not_enough_parameters():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_not_enough_parameters)


def test_register_postexecute_hook_too_many_parameters():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_too_many_parameters)


def test_register_postexecute_hook_no_parameter_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_no_parameter_annotation)


def test_register_postexecute_hook_partial_parameter_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_partial_parameter_annotation)


def test_register_postexecute_hook_wrong_parameter_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_wrong_parameter_annotation)


def test_register_postexecute_hook_no_return_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_no_return_annotation)


def test_register_postexecute_hook_wrong_return_annotation():
    app = SayApp()
    with pytest.raises(TypeError):
        app.register_postexecute_hook(app.postexecute_hook_wrong_return_annotation)


    # ###
    # #
    # # preparse hook
    # #
    # ###
    # def preparse(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:
    #     """Preparsing hook"""
    #     self.called_preparse += 1
    #     return data

    # ###
    # #
    # # Postparsing hooks
    # #
    # ###
    # def postparse_hook(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook"""
    #     self.called_postparsing += 1
    #     return data

    # def postparse_hook_stop(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook with requests application exit"""
    #     self.called_postparsing += 1
    #     data.stop = True
    #     return data

    # def postparse_hook_emptystatement(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook with raises an EmptyStatement exception"""
    #     self.called_postparsing += 1
    #     raise cmd2.EmptyStatement

    # def postparse_hook_exception(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook which raises an exception"""
    #     self.called_postparsing += 1
    #     raise ValueError

    # def postparse_hook_too_many_parameters(self, data1, data2) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook with too many parameters"""
    #     pass

    # def postparse_hook_undeclared_parameter_annotation(self, data) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook with an undeclared parameter type"""
    #     pass

    # def postparse_hook_wrong_parameter_annotation(self, data: str) -> cmd2.plugin.PostparsingData:
    #     """A postparsing hook with the wrong parameter type"""
    #     pass

    # def postparse_hook_undeclared_return_annotation(self, data: cmd2.plugin.PostparsingData):
    #     """A postparsing hook with an undeclared return type"""
    #     pass

    # def postparse_hook_wrong_return_annotation(self, data: cmd2.plugin.PostparsingData) -> str:
    #     """A postparsing hook with the wrong return type"""
    #     pass

    # ###
    # #
    # # precommand hooks, some valid, some invalid
    # #
    # ###
    # def precmd(self, statement: cmd2.Statement) -> cmd2.Statement:
    #     """Override cmd.Cmd method"""
    #     self.called_precmd += 1
    #     return statement

    # def precmd_hook(self, data: plugin.PrecommandData) -> plugin.PrecommandData:
    #     """A precommand hook"""
    #     self.called_precmd += 1
    #     return data

    # def precmd_hook_emptystatement(self, data: plugin.PrecommandData) -> plugin.PrecommandData:
    #     """A precommand hook which raises an EmptyStatement exception"""
    #     self.called_precmd += 1
    #     raise cmd2.EmptyStatement

    # def precmd_hook_exception(self, data: plugin.PrecommandData) -> plugin.PrecommandData:
    #     """A precommand hook which raises an exception"""
    #     self.called_precmd += 1
    #     raise ValueError

    # def precmd_hook_not_enough_parameters(self) -> plugin.PrecommandData:
    #     """A precommand hook with no parameters"""
    #     pass

    # def precmd_hook_too_many_parameters(self, one: plugin.PrecommandData, two: str) -> plugin.PrecommandData:
    #     """A precommand hook with too many parameters"""
    #     return one

    # def precmd_hook_no_parameter_annotation(self, data) -> plugin.PrecommandData:
    #     """A precommand hook with no type annotation on the parameter"""
    #     return data

    # def precmd_hook_wrong_parameter_annotation(self, data: str) -> plugin.PrecommandData:
    #     """A precommand hook with the incorrect type annotation on the parameter"""
    #     return data

    # def precmd_hook_no_return_annotation(self, data: plugin.PrecommandData):
    #     """A precommand hook with no type annotation on the return value"""
    #     return data

    # def precmd_hook_wrong_return_annotation(self, data: plugin.PrecommandData) -> cmd2.Statement:
    #     return self.statement_parser.parse('hi there')




    # ###
    # #
    # # command finalization hooks, some valid, some invalid
    # #
    # ###
    # def cmdfinalization_hook(self, data: plugin.CommandFinalizationData) -> plugin.CommandFinalizationData:
    #     """A command finalization hook."""
    #     self.called_cmdfinalization += 1
    #     return data

    # def cmdfinalization_hook_stop(self, data: cmd2.plugin.CommandFinalizationData) -> cmd2.plugin.CommandFinalizationData:
    #     """A postparsing hook which requests application exit"""
    #     self.called_cmdfinalization += 1
    #     data.stop = True
    #     return data

    # def cmdfinalization_hook_exception(self, data: cmd2.plugin.CommandFinalizationData) -> cmd2.plugin.CommandFinalizationData:
    #     """A postparsing hook which raises an exception"""
    #     self.called_cmdfinalization += 1
    #     raise ValueError

    # def cmdfinalization_hook_not_enough_parameters(self) -> plugin.CommandFinalizationData:
    #     """A command finalization hook with no parameters."""
    #     pass

    # def cmdfinalization_hook_too_many_parameters(self, one: plugin.CommandFinalizationData, two: str) -> plugin.CommandFinalizationData:
    #     """A command finalization hook with too many parameters."""
    #     return one

    # def cmdfinalization_hook_no_parameter_annotation(self, data) -> plugin.CommandFinalizationData:
    #     """A command finalization hook with no type annotation on the parameter."""
    #     return data

    # def cmdfinalization_hook_wrong_parameter_annotation(self, data: str) -> plugin.CommandFinalizationData:
    #     """A command finalization hook with the incorrect type annotation on the parameter."""
    #     return data

    # def cmdfinalization_hook_no_return_annotation(self, data: plugin.CommandFinalizationData):
    #     """A command finalizationhook with no type annotation on the return value."""
    #     return data

    # def cmdfinalization_hook_wrong_return_annotation(self, data: plugin.CommandFinalizationData) -> cmd2.Statement:
    #     """A command finalization hook with the wrong return type annotation."""
    #     return self.statement_parser.parse('hi there')


# class PluggedApp(Plugin, cmdsh.Shell):
#     """A sample app with a plugin mixed in"""
#     def do_say(self, statement):
#         """Repeat back the arguments"""
#         self.wout(' '.join(statement.arglist))
#         return cmdsh.Result()
