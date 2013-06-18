##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2013 Fabio Castelli
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
# 
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

PLUGIN_NAME = 'Emesene'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Emesene plugin'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = 'http://www.ubuntutrucchi.it/'

EMESENE_PLUGIN_FILENAME = 'gespeaker_emesene.py'

import os
from os.path import join, exists, isdir, islink
from xdg.BaseDirectory import xdg_config_home
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Emesene(GespeakerPlugin):
  def load(self):
    "Plugin load"
    GespeakerPlugin.load(self)
    # Warning! Emesene 1.6 uses absolute .config folder, not xdg config home
    self.plugins_path = os.path.join(
      xdg_config_home, 'emesene1.0', 'pluginsEmesene')
    self.plugin_filename = join(self.plugins_path, EMESENE_PLUGIN_FILENAME)
    if exists(self.plugins_path) and isdir(self.plugins_path):
      if exists(self.plugin_filename) or islink(self.plugin_filename):
        # Remove previous .py file
        os.remove(self.plugin_filename)
      if exists('%sc' % self.plugin_filename):
        # Remove previous .pyc file
        os.remove('%sc' % self.plugin_filename)
      # Symlink emesene
      os.symlink(
        join(__path__[0], EMESENE_PLUGIN_FILENAME),
        join(self.plugins_path, EMESENE_PLUGIN_FILENAME)
      )

plugin = GespeakerPlugin_Emesene(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
