# Version 1.0.4 #

See [Releases](Releases.md) for a list of other versions.

Released 2010-03-27

## Changes ##

  1. Fixes [Issue 8](https://code.google.com/p/timtools/issues/detail?id=8) (ImportError: No module named _fontdata\_enc\_winansi). 'mkdist.py' now explicitely includes `reportlab.pdfbase.*`. py2exe doesn't include them automatically because they are imported dynamically._
