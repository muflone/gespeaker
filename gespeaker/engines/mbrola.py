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

import os
import subprocess

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import KEY_ENGINE, KEY_FILENAME, KEY_NAME, KEY_LANGUAGE, KEY_GENDER

MAX_FILE_SIZE = 2000

KEY_ESPEAK_NAME = 'name'
KEY_ESPEAK_GENDER = 'gender'
KEY_ESPEAK_MBROLA = 'mbrola'

class EngineMBROLA(EngineBase):
  def __init__(self, settings):
    """Initialize the engine"""
    super(self.__class__, self).__init__(settings)
    self.name = 'eSpeak + MBROLA'
    self.has_gender = False
    self.dir_languages = '/usr/share/espeak-data/voices/mb'
    self.dir_mbrola_voices = '/usr/share/mbrola'

  def get_languages(self):
    """Get the list of all the supported languages"""
    result = super(self.__class__, self).get_languages()
    for filename in os.listdir(self.dir_languages):
      filepath = os.path.join(self.dir_languages, filename)
      if not os.path.isdir(filepath):
        # Get and add new language from filename
        new_language = self.get_language_from_filename(filepath)
        if new_language:
          result.append(new_language)
    return result

  def get_variants(self):
    """Get the list of all the supported variants"""
    result = super(self.__class__, self).get_variants()
    return result

  def get_language_from_filename(self, filename):
    """Get language information from the specified filename"""
    info = None
    # Only process files whose size is less than max file size
    if os.path.getsize(filename) <= MAX_FILE_SIZE:
      with open(filename, 'r') as f:
        info = {}
        info[KEY_ENGINE] = self.name
        info[KEY_FILENAME] = filename
        info[KEY_NAME] = os.path.basename(filename)
        info[KEY_GENDER] = ''
        info[KEY_ESPEAK_MBROLA] = ''
        # Extract information from the voice file
        for line in f.readlines():
          # Remove newline characters
          line = line.replace('\r', '')
          line = line.replace('\n', '')
          if ' ' in line:
            values = line.split(' ')
            key = values[0]
            if key == KEY_ESPEAK_NAME:
              # Save the language name
              description = values[1]
              description = description.replace('-mbrola-', ' ')
              description = description.replace('mbrola-', '')
              description = description.replace('-mbrola', '')
              description = description.replace('-mb-', ' ')
              description = description.replace('en-', '')
              description = description.title()
              description = description.replace('Us ', 'US ')
              info[KEY_LANGUAGE] = description
            elif key == KEY_ESPEAK_GENDER:
              # Save the gender
              info[KEY_GENDER] = values[1]
            elif key == KEY_ESPEAK_MBROLA:
              # Save the MBROLA data file
              info[KEY_ESPEAK_MBROLA] = values[1]
    # Check if the MBROLA data file exists
    dir_mb_voice = os.path.join(self.dir_mbrola_voices, info[KEY_ESPEAK_MBROLA])
    if info[KEY_ESPEAK_MBROLA]:
      if os.path.isdir(dir_mb_voice):
        if os.path.isfile(os.path.join(dir_mb_voice, info[KEY_ESPEAK_MBROLA])):
          return info
        else:
          # MBROLA voice file not found
          self.settings.debug_line(
            'MBROLA data file %s not found for voice %s' % (
            os.path.join(dir_mb_voice, info[KEY_ESPEAK_MBROLA]), info[KEY_NAME]))
      else:
        # MBROLA voice directory not found
        self.settings.debug_line(
          'MBROLA data directory %s not found for voice %s' % (
          dir_mb_voice, info[KEY_NAME]))
      return None

  def play(self, text, language, variant, on_play_completed):
    """Play a text using the specified language and variant"""
    super(self.__class__, self).play(text, language, variant, on_play_completed)
    arguments = ['espeak', '-v']
    if not variant:
      arguments.append(language)
    else:
      arguments.append('%s+%s' % (language, variant))
    self.settings.debug_line(arguments)
    self._espeak_process = subprocess.Popen(arguments, stdin=subprocess.PIPE)
    self._espeak_process.stdin.write(text)
    self._espeak_process.stdin.flush()
    self._espeak_process.stdin.close()

  def is_playing(self, on_play_completed):
    """Check if the engine is playing and call on_play_completed callback
    when the playing has been completed"""
    if self._espeak_process and self._espeak_process.poll() is not None:
      self.playing = False
      self._espeak_process = None
    return super(self.__class__, self).is_playing(on_play_completed)

  def stop(self):
    """Stop any previous play"""
    if self._espeak_process:
      # Show terminate message when debug is activated
      self.settings.debug_line('Terminate %s engine with pid %d' % (
          self.name, self._espeak_process.pid))
      self._espeak_process.terminate()
    return super(self.__class__, self).stop()