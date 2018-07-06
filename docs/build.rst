.. _timtools.build:

==================
Build the zip file
==================

How to set up a build environment on a Windows machine:

- Install Python : Go to https://www.python.org/downloads/windows/ and
  select "Latest Python 3 Release".  Choose "Windows x86 executable
  installer" (or -64) and run it as usual with default installation
  options.
  
- Install `pywin32 <https://github.com/mhammond/pywin32>`__

- Install `PIL <http://www.pythonware.com/products/pil/>`__
  
- (If Microsoft Visual C++ 14.0 is required, get it with `Microsoft
  Visual C++ Build Tools
  <http://landinghub.visualstudio.com/visual-cpp-build-tools>`__)

- pip install -e timtools

We cannot use pipenv because it doesn't support -e switch for install.

When your build environment is set up, here is how to create a
distribution file::

  i  
  pyinstaller timtools/scripts/openmail.py
  pyinstaller timtools/scripts/prn2pdf.py
  pyinstaller timtools/scripts/prnprint.py

  cd dist
  mkdir timtools
  xcopy openmail\* timtools /s
  xcopy prn2pdf\* timtools /s
  xcopy prnprint\* timtools /s
  python -m zipfile -c timtools.zip timtools

  
This creates a file :file:`timtools.zip` in your `dist` folder.
  
