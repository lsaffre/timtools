## Copyright 2005-2009 Luc Saffre
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

from types import IntType


class Month:

    def __init__(self, year, month):
        #assert month > 0 and month < 13
        self.year = year
        self.month = month

    def __str__(self):
        return "%02d/%d" % (self.month, self.year)

    def __repr__(self):
        return "Month(%d,%d)" % (self.year, self.month)

    def __add__(self, other):
        assert type(other) == IntType
        self.month += other
        if self.month > 12:
            q, r = divmod(self.month, 12)
            self.year += q
            self.month = r
        return self

    def __sub__(self, other):
        if type(other) == IntType:
            return self.__add__(-other)
        return (self.year - other.year) * 12 + (self.month - other.month)

    def __cmp__(self, other):
        if self.year > other.year: return 1
        if self.year < other.year: return -1
        if self.month > other.month: return 1
        if self.month < other.month: return -1
        return 0

    def parse(s):
        s = s.replace(".", "-")
        s = s.replace("/", "-")
        l = s.split("-")
        if len(l) == 2:
            l = map(int, l)
            return Month(*l)
        elif len(l) == 1:
            assert len(s) == 6, repr(s)
            y = int(s[0:4])
            m = int(s[4:6])
            return Month(y, m)
        else:
            raise ValueError, repr(s)

    parse = staticmethod(parse)
