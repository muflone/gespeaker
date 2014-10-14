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

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import KEY_ENGINE, KEY_FILENAME, KEY_NAME, KEY_LANGUAGE, KEY_GENDER

class EngineDummy(EngineBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.name = 'Dummy'
    self.has_gender = False
    self.has_variants = True

  def get_languages(self):
    result = super(self.__class__, self).get_languages()
    result.append({
      KEY_ENGINE: self.name,
      KEY_FILENAME: '',
      KEY_NAME: 'dummy',
      KEY_LANGUAGE: 'A dummy language',
      KEY_GENDER: ''
      })
    return result

  def get_variants(self):
    result = super(self.__class__, self).get_variants()
    result.append({
      KEY_ENGINE: self.name,
      KEY_FILENAME: '',
      KEY_NAME: 'dummy',
      KEY_LANGUAGE: 'A dummy variant',
      KEY_GENDER: ''
      })
    return result
