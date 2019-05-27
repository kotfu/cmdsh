****************
The Command Loop
****************

The core of any ``cmdsh`` based application is the command loop. You enter the
command loop by::

    import cmdsh
    shell = cmdsh.Shell()
    last_result = shell.loop()

The shell then repeatedly reads a statement, parses the input, executes a command, and
displays any output. This continues until some command requests the loop terminate.


Preloop Hooks
=============

Before the command loop begins, the shell calls every registered preloop hooks. To
register a preloop hook::

    >>> import cmdsh
    >>> class App(cmdsh.Shell):
    ...     def __init__(self, *args, **kwargs):
    ...         super().__init__(*args, **kwargs)
    ...         self.register_preloop_hook(self.myhookmethod)
    ...
    ...     def myhookmethod(self):
    ...         self.wout("before the loop begins")


loop()
======

Here's the specific steps that occur each time through the command loop:

#. Output the prompt
#. Read input
#. Call ``parse()``
#. Call ``do()``
#. Call ``do_command`` method
#. Call all registered post-execute hooks


do()
----

The ``do()`` method takes a string parameter, and performs the following functions:

  - parse the string into a statement
  - execute the statement
  - keeps a historical record of the parsing and execution


parse()
^^^^^^^

The ``parse()`` method turns a string of input into a ``Statement`` object

First, the raw input is passed through any InputFilters that have been registered. InputFilters take
a string and return a string. Any exceptions thrown prevent any further parsing actions.

Second, the raw string and the filtered string are added to a ``Statement`` object, which is passed
to the ``parse()`` method of the parser class assigned to the shell personality. The ``parse()``
method returns a more robust statement object with at least an ``argv`` list of arguments.

Third, the shell calls each registered postparse hook, passing the statement. The hook method can
modify the statement if desired, or return it as passed. Raising any exception causes the statement
to not be executed, and any subsequent post parse hooks will not be called.


execute()
^^^^^^^^^

The ``do()`` method is responsible for executing a Statement


Postloop Hooks
==============

Once the command loop terminates, the shell calls every registered postloop hook. Here's
an example of a postloop hook::

    >>> import cmdsh
    >>> class App(cmdsh.Shell):
    ...     def __init__(self, *args, **kwargs):
    ...         super().__init__(*args, **kwargs)
    ...         self.register_postloop_hook(self.myhookmethod)
    ...
    ...     def myhookmethod(self):
    ...         self.wout("before the loop begins")
