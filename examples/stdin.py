#
# -*- coding: utf-8 -*-
"""an example that shows how your shell can read commands piped from standard input

try this out by

$ echo "say hello there" | python stdin.py
"""

import sys

import cmdsh


class Shell(cmdsh.Shell):
    """A simple command shell with a single command"""
    def __init__(self):
        super().__init__()
        self.prompt = 'stdin-example: '

    def do_say(self, statement):
        """output the given arguments"""
        self.wout(' '.join(statement.arglist))
        return cmdsh.Result()


def main():
    """instantiate and launch the application"""
    shell = Shell()
    last_result = shell.loop()
    return last_result.exit_code


if __name__ == "__main__":
    sys.exit(main())
