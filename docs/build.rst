==================
Build the zip file
==================

How to set up a build environment on a Windows machine:

- Install Python : Go to https://www.python.org/downloads/windows/ and
  select "Latest Python 3 Release".  Choose "Windows x86 executable
  installer" (or -64) and run it as usual with default installation
  options.
  
- Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
  
- pip install -e timtools
- pip install pyinstaller

We don't recommend to use pipenv because it doesn't support -e switch
for install.

When your build environment is set up, here is how to create a
distribution file::

  i  
  pyinstaller timtools/scripts/openmail
  pyinstaller timtools/scripts/prn2pdf
  pyinstaller timtools/scripts/prnprint
  cd dist
  python -m zipfile -c timtools.zip timtools

  
This creates a file :file:`timtools.zip` in your `dist` folder.
  
