#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# -- General configuration ------------------------------------------------

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'


project = 'cmdsh'
copyright = ''
author = ''
html_show_copyright=False

# get the version and release via setuptools_scm
from pkg_resources import get_distribution
release = get_distribution('cmdsh').version
version = '.'.join(release.split('.')[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# when we autodoc classes, show the methods in the order they are in the
# source
autodoc_member_order = 'bysource'

# Make the default role of ` try to link to anything it can find.
# This allows for cleaner docstrings which still get linked when
# we build the documentation.
default_role = 'any'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
#exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'show_powered_by': 'false',
    'description': 'Command line tool and python library for managing a Tomcat server.',
    'sidebar_width': '260px',
    'page_width': '1135px',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
#        'navigation.html',
		'globaltoc.html',
        'searchbox.html',
#        'relations.html',  # needs 'show_related': True theme option to display
#        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'cmdshdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'cmdsh.tex', 'cmdsh Documentation',
     'Jared Crapo', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'cmdsh', 'cmdsh Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'cmdsh', 'cmdsh Documentation',
     author, 'cmdsh', 'One line description of project.',
     'Miscellaneous'),
]