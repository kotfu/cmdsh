#
# -*- coding: utf-8 -*-
"""setuptools based setup for cmdsh

"""

from os import path

from setuptools import setup, find_packages

#
# get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cmdsh',
    use_scm_version=True,

    description='A python library for creating interactive language shells.',
    long_description=long_description,

    author='Jared Crapo',
    author_email='jared@kotfu.net',
    url='https://github.com/kotfu/cmdsh',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='cmd command shell',

    packages=find_packages(where="src"),
    package_dir={'':'src'},

    python_requires='>=3.5',
    install_requires=[
        ],

    setup_requires=['setuptools_scm'],

    # dependencies for development and testing
    # $ pip3 install -e .[dev]
    extras_require={
        'dev': ['pytest', 'pytest-mock', 'tox',
                'codecov', 'pytest-cov', 'pytest-xdist',
                'pylint', 'flake8', 'rope',
                'setuptools_scm', 'invoke',
                'sphinx', 'sphinx-autobuild', 'wheel', 'twine'],
    },

)
