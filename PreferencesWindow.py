import gtk
import Settings
import SubprocessWrapper
import os.path
from gettext import gettext as _
from DialogSimpleMessages import ShowDialogError
from pygtkutils import *

def showPreferencesWindow(gladeFile, iconLogo):
  prefsWindow = PreferencesWindow(gladeFile, iconLogo)

class PreferencesWindow(object):
  def __init__(self, gladeFile, iconLogo):
    self.gladeFile = gladeFile
    self.loadControls()
    self.dlgPrefs.set_icon_from_file(iconLogo)
    signals = {
      'on_cboPlayer_changed': self.on_cboPlayer_changed,
      'on_btnPlayerTest_clicked': self.on_btnPlayerTest_clicked,
      'on_chkCustomWelcome_toggled': self.on_chkCustomWelcome_toggled,
      'on_btnOk_clicked': self.on_btnOk_clicked
    }
    self.gladeFile.signal_autoconnect(signals)
    # Load settings
    self.cboPlayer.set_active(Settings.get('PlayMethod'))
    self.txtPlayerCommand.set_text(Settings.get('PlayCommand'))
    self.chkPlayWelcome.set_active(Settings.get('PlayWelcomeText') == True)
    self.chkCustomWelcome.set_active(Settings.get('UseCustomWelcome') == True)
    self.txtWelcomeText.set_text(Settings.get('WelcomeText'))
    self.chkSaveVoice.set_active(Settings.get('SaveVoiceSettings') == True)
    self.chkSaveSize.set_active(Settings.get('SaveWindowSize') == True)
    self.chkSingleRecord.set_active(Settings.get('SingleRecord') == True)
    self.chkWordWrap.set_active(Settings.get('WordWrap') == True)
    self.chkLoadVariants.set_active(Settings.get('LoadVariants') == True)
    # Before to use the window property the realize method must be called
    self.dlgPrefs.realize()
    # Change WM buttons making the window only movable with the closing button
    self.dlgPrefs.window.set_functions(gtk.gdk.FUNC_CLOSE | gtk.gdk.FUNC_MOVE)
    self.dlgPrefs.run()
    self.dlgPrefs.destroy()

  def loadControls(self):
    def separator_filter(model, iter, data=None):
      return model.get_value(iter, 2)
    gw = self.gladeFile.get_widget
    self.dlgPrefs = gw('dlgPreferences')
    self.cboPlayer = gw('cboPlayer')
    self.lblPlayerCommand = gw('lblPlayerCommand')
    self.txtPlayerCommand = gw('txtPlayerCommand')
    self.btnPlayerTest = gw('btnPlayerTest')
    self.chkPlayWelcome = gw('chkPlayWelcome')
    self.chkCustomWelcome = gw('chkCustomWelcome')
    self.lblCustomWelcome = gw('lblCustomWelcome')
    self.txtWelcomeText = gw('txtWelcomeText')
    self.chkSaveVoice = gw('chkSaveVoice')
    self.chkSaveSize = gw('chkSaveSize')
    self.chkSingleRecord = gw('chkRecordSingleTrack')
    self.chkWordWrap = gw('chkWordWrap')
    self.chkLoadVariants = gw('chkLoadVariants')
    self.btnOk = gw('btnOk')
    # Prepare model for players combo
    listStore = gtk.ListStore(gtk.gdk.Pixbuf, str, bool)
    self.cboPlayer.set_model(listStore)
    # First is image
    cell = gtk.CellRendererPixbuf()
    self.cboPlayer.pack_start(cell, False)
    self.cboPlayer.add_attribute(cell, 'pixbuf', 0)
    # Second is text
    cell = gtk.CellRendererText()
    self.cboPlayer.pack_start(cell, False)
    self.cboPlayer.add_attribute(cell, 'text', 1)
    self.cboPlayer.set_row_separator_func(separator_filter)
    # Load icons and text for methods
    listStore.append([Pixbuf_load_file(
      os.path.join(os.path.dirname(__file__), 'alsalogo.png'), (24, 24)), 
      _('ALSA - Advanced Linux Sound Architecture'), False])
    listStore.append([Pixbuf_load_file(
      os.path.join(os.path.dirname(__file__), 'palogo.png'), (24, 24)), 
      _('PulseAudio sound server'), False])
    listStore.append([None, '_', True])
    listStore.append([None, _('Custom sound application'), False])
    # Change testing button caption
    Button_change_stock_description(self.btnPlayerTest, _('_Test'), True)

  def on_chkCustomWelcome_toggled(self, widget, data=None):
    self.lblCustomWelcome.set_sensitive(self.chkCustomWelcome.get_active())
    self.txtWelcomeText.set_sensitive(self.chkCustomWelcome.get_active())

  def on_btnOk_clicked(self, widget, data=None):
    "Apply settings"
    Settings.set('PlayMethod', self.cboPlayer.get_active())
    Settings.set('PlayCommand', self.txtPlayerCommand.get_text())
    Settings.set('PlayWelcomeText', self.chkPlayWelcome.get_active())
    Settings.set('UseCustomWelcome', self.chkCustomWelcome.get_active())
    Settings.set('WelcomeText', self.txtWelcomeText.get_text())
    Settings.set('SaveVoiceSettings', self.chkSaveVoice.get_active())
    Settings.set('SaveWindowSize', self.chkSaveSize.get_active())
    Settings.set('SingleRecord', self.chkSingleRecord.get_active())
    Settings.set('WordWrap', self.chkWordWrap.get_active())
    Settings.set('LoadVariants', self.chkLoadVariants.get_active())

  def on_cboPlayer_changed(self, widget, data=None):
    "Enable and disable controls if custom command is not set"
    active = self.cboPlayer.get_active()
    text = self.txtPlayerCommand.get_text()
    self.lblPlayerCommand.set_sensitive(active == 3)
    self.txtPlayerCommand.set_sensitive(active == 3)
    self.btnOk.set_sensitive((active != 3) or bool(text))
    self.btnPlayerTest.set_sensitive((active != 3) or bool(text))

  def on_btnPlayerTest_clicked(self, widget, data=None):
    "Test selected player with testing.wav"
    # Set waiting cursor
    Window_change_cursor(self.dlgPrefs.window, gtk.gdk.WATCH, True)
    players = ('aplay', 'paplay', '', self.txtPlayerCommand.get_text())
    filename = os.path.join(os.path.dirname(__file__), 'testing.wav')
    test = SubprocessWrapper.Popen(['cat', filename], 
      stdout=SubprocessWrapper.PIPE)
    play = None
    try:
      # Try to play with pipe
      play = SubprocessWrapper.Popen(players[self.cboPlayer.get_active()], 
        stdin=test.stdout,
        stdout=SubprocessWrapper.PIPE,
        stderr=SubprocessWrapper.PIPE)
      play.communicate()
    except OSError, (errno, strerror):
      # Error during communicate"
      ShowDialogError(title=_('Audio testing'), showOk=True,
        text=_('There was an error during the test for the audio player.\n'
          'Error %s: %s' % (errno, strerror)))
    # Terminate test if it's still running, follows a broken pipe error
    if test.poll() is None:
      test.terminate()
    # Restore default cursor
    Window_change_cursor(self.dlgPrefs.window, None, False)
