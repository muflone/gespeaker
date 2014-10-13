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

from gi.repository import Gtk

from .base import ModelBase

class ModelVariants(ModelBase):
  COL_VARIANT = 0
  COL_DESCRIPTION = 1
  def __init__(self, model):
    super(self.__class__, self).__init__(model)
    self.model = model

  def add(self, variant, description):
    """Add a new row in the model"""
    super(self.__class__, self).add(
      items=(variant, description))

  def get_variant(self, treepath):
    """Get the engine of a row"""
    return self.get_model_data(treepath, self.COL_VARIANT)

  def get_description(self, treepath):
    """Get the language of a row"""
    return self.get_model_data(treepath, self.COL_DESCRIPTION)
