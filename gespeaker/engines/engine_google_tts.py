##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2015 Fabio Castelli
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

import os
import subprocess
import tempfile

import gtts
import psutil

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import KEY_ENGINE, KEY_NAME, KEY_LANGUAGE, KEY_GENDER

class EngineGoogleTTS(EngineBase):
  name = 'Google TTS'
  required_modules = ('gtts', )

  def __init__(self, settings):
    """Initialize the engine"""
    super(self.__class__, self).__init__(settings, globals())

  def get_languages(self):
    """Get the list of all the supported languages"""
    result = super(self.__class__, self).get_languages()
    # Languages map for gender
    languages_map = {
      'male': ('af', 'sq', 'ar', 'hy', 'ca', 'hr', 'eo', 'is', 'lv', 'mk', 'ro',
        'sr', 'sw', 'ta', 'vi', 'cy'),
      'female': ('cs', 'da', 'de', 'el', 'en', 'en-au', 'en-uk', 'en-us',
        'es', 'es-es', 'es-us', 'fi', 'fr', 'ht', 'hi', 'hu', 'id', 'it', 'ja',
        'ko', 'la', 'nl', 'no', 'pl', 'pt', 'pt-br', 'ru', 'sk', 'sv', 'th',
        'tr', 'zh', 'zh-cn', 'zh-tw', 'zh-yue')
    }
    for name, description in gtts.gTTS.LANGUAGES.items():
      new_language = {}
      new_language[KEY_ENGINE] = self.name
      new_language[KEY_NAME] = name
      new_language[KEY_LANGUAGE] = description
      new_language[KEY_GENDER] = 'unknown'
      for gender in 'male', 'female':
        if name in languages_map[gender]:
          new_language[KEY_GENDER] = gender
          break
      result.append(new_language)
    return result

  def play(self, text, language, on_play_completed):
    """Play a text using the specified language"""
    super(self.__class__, self).play(text, language, on_play_completed)
    self._tmp_filename = tempfile.mkstemp(prefix='gespeaker_', suffix='.mp3')[1]
    self.__process_speaker = gtts.gTTS(text=text, lang=language)
    self.__process_speaker.save(self._tmp_filename)
    self.__process_speaker = None
    
    arguments = ['mpg123', '-q']
    arguments.append(self._tmp_filename)
    self.settings.debug_line(arguments)
    self.__process_player = subprocess.Popen(arguments)

  def is_playing(self, on_play_completed):
    """Check if the engine is playing and call on_play_completed callback
    when the playing has been completed"""
    if self.__process_player and self.__process_player.poll() is not None:
      self.playing = False
      self.__process_player = None
    return super(self.__class__, self).is_playing(on_play_completed)

  def stop(self):
    """Stop any previous play"""
    if self.__process_player:
      # Show terminate message when debug is activated
      self.settings.debug_line('Terminate %s engine with pid %d' % (
          self.name, self.__process_player.pid))
      self.__process_player.terminate()
    # Remove stale temporary file
    if os.path.isfile(self._tmp_filename):
      os.remove(self._tmp_filename)
    return super(self.__class__, self).stop()

  def pause(self, status_pause):
    """Pause a previous play or resume after pause"""
    super(self.__class__, self).pause(status_pause)
    for process in (self.__process_speaker, self.__process_player):
      if process:
        # Show pause message when debug is activated
        self.settings.debug_line('%s %s engine with pid %d' % (
          status_pause and 'Pause' or 'Resume',
          self.name, process.pid))
        psprocess = psutil.Process(process.pid)
        if status_pause:
          psprocess.suspend()
        else:
          psprocess.resume()
    return True

engine_classes = (EngineGoogleTTS, )
