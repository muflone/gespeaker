##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2013 Fabio Castelli
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

import gtk.gdk
import os
import handlepaths
import ConfigParser
import Settings

ICON_WIDTH = 48
ICON_HEIGHT = 48

plugins = {}
config = None

def register_plugin(name, plugin_class):
  "Register a new plugin"
  global plugins
  plugins[name] = plugin_class

def signal_proxy(signal, argc=0, args=None):
  "Call a signal by its name"
  for plugin in plugins.itervalues():
    if hasattr(plugin, signal):
      method = getattr(plugin, signal)
      if method and plugin.active:
        if argc==1:
          method(args)
        elif argc==0:
          method()

def loadPluginsSettings():
  "Load plugins from the configuration file"
  global config
  config = ConfigParser.RawConfigParser()
  if os.path.exists(Settings.pluginsfile):
    config.read(Settings.pluginsfile)

class GespeakerPlugin(object):
  def __init__(self, name, version, description, author, icon='', website=''):
    "Module initialization"
    self.name = name
    self.version = version
    self.description = description
    self.author = author
    self.icon = icon
    self.website = website
    self.logger('init plugin v.%s' % version)
    self.active = True

  def load(self):
    "Plugin load"
    pass

  def unload(self):
    "Plugin unload"
    pass

  def reload(self):
    "Plugin reload"
    self.unload()
    self.load()

  def configure(self):
    "Plugin custom configuration"
    pass

  def update_ui(self):
    "Update UI for changes"
    pass

  def enable(self):
    "Enable the disabled plugin"
    self.active = True

  def disable(self):
    "Disable the plugin"
    self.active = False

  def logger(self, message):
    "Print a message from a plugin"
    print '[%s]: %s' % (self.name, message)

  def render_icon(self):
    filename = self.icon.replace('$icons', handlepaths.getPath('icons'))
    if not filename or not os.path.exists(filename):
      filename = handlepaths.getPath('icons', 'generic-plugin.png')
    return gtk.gdk.pixbuf_new_from_file_at_size(filename, 
      ICON_WIDTH, ICON_HEIGHT)
