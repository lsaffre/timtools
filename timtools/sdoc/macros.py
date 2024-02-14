## Copyright 2003-2009 Luc Saffre
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

import os

localRoot = ""
targetRoot = ""
SRC_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
SRC_ROOT = os.path.abspath(SRC_ROOT)
print("SRC_ROOT =", SRC_ROOT)


def fileref(filename):
    href = "../../" + filename
    return url(href, filename)


def url(url, label=None, title=None):
    if label is None:
        label = url
    if title is None:
        title = ""
    r = """

.. raw:: html

   <a href="%(url)s" title="%(title)s">%(label)s</a>
""" % locals()
    # print r
    return r
