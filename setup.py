import sys
if sys.version_info[0] != 2:
    raise Exception("Requires Python 2")

from setuptools import setup
fn = 'timtools/setup_info.py'
exec(compile(open(fn, "rb").read(), fn, 'exec'))

if __name__ == '__main__':
    setup(**SETUP_INFO)
