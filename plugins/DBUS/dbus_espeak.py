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

import dbus
import dbus.service

class GespeakerDBUSServiceEspeak(dbus.service.Object):
  "Class for espeak engine"
  def __init__(self, gespeakerUI):
    self.gespeakerUI = gespeakerUI
    bus_name = dbus.service.BusName('org.gtk.gespeaker', bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, bus_name, '/org/gtk/gespeaker/espeak')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.espeak')
  def play(self):
    "Play the current text"
    self.gespeakerUI.proxy['espeak.play'](None, None)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.espeak')
  def stop(self):
    "Stop the current playing"
    self.gespeakerUI.proxy['espeak.stop'](None, None)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.espeak')
  def pause(self):
    "Pause/restore the current play"
    self.gespeakerUI.proxy['espeak.pause'](None, None)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.espeak', out_signature='b')
  def is_playing(self):
    "Return if espeak is actually playing"
    return self.gespeakerUI.proxy['espeak.is_playing']()
