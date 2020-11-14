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

from .base import ModelBase

class ModelLanguages(ModelBase):
  COL_ENGINE = 0
  COL_DESCRIPTION = 1
  COL_NAME = 2
  COL_GENDER = 3
  def __init__(self, model, icon_male, icon_female, icon_unknown):
    super(self.__class__, self).__init__(model)
    self.model = model
    self._gender_map = {
      'male': icon_male,
      'female': icon_female,
      'unknown': icon_unknown
    }

  def add(self, engine, description, name, gender):
    """Add a new row in the model"""
    super(self.__class__, self).add(
      items=(engine, description, name, gender,
        self._gender_map.get(gender, self._gender_map['unknown'])))

  def get_engine(self, treepath):
    """Get the engine of a row"""
    return self.get_model_data(treepath, self.COL_ENGINE)

  def get_description(self, treepath):
    """Get the description of a row"""
    return self.get_model_data(treepath, self.COL_DESCRIPTION)

  def get_name(self, treepath):
    """Get the name of a row"""
    return self.get_model_data(treepath, self.COL_NAME)

  def get_gender(self, treepath):
    """Get the gender of a row"""
    return self.get_model_data(treepath, self.COL_GENDER)
