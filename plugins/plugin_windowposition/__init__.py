##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2014 Fabio Castelli
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

PLUGIN_NAME = 'Save window position'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Save window position on close and restore it on startup'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = ''

import Settings
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_SaveWindowPosition(GespeakerPlugin):
  def on_uiready(self, ui):
    self.ui = ui
    # Restore window size
    left = Settings.get('MainWindowLeft')
    top = Settings.get('MainWindowTop')
    self.logger('Load window position (%d,%d)' % (left, top))
    self.ui.set_position('%dx%d' % (left, top))
  
  def on_closing(self):
    # Save window size
    sizes = self.ui.winMain.get_position()
    self.logger('Save window position (%d,%d)' % (sizes[0], sizes[1]))
    Settings.set('MainWindowLeft', sizes[0])
    Settings.set('MainWindowTop', sizes[1])

plugin = GespeakerPlugin_SaveWindowPosition(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
