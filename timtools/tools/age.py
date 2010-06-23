## Copyright 2006-2009 Luc Saffre
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

# posted on 2006-10-03 by a pretty average guy called "bjorn"
# copied from http://blog.tkbe.org/archive/python-how-old-are-you/

from datetime import date as _date
from calendar import monthrange as _monthrange

def age(dob, today=_date.today()):

    y = today.year - dob.year
    m = today.month - dob.month
    d = today.day - dob.day
       
    while m <0 or d <0:
        while m <0:
            y -= 1
            m = 12 + m  # m is negative
        if d <0:
            m -= 1
            days = days_previous_month(today.year, today.month)
            d = max(0, days - dob.day) + today.day
    return y, m, d
       
def days_previous_month(y, m):
    m -= 1
    if m == 0:
        y -= 1
        m = 12
    _, days = _monthrange(y, m)
    return days

