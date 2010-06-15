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

NAME = 'Debug'
VERSION = '0.1'
AUTHOR = 'Fabio Castelli'
DESCRIPTION = 'Debug interface plugin'

from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Debug(GespeakerPlugin):
  def __init__(self, name, version, description, author):
    "Module initialization"
    GespeakerPlugin.__init__(self, name, version, description, author)
    self.logger('__init__("%s", "%s", "%s", "%s")' % (
      NAME, VERSION, AUTHOR, DESCRIPTION))

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
    self.logger('uiready(%s)' % ui)

plugin = GespeakerPlugin_Debug(NAME, VERSION, DESCRIPTION, AUTHOR)
register_plugin(NAME, plugin)
