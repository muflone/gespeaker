##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
# Copyright: 2009-2015 Fabio Castelli
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
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import subprocess
import sys
import os

PIPE = subprocess.PIPE
PYTHON_VERSION = sys.version_info[0:2]

class Popen(object):
  def __init__(self, args, stdin=None, stdout=None, stderr=None, shell=False):
    self.process = subprocess.Popen(args=args, 
      stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)
    self.stdin = self.process.stdin
    self.stdout = self.process.stdout
    self.stderr = self.process.stderr
    self.pid = self.process.pid

  def __del__(self):
    self.process = None
  
  def communicate(self):
    return self.process.communicate()

  def poll(self):
    return self.process.poll()

  def terminate(self):
    "Python version < 2.6 doesn't have a terminate method for subprocess"
    if PYTHON_VERSION[0] == 2 and PYTHON_VERSION[1] >= 6:
      return self.process.terminate()
    else:
      signal = 15
      return os.kill(self.pid, signal)

  def stop(self):
    signal = 19
    if PYTHON_VERSION[0] == 2 and PYTHON_VERSION[1] >= 6:
      return self.process.send_signal(signal)
    else:
      return os.kill(self.pid, signal)

  def resume(self):
    signal = 18
    if PYTHON_VERSION[0] == 2 and PYTHON_VERSION[1] >= 6:
      return self.process.send_signal(signal)
    else:
      return os.kill(self.pid, signal)

  def wait(self):
    return self.process.wait()
