fn = 'timtools/setup_info.py'
exec(compile(open(fn, "rb").read(), fn, 'exec'))

from setuptools import setup
import sys

if __name__ == '__main__':

    if False:  # sys.version_info[0] != 2:
        #raise Exception("Requires Python 2")
        print("Requires Python 2. Exiting silently.")
    else:
        setup(**SETUP_INFO)
