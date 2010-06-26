#!/usr/bin/env python

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

import os
import sys
import gettext
import pkgutil
import imp
import gtk.glade
import gespeakerUI
import handlepaths
import Settings
import plugins

if __name__ == '__main__':
  for module in (gettext, gtk.glade):
    module.bindtextdomain(handlepaths.APP_NAME, handlepaths.getPath('locale'))
    module.textdomain(handlepaths.APP_NAME)

  # Load user settings
  plugins.loadPluginsSettings()
  Settings.load()

  print 'loading available plugins...'
  plugins_path = [handlepaths.getPath('plugins')]
  for loader, name, isPkg in pkgutil.iter_modules(plugins_path):
    file, pathname, description = imp.find_module(name, plugins_path)
    imp.load_module(name, file, pathname, description)
  
  main = gespeakerUI.gespeakerUI()
  plugins.signal_proxy('load')
  plugins.signal_proxy('on_uiready', argc=1, args=main)
  main.run()
  plugins.signal_proxy('on_closed')
  plugins.signal_proxy('unload')
  plugins.signal_proxy('on_terminate')
  # Save settings
  print 'saving settings'
  Settings.save(clearDefaults=True)
