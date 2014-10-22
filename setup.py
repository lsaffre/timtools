from distutils.core import setup # , Extension
# import py2exe
execfile('timtools/project_info.py')
setup(**SETUP_INFO)
