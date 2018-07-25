.. _timtools.build:

==================
Build the zip file
==================

How to set up a build environment on a Windows machine:

- Install Python 2 : Go to https://www.python.org/downloads/windows/
  
- Install `pywin32 <https://github.com/mhammond/pywin32>`__

- Install `PIL <http://www.pythonware.com/products/pil/>`__
  
- (If Microsoft Visual C++ 14.0 is required, get it with `Microsoft
  Visual C++ Build Tools
  <http://landinghub.visualstudio.com/visual-cpp-build-tools>`__)

- pip install -e timtools

We cannot use pipenv because it doesn't support -e switch for install.

When your build environment is set up, simply run the file
:file:`mkdist.bat` in the project's root directory.
  
This creates a file :file:`timtools.zip` in the download folder
of the documentation tree (:file:`docs\dl`).

You can test the exe files as follows::

  > cd dist\timtools
  > openmail --help

  
You can then publish the documentation tree from an 
atelier environment as follows::

  $ go tt
  $ inv bd pd
