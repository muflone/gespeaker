##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2010 Fabio Castelli
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

PLUGIN_NAME = 'aMSN'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'aMSN plugin'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.png' % __path__[0]
PLUGIN_WEBSITE = 'http://www.ubuntutrucchi.it/'

import os
from os.path import join, exists, isdir, islink
from xdg.BaseDirectory import _home as xdg_home
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_AMSN(GespeakerPlugin):
  def load(self):
    "Plugin load"
    GespeakerPlugin.load(self)
    plugin_path = join(xdg_home, '.amsn', 'plugins')
    plugin_filename = join(plugin_path, 'Gespeaker')
    #
    if exists(plugin_path) and isdir(plugin_path):
      if exists(plugin_filename) or islink(plugin_filename):
        # Remove previous gespeaker symlink
        os.remove(plugin_filename)
      # Symlink plugin
      os.symlink(__path__[0], plugin_filename)
        

plugin = GespeakerPlugin_AMSN(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
