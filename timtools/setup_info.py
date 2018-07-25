## Copyright 2002-2018 Rumma & Ko Ltd
"""
This module is being execfile'd from `setup.py`, `timtools/__init__.py`
and possibly some external tools, too.
"""
SETUP_INFO = dict(
  name = 'timtools', 
  version = '2.0.1',
  install_requires = ['reportlab', 'pyinstaller'],
  description = "A collection of command-line tools for Win32",
  license = 'GPL',
  test_suite = 'tests',
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://timtools.lino-framework.org",
  long_description="""\
timtools is a collection of command-line tools for TIM.

The central project homepage is http://timtools.lino-framework.org

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

# scripts = "prn2pdf prnprint openmail sync"
# scripts = ['timtools/scripts/{}.py'.format(n) for n in scripts.split()]
# SETUP_INFO.update(scripts=scripts)
