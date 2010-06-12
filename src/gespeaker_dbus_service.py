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
import dbus.glib
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
    self.gespeakerUI.proxy['ui.hide']()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui')
  def show(self):
    "Show the window"
    self.gespeakerUI.proxy['ui.show']()

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.ui', in_signature='s')
  def play_text(self, text):
    "Replace the current text and play it"
    self.gespeakerUI.proxy['text.set'](text, 0)
    self.gespeakerUI.proxy['espeak.stop'](None, None)
    self.gespeakerUI.proxy['espeak.play'](None, None)

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
    if value in range(0, 101):
      self.gespeakerUI.hscDelay.set_value(delay)
      return True
    else:
      return False
