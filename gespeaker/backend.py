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

import gespeaker.engines

class Backend(object):
  def __init__(self):
    """Initialize the backend"""
    self.engines = {}
    self.on_play_complete = None
    self.current_engine = None
    # Load engines
    for engine in gespeaker.engines.engines:
      obj_engine = engine()
      self.engines[obj_engine.name] = obj_engine

  def get_languages(self):
    """Get the list of the languages for all the engines"""
    result = []
    for engine in self.engines.values():
      result.extend(engine.get_languages())
    return result

  def get_variants(self):
    """Get the list of the variants for all the engines"""
    result = []
    for engine in self.engines.values():
      result.extend(engine.get_variants())
    return result

  def set_current_engine(self, engine):
    """Set the current engine"""
    self.current_engine = engine

  def play(self, text, language, variant):
    """Play the text using the language and the variant"""
    return self.engines[self.current_engine].play(
      text, language, variant, self.on_play_complete)

  def stop(self):
    """Stop any previous play"""
    return self.engines[self.current_engine].stop()
