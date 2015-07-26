##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
# Copyright: 2009-2015 Fabio Castelli
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
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

PLUGIN_NAME = 'Save window size'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Save window size on close and restore it on startup'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = ''

import Settings
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_SaveWindowSize(GespeakerPlugin):
  def on_uiready(self, ui):
    self.ui = ui
    # Restore window size
    width = Settings.get('MainWindowWidth')
    height = Settings.get('MainWindowHeight')
    self.logger('Load window size (%dx%d)' % (width, height))
    self.ui.winMain.set_default_size(width, height)
  
  def on_closing(self):
    # Save window size
    sizes = self.ui.winMain.get_size()
    self.logger('Save window size (%dx%d)' % (sizes[0], sizes[1]))
    Settings.set('MainWindowWidth', sizes[0])
    Settings.set('MainWindowHeight', sizes[1])
    Settings.set('SettingsExpander', self.ui.expSettings.get_expanded())

plugin = GespeakerPlugin_SaveWindowSize(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
