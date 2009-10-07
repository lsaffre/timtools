from distutils.core import setup, Extension
import timtools
setup(name='timtools',
      version=timtools.__version__,
      description="A collection of command-line tools for Win32",
      license='GPL',
      packages=['timtools'],
      author='Luc Saffre',
      author_email='luc.saffre@gmail.com',
      requires=['reportlab','PIL'],
      url="http://code.google.com/p/timtools/",
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
""".splitlines()
      )
