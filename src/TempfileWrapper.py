##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2014 Fabio Castelli
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
# 
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

import tempfile
import sys
import os

PYTHON_VERSION = sys.version_info[0:2]

class NamedTemporaryFile(object):
  "Replacement for NamedTemporaryFile compatible with python 2.5"
  def __init__(self, mode='w+b', delete=True):
    self.delete = delete
    if PYTHON_VERSION[0] == 2 and PYTHON_VERSION[1] >= 6:
      self.tempfile = tempfile.NamedTemporaryFile(mode=mode, delete=delete)
      self.name = self.tempfile.name
    else:
      # Python < 2.6 doesn't have a delete argument for NamedTemporaryFile
      # We have to proceed manually :-\
      self.name = tempfile.mkstemp()[1]
      self.tempfile = open(self.name, mode=mode)
  
  def __del__(self):
    self.close()
    self.tempfile = None

  def write(self, data):
    "Write data to the temporary file"
    return self.tempfile.write(data)

  def close(self):
    "Close the temporary file and delete it if requested"
    ret = self.tempfile.close()
    if PYTHON_VERSION[0] == 2 and PYTHON_VERSION[1] < 6 and self.delete:
      # Manually deletion of temporary filename
      os.remove(self.name)
    return ret
