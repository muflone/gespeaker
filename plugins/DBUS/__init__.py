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

NAME = 'DBUS'
VERSION = '0.1'
AUTHOR = 'Fabio Castelli'
DESCRIPTION = 'DBUS interface plugin'

from plugins import GespeakerPlugin, register_plugin
import dbus.glib
from dbus_service import GespeakerDBUSService
from dbus_text import GespeakerDBUSServiceText
from dbus_ui import GespeakerDBUSServiceUI
from dbus_espeak import GespeakerDBUSServiceEspeak
from dbus_voice import GespeakerDBUSServiceVoice
from dbus_cmdline import parseArgs

class GespeakerPlugin_DBUS(GespeakerPlugin):
  def load(self, gespeakerUI):
    "Plugin load"
    GespeakerPlugin.load(self, gespeakerUI)
    GespeakerDBUSService(self.ui)
    GespeakerDBUSServiceText(self.ui)
    GespeakerDBUSServiceUI(self.ui)
    GespeakerDBUSServiceEspeak(self.ui)
    GespeakerDBUSServiceVoice(self.ui)
    parseArgs()

  def unload(self):
    "Plugin reload"
    pass

  def reload(self):
    "Plugin reload"
    pass

plugin = GespeakerPlugin_DBUS(NAME, VERSION, DESCRIPTION, AUTHOR)
register_plugin(NAME, plugin)
