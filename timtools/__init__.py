# Copyright 2003-2018 Rumma & Ko Ltd
# License: BSD (see COPYING.txt)

# import os
# execfile(os.path.join(os.path.dirname(__file__), 'project_info.py'))
# from timtools.setup_info import SETUP_INFO

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://timtools.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/timtools/blob/master/%s'
doc_trees = ['docs']
