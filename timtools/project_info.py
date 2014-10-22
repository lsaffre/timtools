## Copyright 2002-2013 Luc Saffre
## This file is part of the TimTools project.
## TimTools is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## TimTools is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with TimTools; if not, see <http://www.gnu.org/licenses/>.
"""
This module is being execfile'd from `setup.py`, `timtools/__init__.py`
and possibly some external tools, too.
"""
SETUP_INFO = dict(
  name = 'timtools', 
  version = '1.0.6',
  install_requires = ['reportlab','PIP'],
  scripts = ['scripts/per_project'],
  description = "A collection of command-line tools for Win32",
  license = 'GPL',
  test_suite = 'tests',
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://timtools.lino-framework.org",
  long_description="""\
A collection of command-line tools for Win32
""",
  classifiers="""\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: French
Natural Language :: German
Operating System :: Microsoft :: Windows :: Windows NT/2000
Programming Language :: Python :: 2
Topic :: Home Automation
Topic :: Office/Business
Topic :: Utilities
Topic :: Printing
""".splitlines())

SETUP_INFO.update(packages = [str(n) for n in """
timtools
""".splitlines() if n])
  
