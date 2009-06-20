##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
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
