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

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import KEY_ENGINE, KEY_FILENAME, KEY_NAME, KEY_LANGUAGE, KEY_GENDER

MAX_FILE_SIZE = 2000

KEY_ESPEAK_NAME = 'name'
KEY_ESPEAK_GENDER = 'gender'

class EngineEspeak(EngineBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.name = 'espeak'
    self.languages_path = '/usr/share/espeak-data/voices'

  def get_languages(self):
    result = super(self.__class__, self).get_languages()
    self.get_languages_from_path(self.languages_path, result)
    return result

  def get_languages_from_path(self, path, languages):
    for filename in os.listdir(path):
      # Skip variants and MBROLA voices
      if filename not in ('!v', 'mb'):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
          # Iter each subdirectory
          self.get_languages_from_path(filepath, languages)
        else:
          # Get and add new language from filename
          new_language = self.get_language_from_filename(filepath)
          if new_language:
            languages.append(new_language)

  def get_language_from_filename(self, filename):
    info = None
    # Only process files littler than max file size
    if os.path.getsize(filename) <= MAX_FILE_SIZE:
      with open(filename, 'r') as f:
        info = {}
        info[KEY_ENGINE] = self.name
        info[KEY_FILENAME] = filename
        info[KEY_NAME] = os.path.basename(filename)
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
              description = description.replace('-', ' ')
              description = description.replace('_', ' ')
              info[KEY_LANGUAGE] = description.title()
            if key == KEY_ESPEAK_GENDER:
              # Save the gender
              info[KEY_GENDER] = values[1]
    return info
