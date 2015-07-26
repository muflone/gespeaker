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

PLUGIN_NAME = 'Welcome message'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Play welcome message on startup'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = ''
PLUGIN_WEBSITE = ''

import Settings
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Welcome(GespeakerPlugin):
  def on_uiready(self, ui):
    # Play welcome message if PlayWelcomeText is set
    if Settings.get('PlayWelcomeText'):
      if Settings.get('UseCustomWelcome'):
        # Play customized welcome message
        message = Settings.get('WelcomeText')
      else:
        # Play default welcome message
        message = Settings.default('WelcomeText')
      self.logger('Play welcome message: %s' % message)
      ui.proxy['text.set'](message, 0)
      ui.proxy['espeak.play'](None, None)

plugin = GespeakerPlugin_Welcome(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
