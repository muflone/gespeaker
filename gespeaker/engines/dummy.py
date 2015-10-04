##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2014 Fabio Castelli
#     License: GPL-2+
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

import multiprocessing
import time
import os

from gespeaker.constants import SIGCONT, SIGSTOP
from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import KEY_ENGINE, KEY_FILENAME, KEY_NAME, KEY_LANGUAGE, KEY_GENDER

class EngineDummy(EngineBase):
  def __init__(self, settings):
    """Initialize the engine"""
    super(self.__class__, self).__init__(settings)
    self.name = 'Dummy'

  def get_languages(self):
    """Get the list of all the supported languages"""
    result = super(self.__class__, self).get_languages()
    result.append({
      KEY_ENGINE: self.name,
      KEY_FILENAME: '',
      KEY_NAME: 'dummy',
      KEY_LANGUAGE: 'A dummy language',
      KEY_GENDER: 'unknown'
      })
    return result

  def play(self, text, language, on_play_completed):
    """Play a text using the specified language"""
    super(self.__class__, self).play(text, language, on_play_completed)
    self.process_speaker = multiprocessing.Process(
      target=self._do_play, args=(text, ))
    self.process_speaker.start()

  def _do_play(self, text):
    """Play the text"""
    for letter in text:
      print(letter)
      time.sleep(0.1)

  def is_playing(self, on_play_completed):
    """Check if the engine is playing and call on_play_completed callback
    when the playing has been completed"""
    if self.process_speaker and not self.process_speaker.is_alive():
      self.playing = False
      self.process_speaker = None
    return super(self.__class__, self).is_playing(on_play_completed)

  def stop(self):
    """Stop any previous play"""
    if self.process_speaker:
      # Show terminate message when debug is activated
      self.settings.debug_line('Terminate %s engine with pid %d' % (
        self.name, self.process_speaker.pid))
      self.process_speaker.terminate()
    return super(self.__class__, self).stop()

  def pause(self, status):
    """Pause a previous play or resume after pause"""
    super(self.__class__, self).pause(status)
    if self.process_speaker:
      # Show pause message when debug is activated
      self.settings.debug_line('%s %s engine with pid %d' % (
        status and 'Pause' or 'Resume',
        self.name, self.process_speaker.pid))
      os.kill(self.process_speaker.pid, status and SIGSTOP or SIGCONT)
    return True
