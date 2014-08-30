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

import dbus
import dbus.service

class GespeakerDBUSServiceText(dbus.service.Object):
  "Class for text handling"
  def __init__(self, gespeakerUI):
    self.gespeakerUI = gespeakerUI
    bus_name = dbus.service.BusName('org.gtk.gespeaker', bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, bus_name, '/org/gtk/gespeaker/text')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text', in_signature='s')
  def replace(self, text):
    "Replace the current text"
    self.gespeakerUI.proxy['text.set'](text, 0)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text', in_signature='s')
  def insert(self, text):
    "Insert the specified text at the cursor"
    self.gespeakerUI.proxy['text.set'](text, 1)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text', in_signature='s')
  def prepend(self, text):
    "Insert the specified text at the begin"
    self.gespeakerUI.proxy['text.set'](text, 2)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text', in_signature='s')
  def append(self, text):
    "Insert the specified text at the end"
    self.gespeakerUI.proxy['text.set'](text, 3)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text')
  def clear(self):
    "Clear the text"
    self.gespeakerUI.proxy['ui.new'](None, False)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text')
  def cut(self):
    "Cut selected text"
    return self.gespeakerUI.proxy['text.cut'](None, None)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text')
  def copy(self):
    "Copy selected text"
    return self.gespeakerUI.proxy['text.copy'](None, None)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.text')
  def paste(self):
    "Paste text from the clipboard"
    return self.gespeakerUI.proxy['text.paste'](None, None)
