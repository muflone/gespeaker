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

  @dbus.service.method(dbus_interface='org.gtk.gespeaker', out_signature='s', sender_keyword='sender')
  def get_version(self, sender):
    "Return the current version"
    return sender
    
  @dbus.service.method(dbus_interface='org.gtk.gespeaker', out_signature='s')
  def get_tempfile(self):
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

  @dbus.service.method(dbus_interface='org.gtk.gespeaker.voice')
  def play(self):
    "Play the current text"
    self.gespeakerUI.proxy['do_play'](None, None)
