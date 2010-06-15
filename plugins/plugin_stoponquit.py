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

NAME = 'Stop on Quit'
VERSION = '0.1'
AUTHOR = 'Fabio Castelli'
DESCRIPTION = 'Terminate play on quit'

from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_StopOnQuit(GespeakerPlugin):
  def on_uiready(self, ui):
    self.ui = ui
  
  def on_closed(self):
    if self.ui.checkIfPlaying():
      self.logger('interrupting previous play')
      self.ui.stopPlaying()

plugin = GespeakerPlugin_StopOnQuit(NAME, VERSION, DESCRIPTION, AUTHOR)
register_plugin(NAME, plugin)
