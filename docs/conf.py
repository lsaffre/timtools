# -*- coding: utf-8 -*-
#
# Multilingual websites with Sphinx documentation build configuration file, created by
# sphinx-quickstart on Thu Nov 13 11:09:54 2008.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default; values that are commented out
# serve to show the default.

from timtools.setup_info import SETUP_INFO

extensions = []
extlinks = {}

from atelier.sphinxconf import configure
configure(globals())

# extensions += ['atelier.sphinxconf.complex_tables']
# extensions += ['sphinx.ext.autosummary']


# Add any paths that contain templates here, relative to this directory.
templates_path = ['.templates']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = "timtools"
copyright = '2002-2018 Rumma & Ko Ltd'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# version = '0'
# The full version, including alpha/beta/rc tags.
version = SETUP_INFO['version']

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'

html_sidebars = {
   '**': ['globaltoc.html', 'searchbox.html', 'links.html'],
}



html_static_path = ['.static']


# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'
last_updated = True

html_favicon = 'favicon.ico'


# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'timtools'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
# latex_documents = [
#   ('index', 'timtools.tex', ur'timtools', ur'Luc Saffre', 'manual'),
# ]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

#language="de"

# srcref_base_uri="http://code.google.com/p/timtools/source/browse"


# http://sphinx.pocoo.org/theming.html
# my_font_family = "Swiss, Helvetica, 'Liberation Sans'"
# html_theme_options = {
#     "font_family": my_font_family,
#     "head_font_family": my_font_family,
# }
