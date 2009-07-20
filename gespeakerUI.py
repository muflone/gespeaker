##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

# No more used
# import TempfileWrapper
import tempfile
import os
from gettext import gettext as _

from DialogYesNo import DialogYesNo
from DialogFileOpenSave import DialogFileOpen, DialogFileSave
from DialogSimpleMessages import *
from DialogAbout import DialogAbout
from EspeakFrontend import EspeakFrontend
import PreferencesWindow
import Settings
from pygtkutils import *

class gespeakerUI(object):
  def __init__(self, app_name, app_title, app_version):
    print 'starting %s' % app_name
    self.espeak = EspeakFrontend()
    # Create temporary filename
    self.tempFilename = tempfile.mkstemp(prefix=app_name)[1]
    gladeUI = 'gespeaker.glade'
    self.app_name = app_name
    self.app_title = app_title
    self.app_version = app_version
    self.timeoutCheck = None
    self.recordToFile = None
    self.variants = ((), ())
    print 'loading interface from %s' % gladeUI
    self.gladeFile = gtk.glade.XML(fname=gladeUI, domain=self.app_name)
    # Signals handler
    signals = {
      'on_imgmenuFileQuit_activate': self.on_imgmenuFileQuit_activate,
      'on_imgmenuEditPlay_activate': self.on_imgmenuEditPlay_activate,
      'on_imgmenuFileNew_activate': self.on_imgmenuFileNew_activate,
      'on_imgmenuFileOpen_activate': self.on_imgmenuFileOpen_activate,
      'on_imgmenuFileSaveAs_activate': self.on_imgmenuFileSaveAs_activate,
      'on_imgmenuEditStop_activate': self.on_imgmenuEditStop_activate,
      'on_btnPlayStop_toggled': self.on_btnPlayStop_toggled,
      'on_btnPause_toggled': self.on_btnPause_toggled,
      'on_tlbRecord_toggled': self.on_tlbRecord_toggled,
      'on_imgmenuEditPause_activate': self.on_imgmenuEditPause_activate,
      'on_imgmenuEditRec_activate': self.on_imgmenuEditRec_activate,
      'on_imgmenuEditResetSettings_activate': self.on_imgmenuEditResetSettings_activate,
      'on_imgmenuHelpAbout_activate': self.on_imgmenuHelpAbout_activate,
      'on_imgmenuEditPreferences_activate': self.on_imgmenuEditPreferences_activate,
      'on_radioVoice_toggled': self.on_radioVoice_toggled,
      'on_cboLanguages_changed': self.on_cboLanguages_changed
    }
    self.gladeFile.signal_autoconnect(signals)
    # Load user settings
    Settings.load()
    # Load window and controls
    self.loadControls()
    self.loadSettings(True)
    self.winMain.show()
    
    # Play welcome message if PlayWelcomeText is set
    if Settings.get('PlayWelcomeText'):
      if Settings.get('UseCustomWelcome'):
        # Play customized welcome message
        self.txvBuffer.set_text(Settings.get('WelcomeText'))
      else:
        # Play default welcome message
        self.txvBuffer.set_text(Settings.default('WelcomeText'))
      self.btnPlayStop.set_active(True)
    gtk.main()
  
  def loadControls(self):
    "Load controls and other values"
    # Load controls from gladeFile
    print 'loading controls from UI'
    gw = self.gladeFile.get_widget
    self.winMain = gw('winMain')
    self.winMain.set_title(self.app_title)
    self.winMain.set_icon_from_file(Settings.iconLogo)
    
    self.txvText = gw('txvText')
    self.txvBuffer = self.txvText.get_buffer()
    self.winMain.set_focus(self.txvText)
    self.expSettings = gw('expSettings')
    self.hscVolume = gw('hscVolume')
    self.hscPitch = gw('hscPitch')
    self.hscSpeed = gw('hscSpeed')
    self.hscDelay = gw('hscDelay')
    self.lblVoice = gw('lblVoice')
    self.radioVoiceMale = gw('radioVoiceMale')
    self.radioVoiceFemale = gw('radioVoiceFemale')
    self.cboLanguages = gw('cboLanguages')
    self.lblVariants = gw('lblVariants')
    self.cboVariants = gw('cboVariants')
    self.imgmenuEditPlay = gw('imgmenuEditPlay')
    self.imgmenuEditStop = gw('imgmenuEditStop')
    self.imgmenuEditRec = gw('imgmenuEditRec')
    self.tlbStop = gw('tlbStop')
    self.btnPlayStop = gw('btnPlayStop')
    self.btnPause = gw('btnPause')
    self.tlbRecord = gw('tlbRecord')
    self.stbStatus = gw('stbStatus')
    self.statusContextId = self.stbStatus.get_context_id(self.app_name)
    self.imgmenuEditPause = gw('imgmenuEditPause')
    self.imgMbrola = gw('imgMbrola')
    # Create model for cboLanguages by (language, shortname, mbrola)
    self.listLanguages = gtk.ListStore(str, str, bool)
    self.cboLanguages.set_model(self.listLanguages)
    cell = gtk.CellRendererText()
    self.cboLanguages.pack_start(cell, True)
    self.cboLanguages.add_attribute(cell, 'text', 0)
    # Load languages list from espeak --voices
    for langs in self.espeak.loadLanguages(Settings.cmdEspeak):
      lang = langs[22:52].rsplit(None, 1)
      self.listLanguages.append(lang + [False])
    # Load mbrola voices if mbrola is available
    if self.espeak.mbrolaExists(Settings.cmdMbrola):
      for lang in self.espeak.loadMbrolaVoices(Settings.get('VoicesmbPath')):
        if lang[2]:
          self.listLanguages.append(lang)
    self.listLanguages.set_sort_column_id(0, gtk.SORT_ASCENDING)
    # Select default voice
    self.defaultLanguageIndex = 0
    defaultLanguage = _('default language')
    if defaultLanguage == 'default language':
      defaultLanguage = 'default'
    self.defaultLanguageIndex = TreeModel_find_text(
      self.listLanguages, 0, defaultLanguage)
    # Prepare sorted model for voice variants
    self.listVariants = gtk.ListStore(str, str)
    self.listVariants.set_sort_column_id(0, gtk.SORT_ASCENDING)
    self.cboVariants.set_model(self.listVariants)
    cell = gtk.CellRendererText()
    self.cboVariants.pack_start(cell, True)
    self.cboVariants.add_attribute(cell, 'text', 1)
    # Restore window size
    if Settings.get('SaveWindowSize'):
      self.winMain.set_default_size(
        Settings.get('MainWindowWidth'),
        Settings.get('MainWindowHeight')
      )
    else:
      self.winMain.set_default_size(
        Settings.default('MainWindowWidth'),
        Settings.default('MainWindowHeight')
      )
    self.expSettings.set_expanded(Settings.get('SettingsExpander'))

  def loadSettings(self, loadEverything):
    if loadEverything:
      # Restore voice settings
      self.hscVolume.set_value(Settings.get('VoiceVolume'))
      self.hscPitch.set_value(Settings.get('VoicePitch'))
      self.hscSpeed.set_value(Settings.get('VoiceSpeed'))
      self.hscDelay.set_value(Settings.get('VoiceDelay'))
      if Settings.get('VoiceTypeMale'):
        self.radioVoiceMale.set_active(True)
      else:
        self.radioVoiceFemale.set_active(True)
      # Sets default language
      language = Settings.get('VoiceLanguage')
      languageIndex = TreeModel_find_text(self.listLanguages, 0, language)
      if not ComboBox_set_item_from_text(self.cboLanguages, 0, language):
        self.cboLanguages.set_active(self.defaultLanguageIndex)
      Settings.set('VoiceLanguage', self.listLanguages[self.cboLanguages.get_active()][1])
    # Load standard settings
    self.txvText.set_wrap_mode(
      Settings.get('WordWrap') and gtk.WRAP_WORD or gtk.WRAP_NONE)
    players = ('aplay', 'paplay', '', Settings.get('PlayCommand'))
    self.cmdPlayer = players[Settings.get('PlayMethod')]
    # Load voice variants
    if Settings.get('LoadVariants'):
      self.variants = self.espeak.loadVariants(Settings.cmdEspeak)
      self.lblVariants.show()
      self.cboVariants.show()
    else:
      self.variants = ((), ())
      self.lblVariants.hide()
      self.cboVariants.hide()
    # Reload list
    voicebutton = Radio_get_active(self.radioVoiceMale.get_group())
    self.on_radioVoice_toggled(voicebutton, None)

  def on_imgmenuFileQuit_activate(self, widget, data=None):
    "Close the program"
    print 'quitting'
    if self.tempFilename and os.path.exists(self.tempFilename):
      os.remove(self.tempFilename)
    # Save window size if SaveWindowSize is set
    if Settings.get('SaveWindowSize'):
      sizes = self.winMain.get_size()
      Settings.set('MainWindowWidth', sizes[0])
      Settings.set('MainWindowHeight', sizes[1])
      Settings.set('SettingsExpander', self.expSettings.get_expanded())
    # Save voice settings if SaveVoiceSettings is set
    if Settings.get('SaveVoiceSettings'):
      Settings.set('VoiceVolume', int(self.hscVolume.get_value()))
      Settings.set('VoicePitch', int(self.hscPitch.get_value()))
      Settings.set('VoiceSpeed', int(self.hscSpeed.get_value()))
      Settings.set('VoiceDelay', int(self.hscDelay.get_value()))
      Settings.set('VoiceTypeMale', self.radioVoiceMale.get_active())
      # Save language only if different from defaultLanguageIndex
      language = ComboBox_get_text(self.cboLanguages, 0)
      language = self.listLanguages[self.cboLanguages.get_active()][0]
      Settings.set('VoiceLanguage', language)
    # Save settings
    print 'saving settings'
    Settings.save(clearDefaults=True)
    gtk.main_quit()
    return 0
  
  def on_imgmenuEditPlay_activate(self, widget, data=None):
    "Press button to start play, indirect cause button style"
    self.btnPlayStop.set_active(True)
  
  def on_imgmenuFileNew_activate(self, widget, data=None):
    "Clears the whole text"
    if TextBuffer_get_text(self.txvBuffer):
      dialog = DialogYesNo(
        message=_('Do you want to delete the current text?'), 
        default_button=gtk.RESPONSE_NO
      )
      dialog.set_icon_from_file(Settings.iconLogo)
      dialog.show()
      if dialog.responseIsYes():
        self.txvBuffer.set_text('')
        print 'text cleared'
  
  def on_imgmenuFileOpen_activate(self, widget, data=None):
    "Loads an external file"
    dialog = DialogFileOpen(
      title=_('Please select the text file to open'),
      initialDir=os.path.expanduser('~'))
    dialog.set_icon_from_file(Settings.iconLogo)
    dialog.addFilter(_('Text files (*.txt)'), ['*.txt'], None)
    dialog.addFilter(_('All files'), ['*'], None)
    if dialog.show():
      file = None
      try:
        file = open(dialog.filename, 'r')
        self.txvBuffer.set_text(file.read())
        print 'loading text from %s' % dialog.filename
      except IOError, (errno, strerror):
        ShowDialogError(
          text=_('Error opening the file') + '\n\n%s' % strerror,
          showOk=True
        )
        print 'unable to load %s (I/O error %s: %s)' % (
          dialog.filename, errno, strerror
        )
      except:
        ShowDialogError(text=_('Error opening the file'), showOk=True)
        print 'error loading %s' % dialog.filename
      if file:
        file.close()
  
  def on_imgmenuFileSaveAs_activate(self, widget, data=None):
    "Saves the whole text in the specified filename"
    dialog = DialogFileSave(
      title=_('Please select where to save the text file'),
      initialDir=os.path.expanduser('~'))
    txtFilter = _('Text files (*.txt)')
    dialog.addFilter(txtFilter, ['*.txt'], None)
    dialog.addFilter(_('All files'), ['*'], None)
    dialog.set_icon_from_file(Settings.iconLogo)
    if dialog.show():
      filename = dialog.filename
      if dialog.lastFilter.get_name() == txtFilter and filename[-4:] != '.txt':
        filename += '.txt'
      print 'saving text in %s' % filename
      file = None
      try:
        file = open(filename, 'w')
        file.write(TextBuffer_get_text(self.txvBuffer))
        print 'file %s saved' % filename
      except IOError, (errno, strerror):
        ShowDialogError(
          text=_('Error saving the file') + '\n\n%s' % strerror,
          showOk=True
        )
        print 'unable to save %s (I/O error %s: %s)' % (
          filename, errno, strerror
        )
      except:
        ShowDialogError(text=_('Error saving the file'), showOk=True)
        print 'error saving %s' % filename
      if file:
        file.close()

  def on_imgmenuEditResetSettings_activate(self, widget, data=None):
    "Restore default settings"
    dialog = DialogYesNo(
      message=_('Do you want to reset the default settings?'),
      default_button=gtk.RESPONSE_NO
    )
    dialog.set_icon_from_file(Settings.iconLogo)
    dialog.show()
    if dialog.responseIsYes():
      if self.defaultLanguageIndex:
        self.cboLanguages.set_active(self.defaultLanguageIndex)
      print 'restored default settings'
      if os.path.exists(Settings.conffile):
        os.remove(Settings.conffile)
        print 'removed user settings file: %s' % Settings.conffile
      # Reload default settings
      Settings.load()
      self.loadSettings(True)

  def on_imgmenuHelpAbout_activate(self, widget, data=None):
    "Show the about dialog"
    print 'show about dialog'
    DialogAbout(
      name=self.app_title,
      version=self.app_version,
      comment=_('A GTK frontend for espeak'),
      copyright='Copyright 2009 Muflone',
      license=file('copyright', 'r').read(), 
      website='http://ubuntrucchi.wordpress.com/',
      website_label='Ubuntu Trucchi',
      authors=['Muflone <muflone@vbsimple.net>'],
      translation=_('translation'), 
      logo=Settings.iconLogo,
      icon=Settings.iconLogo
    )

  def on_imgmenuEditStop_activate(self, widget, data=None):
    "Press button to stop play, indirect cause button style"
    self.btnPlayStop.set_active(False)

  def on_imgmenuEditPause_activate(self, widget, data=None):
    "Press button to pause or continue"
    self.btnPause.set_active(not self.btnPause.get_active())

  def on_imgmenuEditRec_activate(self, widget, data=None):
    "Press button to record or disable recording"
    self.tlbRecord.set_active(not self.tlbRecord.get_active())
    
  def checkIfPlaying(self):
    "Check if a process is still running"
    if self.espeak.isPlaying():
      # Still running
      return True
    else:
      # Disable stop buttons on menu and toolbar
      self.btnPlayStop.set_active(False)
      return False

  def setStopCheck(self, active):
    "Set/unset timeout check for running processes"
    if active:
      self.timeoutCheck = gobject.timeout_add(500, self.checkIfPlaying)
    else:
      gobject.source_remove(self.timeoutCheck)
      self.timeoutCheck = None

  def on_btnPlayStop_toggled(self, widget, data=None):
    "Play and stop by pressing and releasing the button"
    if self.btnPlayStop.get_active() and TextBuffer_get_text(self.txvBuffer):
      # Button active so we have to start to play
      self.startPlaying()
    elif self.btnPlayStop.get_active():
      self.btnPlayStop.set_active(False)
    elif TextBuffer_get_text(self.txvBuffer):
      # If Pause button is active then we have to continue before to kill
      if self.btnPause.get_active():
        self.btnPause.set_active(False)
      # Button inactive so we have to stop the playing
      self.stopPlaying()

  def on_btnPause_toggled(self, widget, data=None):
    "Pause and unpause espeak and player by signals STOP/CONT"
    self.espeak.pauseOrResume(self.btnPause.get_active())

  def startPlaying(self):
    "Play whole text"
    self.playText(TextBuffer_get_text(self.txvBuffer))

  def playText(self, text):
    if text:
      # Save buffer text on temporary filename and play it
      tmpFile = open(self.tempFilename, mode='w')
      tmpFile.write(text)
      tmpFile.close()
      # Replace espeak's arguments with dialog values
      language = self.listLanguages[self.cboLanguages.get_active()][1]
      isMbrola = self.listLanguages[self.cboLanguages.get_active()][2]
      # Apply variant and voice to non-mbrola voices
      if not isMbrola:
        # Choose voice variant
        if self.cboVariants.get_active() == 0:
          # Default voice
          if self.radioVoiceFemale.get_active():
            language += '+12'
        else:
          language += '+%s' % self.listVariants[self.cboVariants.get_active()][0]
      args = {
        '%v': str(int(self.hscVolume.get_value())), 
        '%p': str(int(self.hscPitch.get_value())),
        '%s': str(int(self.hscSpeed.get_value())),
        '%d': str(int(self.hscDelay.get_value())),
        '%l': language,
        '%f': self.tempFilename
      }
      cmd = [Settings.cmdEspeak] + [
        args.get(p, p) for p in Settings.argsEspeak.split()]
      # Enable stop buttons on menu and toolbar
      self.imgmenuEditPlay.set_sensitive(False)
      self.imgmenuEditStop.set_sensitive(True)
      self.imgmenuEditPause.set_sensitive(True)
      self.imgmenuEditRec.set_sensitive(False)
      self.btnPause.set_sensitive(True)
      self.btnPlayStop.set_label('gtk-media-stop')
      self.tlbRecord.set_sensitive(False)
      if not isMbrola:
        self.espeak.play(cmd, self.cmdPlayer, self.recordToFile)
      else:
        args = {
          '%l': '%s/%s' % (
            Settings.get('VoicesmbPath'), 
            language.replace('mb-', '', 1))
        }
        cmdMbrola = [Settings.cmdMbrola] + [
          args.get(p, p) for p in Settings.argsMbrola.split()]
        self.espeak.playMbrola(cmd, self.cmdPlayer, cmdMbrola, self.recordToFile)
      # Enable check for running processes
      self.setStopCheck(True)

  def stopPlaying(self):
    self.espeak.stop()
    # Disable buttons and menus
    self.setStopCheck(False)
    self.imgmenuEditPlay.set_sensitive(True)
    self.imgmenuEditStop.set_sensitive(False)
    self.imgmenuEditPause.set_sensitive(False)
    self.imgmenuEditRec.set_sensitive(True)
    self.btnPause.set_sensitive(False)
    self.btnPlayStop.set_label('gtk-media-play')
    if Settings.get('SingleRecord'):
      self.tlbRecord.set_active(False)
    self.tlbRecord.set_sensitive(True)

  def on_imgmenuEditPreferences_activate(self, widget, data=None):
    "Show preferences dialog"
    prefsUI = 'preferences.glade'
    gladePrefs = gtk.glade.XML(fname=prefsUI, domain=self.app_name)
    PreferencesWindow.showPreferencesWindow(gladePrefs, self.espeak)
    self.loadSettings(False)

  def on_tlbRecord_toggled(self, widget, data=None):
    self.recordToFile = None
    if self.tlbRecord.get_active():
      dialog = DialogFileSave(
        title=_('Please select where to save the recorded file'),
        initialDir=os.path.expanduser('~'))
      dialog.set_icon_from_file(Settings.iconLogo)
      dialog.addFilter(_('Wave files (*.wav)'), ['*.wav'], None)
      dialog.addFilter(_('All files'), ['*'], None)
      if dialog.show():
        filename = dialog.filename
        if filename[-4:] != '.wav':
          filename += '.wav'
        print 'record to %s' % filename
        self.recordToFile = filename
        self.stbStatus.push(self.statusContextId, 
          _('Recording audio track to: %s' % self.recordToFile))
      else:
        self.tlbRecord.set_active(False)
      dialog.destroy()
    else:
      self.stbStatus.pop(self.statusContextId)

  def on_radioVoice_toggled(self, widget, data=None):
    "Assign variants after voice type change"
    if widget.get_active():
      self.listVariants.clear()
      self.listVariants.append(None)
      for v in self.variants[widget is self.radioVoiceFemale and 1 or 0]:
        self.listVariants.append(v)
      self.cboVariants.set_active(0)

  def on_cboLanguages_changed(self, widget, data=None):
    "Check if a mbrola voice has been selected"
    status = self.listLanguages[self.cboLanguages.get_active()][2]
    self.imgMbrola.set_from_stock(size=gtk.ICON_SIZE_BUTTON,
      stock_id=status and gtk.STOCK_YES or gtk.STOCK_NO)
    self.lblVoice.set_sensitive(not status)
    self.radioVoiceMale.set_sensitive(not status)
    self.radioVoiceFemale.set_sensitive(not status)
    self.lblVariants.set_sensitive(not status)
    self.cboVariants.set_sensitive(not status)
