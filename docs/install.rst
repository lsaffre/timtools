===================
Installing timtools
===================

Quick instructions
==================

- Disable your current timtools (and make sure to have a backup copy)
  by renaming the :file:`timtools` subdirectory in your TIM directory
  to :file:`timtools.old` (or something else).

- Download the :xfile:`timtools.zip` file from
  http://timtools.lino-framework.org/dl/timtools.zip

- Unzip its contents into your TIM directory. It should create a new
  :file:`timtools` subdirectory.


Explanations
============


.. xfile:: timtools.zip

    This is the file that contains the latest released version.

The name of the download file is always
:xfile:`timtools.zip` regardless of the version.

.. py2rst::

  from timtools.setup_info import SETUP_INFO
  print("The currently published file contains version {}.".format(SETUP_INFO['version']))


    
    
    
