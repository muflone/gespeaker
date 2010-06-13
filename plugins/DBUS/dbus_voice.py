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

class GespeakerDBUSServiceVoice(dbus.service.Object):
  "Class for voice settings"
  def __init__(self, gespeakerUI):
    self.gespeakerUI = gespeakerUI
    bus_name = dbus.service.BusName('org.gtk.gespeaker', bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, bus_name, '/org/gtk/gespeaker/voice')

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='as')
  def list_all_voices(self):
    "Return the list of available voices"
    return [language[0] for language in self.gespeakerUI.listLanguages]

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='as')
  def list_mbrola_voices(self):
    "Return the list of mbrola voices"
    mbrolaVoices = []
    for index in range(len(self.gespeakerUI.listLanguages)):
      if self.gespeakerUI.listLanguages[index][2]:
        mbrolaVoices.append(self.gespeakerUI.listLanguages[index][0])
    return mbrolaVoices

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='s')
  def get_voice_name(self, index):
    "Return the name of specified voice"
    return self.gespeakerUI.listLanguages[index][0]

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='s')
  def get_voice_short(self, index):
    "Return the short-name of specified voice"
    return self.gespeakerUI.listLanguages[index][1]

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='b')
  def get_voice_is_mbrola(self, index):
    "Return if the specified voice is mbrola"
    return self.gespeakerUI.listLanguages[index][2]

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='i')
  def get_voices_count(self):
    "Return the number of available voices"
    return len(self.gespeakerUI.listLanguages)

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='i')
  def get_voice(self):
    "Return the index of current voice"
    return self.gespeakerUI.cboLanguages.get_active()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='b')
  def set_voice(self, voice):
    "Set the current voice"
    if voice in range(0, self.get_voices_count()):
      self.gespeakerUI.cboLanguages.set_active(voice)
      return True
    else:
      return False

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='s', out_signature='b')
  def set_voice_by_name(self, voice):
    "Set the current voice by its name"
    voices = self.list_all_voices()
    if voice in voices:
      self.gespeakerUI.cboLanguages.set_active(voices.index(voice))
      return True
    else:
      return False

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='s')
  def get_voice_type(self):
    "Get the current voice type"
    if self.gespeakerUI.radioVoiceMale.get_property('sensitive'):
      return self.gespeakerUI.radioVoiceMale.get_active() and 'male' or 'female'
    else:
      return 'disabled'

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='s', out_signature='b')
  def set_voice_type(self, voice_type):
    "Set the current voice type"
    if voice_type in ('male', 'female') and \
    self.gespeakerUI.radioVoiceMale.get_property('sensitive'):
      if voice_type == 'male':
        self.gespeakerUI.radioVoiceMale.set_active(True)
      else:
        self.gespeakerUI.radioVoiceFemale.set_active(True)
      return True
    else:
      return False

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='i')
  def get_pitch(self):
    "Return the current pitch"
    return self.gespeakerUI.hscPitch.get_value()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='b')
  def set_pitch(self, pitch):
    "Set the current pitch"
    if pitch in range(0, 100):
      self.gespeakerUI.hscPitch.set_value(pitch)
      return True
    else:
      return False

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='i')
  def get_volume(self):
    "Return the current volume"
    return self.gespeakerUI.hscVolume.get_value()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='b')
  def set_volume(self, volume):
    "Set the current volume"
    if volume in range(0, 201):
      self.gespeakerUI.hscVolume.set_value(volume)
      return True
    else:
      return False

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='i')
  def get_speed(self):
    "Return the current speed"
    return self.gespeakerUI.hscSpeed.get_value()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='b')
  def set_speed(self, speed):
    "Set the current speed"
    if speed in range(80, 391):
      self.gespeakerUI.hscSpeed.set_value(speed)
      return True
    else:
      return False

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', out_signature='i')
  def get_delay(self):
    "Return the current delay"
    return self.gespeakerUI.hscDelay.get_value()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice', in_signature='i', out_signature='b')
  def set_delay(self, delay):
    "Set the current delay"
    if delay in range(0, 101):
      self.gespeakerUI.hscDelay.set_value(delay)
      return True
    else:
      return False
