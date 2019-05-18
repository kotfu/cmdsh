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

import types

import cmdsh


class Personality():
    def __init__(self):
        self.parser = cmdsh.parsers.SimpleParser()

    def bind(self, shell):
        """bind methods to the shell"""
        shell.render_prompt = types.MethodType(self.render_prompt.__func__, shell)

    # bound methods
    def render_prompt(self) -> str:
        """attempt to dynamically bind"""
        # pylint: disable=no-member
        return '{}render: '.format(self.prompt)


def test_bind():
    flavor = Personality()
    shell = cmdsh.Shell(personality=flavor)
    shell.prompt = 'hi:'
    assert shell.render_prompt() == 'hi:render: '
