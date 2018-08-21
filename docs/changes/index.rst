===================
Changes in timtools
===================


.. _tt2_0_2:

Version 2.0.2 (not yet released)
===================================

The :cmd:`sync` command failed with a traceback::

    Traceback (most recent call last):
      File "timtools\scripts\sync.py", line 18, in <module>
    ImportError: cannot import name __url__
    [292] Failed to execute script sync


.. _tt2_0_1:

Version 2.0.1 (released 2018-07-25)
===================================

Added also the :cmd:`sendmail` command.


.. _tt2_0_0:

Version 2.0.0 (released 2018-07-06)
===================================

The version bump is because now we use pyinstaller for creating the
:xfile:`timtools.zip` file and because now the source code is publicly
available again for the first time since googlecode was closed.

timtools 2.0.0 fixes a problem in the :cmd:`openmail` command: that
command wrote its temporary file using cp850 encoding, now it uses
UTF-8.

**Warning** : this is the first release of the 2.0 series and it
potentially contains regression bugs which break things.  For example
it includes only the commands :cmd:`sync`, :cmd:`prnprint`,
:cmd:`prn2pdf` and :cmd:`openmail` because these are the only ones we
know to be used.  If you discover that your TIM actually uses some
other timtools command, let us know.

See :doc:`/install` for installation instructions.


Older changes
==============

.. toctree::
   :maxdepth: 1
   :glob:
   
   2012/index
   2010/index
   2009
   2007
   
   

