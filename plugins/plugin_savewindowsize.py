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

NAME = 'Save window size'
VERSION = '0.1'
AUTHOR = 'Fabio Castelli'
DESCRIPTION = 'Save window size on close and restore on startup'

import Settings
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_SaveWindowSize(GespeakerPlugin):
  def on_uiready(self, ui):
    self.ui = ui
    # Restore window size
    if Settings.get('SaveWindowSize'):
      width = Settings.get('MainWindowWidth')
      height = Settings.get('MainWindowHeight')
      self.logger('Load window size (%dx%d)' % (width, height))
      self.ui.winMain.set_default_size(width, height)
  
  def on_closing(self):
    # Save window size if SaveWindowSize is set
    if Settings.get('SaveWindowSize'):
      sizes = self.ui.winMain.get_size()
      self.logger('Save window size (%dx%d)' % (sizes[0], sizes[1]))
      Settings.set('MainWindowWidth', sizes[0])
      Settings.set('MainWindowHeight', sizes[1])
      Settings.set('SettingsExpander', self.ui.expSettings.get_expanded())

plugin = GespeakerPlugin_SaveWindowSize(NAME, VERSION, DESCRIPTION, AUTHOR)
register_plugin(NAME, plugin)
