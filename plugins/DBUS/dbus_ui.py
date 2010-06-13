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

class GespeakerDBUSServiceUI(dbus.service.Object):
  "Class for UI handling"
  def __init__(self, gespeakerUI):
    self.gespeakerUI = gespeakerUI
    bus_name = dbus.service.BusName('org.gtk.gespeaker', bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, bus_name, '/org/gtk/gespeaker/ui')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='b')
  def new(self, confirm=True):
    "Clear the text with the confirm if requested"
    self.gespeakerUI.proxy['ui.new'](None, confirm)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def open(self, filename=None):
    "Open a text file with the dialog if filename was not provided"
    self.gespeakerUI.proxy['ui.open'](None, filename)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def save(self, filename=None):
    "Save the current text in a text file with the dialog if filename was not provided"
    self.gespeakerUI.proxy['ui.save'](None, filename)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def record(self, filename=None):
    "Record the voice in a wave file with dialog if filename was not provided"
    return self.gespeakerUI.proxy['ui.record'](None, filename)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui')
  def unrecord(self):
    "Disable recording"
    return self.gespeakerUI.proxy['ui.unrecord']()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='b')
  def reset(self, confirm=True):
    "Reset the default settings with confirm if requested"
    self.gespeakerUI.proxy['ui.reset'](None, confirm)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui')
  def quit(self):
    "Close the application"
    self.gespeakerUI.proxy['ui.quit'](None, None)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui')
  def hide(self):
    "Hide the window"
    self.gespeakerUI.proxy['ui.set_window']('hide')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='i', out_signature='s')
  def set_opacity(self, opacity):
    "Set window opacity"
    return self.gespeakerUI.proxy['ui.set_window']('set-opacity', opacity)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def set_position(self, position):
    "Set the window position"
    return self.gespeakerUI.proxy['ui.set_position'](position)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def set_size(self, size):
    "Set the window size"
    return self.gespeakerUI.proxy['ui.set_size'](size)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s', out_signature='s')
  def set_window(self, action):
    "Show the window"
    return self.gespeakerUI.proxy['ui.set_window'](action)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui')
  def show(self):
    "Show the window"
    self.gespeakerUI.proxy['ui.set_window']('show')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def play_text(self, text):
    "Replace the current text and play it"
    self.gespeakerUI.proxy['text.set'](text, 0)
    self.gespeakerUI.proxy['espeak.stop'](None, None)
    self.gespeakerUI.proxy['espeak.play'](None, None)
