#
# -*- coding: utf-8 -*-
"""An example of a command shell with dynamically generated prompt"""

import datetime
import sys

import cmdsh


class App(cmdsh.Shell):
    """A simple command shell with a dynamically generated prompt"""
    def __init__(self):
        # cmdsh.Shell initialization
        super().__init__()
        # if you only want a static prompt, set this attribute
        # and you are good to go
        self.prompt = 'static-prompt: '

    def render_prompt(self) -> str:
        """Create a dynamic prompt that shows the time"""
        now = datetime.datetime.now()
        return now.strftime('%H:%M> ')

    def do_echo(self, statement: cmdsh.Statement) -> cmdsh.Result:
        """output the given arguments"""
        self.wout(' '.join(statement.arglist))
        return cmdsh.Result()


def main():
    """instantiate and launch the application"""
    app = App()
    last_result = app.loop()
    return last_result.exit_code


if __name__ == "__main__":
    sys.exit(main())
