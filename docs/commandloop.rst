The Command Loop
================

The core of any ``cmdsh`` based application is the command loop. You enter the
command loop by::

>>> import cmdsh
>>> shell = cmdsh.Shell()
>>> last_result = shell.cmdloop()

The shell then repeatedly reads a statement, parses the input, executes a command, and
displays any output. This continues until some command requests the loop terminate.


Preloop Hooks
-------------

Before the command loop begins, the shell calls every registered preloop hooks. To
register a preloop hook::

    class App(cmdsh.Shell):
        def __init__(self, *args, *kwargs):
            super().__init__(*args, **kwargs)
            self.register_preloop_hook(self.myhookmethod)

        def myhookmethod(self):
            self.wout("before the loop begins")


Command Loop Details
--------------------

Here's the specific steps that occur in the command loop:

#. Output the prompt
#. Read input
#. Parse input into a ``Statement`` object
#. Call ``do_command`` method


Postloop Hooks
--------------

Once the command loop terminates, the shell calls every registered postloop hook. Here's
an example of a postloop hook::

    class App(cmdsh.Shell):
        def __init__(self, *args, *kwargs):
            super().__init__(*args, **kwargs)
            self.register_postloop_hook(self.myhookmethod)

        def myhookmethod(self):
            self.wout("before the loop begins")
