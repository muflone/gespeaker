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

from gi.repository import GObject

KEY_ENGINE = 'engine'
KEY_FILENAME = 'filename'
KEY_NAME = 'name'
KEY_LANGUAGE = 'language'
KEY_GENDER = 'gender'

class EngineBase(object):
  def __init__(self):
    """Initialize the engine"""
    self.__name = None
    self.has_gender = True
    self.playing = False

  def get_languages(self):
    """Get the list of all the supported languages"""
    return []

  def get_variants(self):
    """Get the list of all the supported variants"""
    return []

  def play(self, text, language, variant, on_play_completed):
    """Play a text using the specified language and variant"""
    self.playing = True
    # Add a timer to check when the playing has stopped
    GObject.timeout_add(500, self.is_playing, on_play_completed)

  def is_playing(self, on_play_completed):
    """Check if the engine is playing and call on_play_completed callback
    when the playing has been completed"""
    if self.playing:
      return True
    else:
      # Call the callback if provided
      if on_play_completed:
        on_play_completed()
      # Stop iterations
      return False
