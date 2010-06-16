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

PLUGIN_NAME = 'DBUS'
PLUGIN_VERSION = '0.2'
PLUGIN_DESCRIPTION = 'DBUS interfaces'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = ''
PLUGIN_WEBSITE = 'http://www.ubuntutrucchi.it/'

from plugins import GespeakerPlugin, register_plugin
import dbus
import dbus.mainloop.glib
from dbus_service import GespeakerDBUSService
from dbus_text import GespeakerDBUSServiceText
from dbus_ui import GespeakerDBUSServiceUI
from dbus_espeak import GespeakerDBUSServiceEspeak
from dbus_voice import GespeakerDBUSServiceVoice
from dbus_cmdline import parseArgs

class GespeakerPlugin_DBUS(GespeakerPlugin):
  def load(self):
    "Plugin load"
    GespeakerPlugin.load(self)
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


  def unload(self):
    "Plugin reload"
    pass

  def reload(self):
    "Plugin reload"
    pass

  def on_uiready(self, ui):
    GespeakerDBUSService(ui)
    GespeakerDBUSServiceText(ui)
    GespeakerDBUSServiceUI(ui)
    GespeakerDBUSServiceEspeak(ui)
    GespeakerDBUSServiceVoice(ui)
    parseArgs()

plugin = GespeakerPlugin_DBUS(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
