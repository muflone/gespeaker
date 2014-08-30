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

PLUGIN_NAME = 'Debug'
PLUGIN_VERSION = '0.2'
PLUGIN_DESCRIPTION = 'Debug interface'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = ''

from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Debug(GespeakerPlugin):
  def __init__(self, name, version, description, author, icon, website):
    "Module initialization"
    GespeakerPlugin.__init__(self, name, version, description, author, icon, website)
    self.logger('__init__("%s", "%s", "%s", "%s", "%s", "%s")' % (
      PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_AUTHOR, PLUGIN_DESCRIPTION, 
      PLUGIN_ICON, PLUGIN_WEBSITE))

  def load(self):
    "Plugin load"
    GespeakerPlugin.load(self)
    self.logger('load()')
  
  def unload(self):
    "Plugin unload"
    GespeakerPlugin.unload(self)
    self.logger('unload()')
  
  def reload(self):
    "Plugin reload"
    GespeakerPlugin.reload(self)
    self.logger('reload()')

  def configure(self):
    "Plugin custom configuration"
    GespeakerPlugin.configure(self)
    self.logger('configure()')

  def update_ui(self):
    "Update UI for changes"
    GespeakerPlugin.update_ui(self)
    self.logger('update_ui()')
  
  def on_uiready(self, ui):
    self.logger('on_uiready(%s)' % ui)

  def on_closing(self):
    self.logger('on_closing()')

  def on_closed(self):
    self.logger('on_closed()')

  def on_shown(self):
    self.logger('on_shown()')

  def on_hidden(self):
    self.logger('on_hidden()')

  def on_terminate(self):
    self.logger('on_terminate()')

plugin = GespeakerPlugin_Debug(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
