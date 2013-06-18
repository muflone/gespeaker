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

import dbus
import dbus.service
import handlepaths

class GespeakerDBUSService(dbus.service.Object):
  "Class for general information"
  def __init__(self, gespeakerUI):
    self.gespeakerUI = gespeakerUI
    bus_name = dbus.service.BusName('org.gtk.gespeaker', bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, bus_name, '/org/gtk/gespeaker')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker', out_signature='s')
  def get_version(self):
    "Return the current version"
    return handlepaths.APP_VERSION
    
  @dbus.service.method(dbus_interface='org.gtk.gespeaker', out_signature='s')
  def get_tempfilename(self):
    "Return the temporary filename"
    return self.gespeakerUI.tempFilename

  @dbus.service.method(dbus_interface='org.gtk.gespeaker', out_signature='i')
  def ping(self):
    "Return always 1"
    return 1
