Contributing
============

Get Source Code
---------------

Clone the repo from github::

   $ git clone git@github.com:kotfu/cmdsh.git


Create Python Environments
--------------------------

cmdsh uses `tox <https://tox.readthedocs.io/en/latest/>`_ to run the test suite against
multiple python versions. I recommend using `pyenv <https://github.com/pyenv/pyenv>`_ with
the `pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`_ plugin to manage these
various versions. If you are a Windows user, ``pyenv`` won't work for you, you'll probably
have to use `conda <https://conda.io/>`_.

This distribution includes a shell script ``build-pyenvs.sh`` which automates the creation
of these environments.

If you prefer to create these virtual envs by hand, do the following::

   $ cd cmdsh
   $ pyenv install 3.7.3
   $ pyenv virtualenv -p python3.7 3.7.3 cmdsh-3.7
   $ pyenv install 3.6.8
   $ pyenv virtualenv -p python3.6 3.6.8 cmdsh-3.6
   $ pyenv install 3.5.7
   $ pyenv virtualenv -p python3.5 3.5.7 cmdsh-3.5

Now set pyenv to make all three of those available at the same time::

   $ pyenv local cmdsh-3.7 cmdsh-3.6 cmdsh-3.5

Whether you ran the script, or did it by hand, you now have isolated virtualenvs for each
of the minor python versions.


Install Dependencies
--------------------

Now install all the development dependencies::

   $ pip install -e .[dev]

This installs the cmdsh package "in-place", so the package points to the source code
instead of copying files to the python ``site-packages`` folder.

All the dependencies now have been installed in the ``cmdsh-3.7`` virtualenv. If you want
to work in other virtualenvs, you'll need to manually select it, and install again::

   $ pyenv shell cmdsh-3.5
   $ pip install -e .[dev]


Branches, Tags, and Versions
----------------------------

This project uses a simplified version of the `git flow branching
strategy <http://nvie.com/posts/a-successful-git-branching-model/>`_. We
don't use release branches, and we generally don't do hotfixes, so we
don't have any of those branches either. The master branch always
contains the latest release of the code uploaded to PyPI, with a tag for
the version number of that release.

The develop branch is where all the action occurs. Feature branches are
welcome. When it's time for a release, we merge develop into master.

This project uses `semantic versioning <https://semver.org/>`_.


Invoking Common Development Tasks
---------------------------------

This project uses many other python modules for various development tasks,
including testing, rendering documentation, and building and distributing
releases. These modules can be configured many different ways, which can
make it difficult to learn the specific incantations required for each
project you are familiar with.

This project uses `invoke <http://www.pyinvoke.org>`_ to provide a clean,
high level interface for these development tasks. To see the full list of
functions available::

   $ invoke -l

You can run multiple tasks in a single invocation, for example::

   $ invoke clean docs sdist wheel

That one command will remove all superflous cache, testing, and build
files, render the documentation, and build a source distribution and a
wheel distribution.

You probably won't need to read further in this document unless you
want more information about the specific tools used.


Testing
-------

You can run the tests against all the supported versions of python using ``tox``::

   $ tox

``tox`` expects that when it runs ``python3.5`` it will actually get a python from
the 3.5.x series. That's why we set up the various python environments earlier.

If you just want to run the tests in your current python environment, use
pytest::

   $ pytest

This runs all the test in ``tests/`` and also runs doctests in ``cmdsh/`` and ``docs/``.

You can speed up the test suite by using ``pytest-xdist`` to parallelize the tests across
the number of cores you have::

   $ pip install pytest-xdist
   $ pytest -n8


Code Quality
------------

Use ``pylint`` and ``flake8`` to check code quality. There is a pylint config file for the
tests and for the main module::

   $ pylint --rcfile=tests/pylintrc tests
   $ pylint --rcfile=cmdsh/pylintrc cmdsh

The flake configuration is saved in ``tox.ini``. Run flake on the test and the main
module::

   $ flake8 tests
   $ flake8 src/cmdsh

You are welcome to use the ``pylint`` and ``flake8`` comment directives to disable certain
messages in the code, but pull requests containing these directives will be carefully
scrutinized.

As allowed by `PEP 8 <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_
this project uses a nominal line length of 100 characters.


Documentation
-------------

The documentation is written in reStructured Test, and turned into HTML using
`Sphinx <http://www.sphinx-doc.org>`_::

   $ cd docs
   $ make html

The output will be in ``docs/build/html``.

If you are doing a lot of documentation work, the `sphinx-autobuild
<https://github.com/GaretJax/sphinx-autobuild>`_ module has been integrated.
Type::

   $ cd docs
   $ make livehtml

Then point your browser at `<http://localhost:8000>`_ to see the
documentation automatically rebuilt as you save your changes.

Indent documentation using 2 spaces.

Make a Release
--------------

To make a release and deploy it to `PyPI <https://pypi.python.org/pypi>`_, do the
following:

1. Merge everything to be included in the release into the **develop** branch.

2. Run ``tox`` to make sure the tests pass in all the supported python versions.

3. Review and update ``CHANGELOG.rst``.

4. Update the milestone corresponding to the release at `<https://github.com/kotfu/cmdsh/milestones>`_

5. Push the **develop** branch to github.

6. Create a pull request on github to merge the **develop** branch into
   **master**. Wait for the checks to pass.

7. Merge the **develop** branch into the **master** branch and close the pull
   request.

8. Tag the **master** branch with the new version number, and push the tag.

9. Build source distribution, wheel distribution, and upload them to pypi staging::

     $ invoke pypi-test

10. Build source distribution, wheel distribution, and upload them to pypi::

     $ invoke pypi

11. Docs are automatically deployed to `<http://cmdsh.readthedocs.io/en/stable/>`_. Make sure they look good.

12. Switch back to the **develop** branch. Add an **Unreleased** section to
    the top of ``CHANGELOG.rst``. Push the change to github.
