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

NAME = 'welcome'
VERSION = '0.1'
AUTHOR = 'Fabio Castelli'
DESCRIPTION = 'Play welcome message on startup'

import Settings
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Welcome(GespeakerPlugin):
  def on_uiready(self, ui):
    self.ui = ui
    # Play welcome message if PlayWelcomeText is set
    if Settings.get('PlayWelcomeText'):
      if Settings.get('UseCustomWelcome'):
        # Play customized welcome message
        message = Settings.get('WelcomeText')
      else:
        # Play default welcome message
        message = Settings.default('WelcomeText')
      self.logger('Play welcome message: %s' % message)
      self.ui.txvBuffer.set_text(message)
      self.ui.btnPlayStop.set_active(True)

plugin = GespeakerPlugin_Welcome(NAME, VERSION, DESCRIPTION, AUTHOR)
register_plugin(NAME, plugin)
