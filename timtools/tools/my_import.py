## Copyright 2002-2009 Luc Saffre
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

import imp


def my_import(name):
    # http://www.python.org/doc/current/lib/built-in-funcs.html
    mod = __import__(name)
    # mod = __import__(name,globals(),locals(),[])
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def module_exists(full_name, path=None):
    """
    tests whether the module exists but does not import it.
    see http://www.python.org/doc/current/library/imp.html#module-imp
    """
    a = full_name.split('.', 1)
    if len(a) == 1:
        # simple module name without package
        try:
            (file, pathname, description) = imp.find_module(full_name, path)
            if file is not None: file.close()
        except ImportError, e:
            return False
        return True
    assert len(a) == 2
    (file, pathname, description) = imp.find_module(a[0], path)
    if description[-1] != imp.PKG_DIRECTORY:
        return False
    pkg = imp.load_module(a[0], file, pathname, description)
    if file is not None: file.close()
    return module_exists(a[1], pkg.__path__)
