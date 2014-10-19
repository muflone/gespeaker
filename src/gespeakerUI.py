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

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

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
import handlepaths
import plugins
from pygtkutils import *

COL_LANGUAGE, COL_NAME, COL_MBROLA = range(3)

class gespeakerUI(object):
  def __init__(self):
    print 'starting %s' % handlepaths.APP_NAME
    # Create temporary filename
    self.tempFilename = tempfile.mkstemp(prefix=handlepaths.APP_NAME)[1]
    self.timeoutCheck = None
    self.recordToFile = None
    self.recordToFileRequested = False
    # Proxy maps
    self.proxy = {
      'text.set': self.set_text,
      'text.cut': self.on_imgmenuEditCut_activate,
      'text.copy': self.on_imgmenuEditCopy_activate,
      'text.paste': self.on_imgmenuEditPaste_activate,
      'ui.new':  self.on_imgmenuFileNew_activate,
      'ui.open': self.on_imgmenuFileOpen_activate,
      'ui.save': self.on_imgmenuFileSaveAs_activate,
      'ui.record': self.on_imgmenuFileRec_activate,
      'ui.unrecord': self.disable_record,
      'ui.reset': self.on_imgmenuEditResetSettings_activate,
      'ui.quit': self.on_imgmenuFileQuit_activate,
      'ui.set_size': self.set_size,
      'ui.set_position': self.set_position,
      'ui.set_window': self.set_window,
      'espeak.play': self.on_imgmenuEditPlay_activate,
      'espeak.stop': self.on_imgmenuEditStop_activate,
      'espeak.pause': self.on_imgmenuEditPause_activate,
      'espeak.is_playing': self.checkIfPlaying,
    }
    # Signals handler
    signals = {
      'on_imgmenuEditPlay_activate': self.on_imgmenuEditPlay_activate,
      'on_imgmenuFileNew_activate': self.on_imgmenuFileNew_activate,
      'on_imgmenuFileOpen_activate': self.on_imgmenuFileOpen_activate,
      'on_imgmenuFileSaveAs_activate': self.on_imgmenuFileSaveAs_activate,
      'on_imgmenuEditStop_activate': self.on_imgmenuEditStop_activate,
      'on_btnPlayStop_toggled': self.on_btnPlayStop_toggled,
      'on_btnPause_toggled': self.on_btnPause_toggled,
      'on_tlbRecord_toggled': self.on_tlbRecord_toggled,
      'on_imgmenuEditPause_activate': self.on_imgmenuEditPause_activate,
      'on_imgmenuFileRec_activate': self.on_imgmenuFileRec_activate,
      'on_imgmenuEditResetSettings_activate': self.on_imgmenuEditResetSettings_activate,
      'on_imgmenuEditCut_activate': self.on_imgmenuEditCut_activate,
      'on_imgmenuEditCopy_activate': self.on_imgmenuEditCopy_activate,
      'on_imgmenuEditPaste_activate': self.on_imgmenuEditPaste_activate,
      'on_imgmenuHelpAbout_activate': self.on_imgmenuHelpAbout_activate,
      'on_imgmenuEditPreferences_activate': self.on_imgmenuEditPreferences_activate,
      'on_radioVoice_toggled': self.on_radioVoice_toggled,
    }
    # Load window and controls
    self.loadControls()
    self.loadSettings(True)
  
  def run(self):
    "Start main loop"
    self.proxy['ui.set_window']('show')
    gtk.main()
  
  def loadControls(self):
    "Load controls and other values"
    # Load controls from gladeFile
    print 'loading controls from UI'
    gw = self.gladeFile.get_widget
    self.winMain = gw('winMain')
    self.winMain.set_title(handlepaths.APP_TITLE)
    self.winMain.set_icon_from_file(handlepaths.get_app_logo())
    
    self.expSettings = gw('expSettings')
    self.hscVolume = gw('hscVolume')
    self.hscPitch = gw('hscPitch')
    self.hscSpeed = gw('hscSpeed')
    self.hscDelay = gw('hscDelay')
    self.lblVoice = gw('lblVoice')
    self.imgmenuEditPlay = gw('imgmenuEditPlay')
    self.imgmenuEditStop = gw('imgmenuEditStop')
    self.imgmenuFileRec = gw('imgmenuFileRec')
    self.tlbStop = gw('tlbStop')
    self.btnPlayStop = gw('btnPlayStop')
    self.btnPause = gw('btnPause')
    self.tlbRecord = gw('tlbRecord')
    self.stbStatus = gw('stbStatus')
    self.statusContextId = self.stbStatus.get_context_id(handlepaths.APP_NAME)
    self.imgmenuEditPause = gw('imgmenuEditPause')
    self.imgMbrola = gw('imgMbrola')
    # Select default voice
    self.defaultLanguageIndex = 0
    defaultLanguage = _('default language')
    if defaultLanguage == 'default language':
      defaultLanguage = 'default'
    self.defaultLanguageIndex = TreeModel_find_text(
      self.listLanguages, COL_LANGUAGE, defaultLanguage)
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
      languageIndex = TreeModel_find_text(self.listLanguages, COL_LANGUAGE, language)
      if not ComboBox_set_item_from_text(self.cboLanguages, 0, language):
        self.cboLanguages.set_active(self.defaultLanguageIndex)
      Settings.set('VoiceLanguage', self.listLanguages[self.cboLanguages.get_active()][COL_NAME])
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
    plugins.signal_proxy('on_closing')
    if self.tempFilename and os.path.exists(self.tempFilename):
      os.remove(self.tempFilename)
    gtk.main_quit()
    return 0
  
  def on_imgmenuEditPlay_activate(self, widget, data=None):
    "Press button to start play, indirect cause button style"
    self.btnPlayStop.set_active(True)
  
  def on_imgmenuFileNew_activate(self, widget, confirm=True):
    "Clears the whole text"
    if TextBuffer_get_text(self.txvBuffer):
      if confirm:
        dialog = DialogYesNo(
          message=_('Do you want to delete the current text?'), 
          default_button=gtk.RESPONSE_NO
        )
        dialog.set_icon_from_file(handlepaths.get_app_logo())
        dialog.show()
      # Clear if confirm was not requested or if the user gave response
      if not confirm or dialog.responseIsYes():
        self.txvBuffer.set_text('')
        print 'text cleared'
  
  def on_imgmenuFileOpen_activate(self, widget, filename=None):
    "Loads an external file"
    if not filename:
      # If filename was not provided show dialog
      dialog = DialogFileOpen(
        title=_('Please select the text file to open'),
        initialDir=os.path.expanduser('~'))
      dialog.set_icon_from_file(handlepaths.get_app_logo())
      dialog.addFilter(_('Text files (*.txt)'), ['*.txt'], None)
      dialog.addFilter(_('All files'), ['*'], None)
      if dialog.show():
        filename = dialog.filename
      dialog.destroy()

    # Open selected filename
    if filename:
      file = None
      try:
        file = open(filename, 'r')
        self.txvBuffer.set_text(file.read())
        print 'loading text from %s' % filename
      except IOError, (errno, strerror):
        ShowDialogError(
          text=_('Error opening the file') + '\n\n%s' % strerror,
          showOk=True,
          icon=handlepaths.get_app_logo()
        )
        print 'unable to load %s (I/O error %s: %s)' % (
          filename, errno, strerror
        )
      except:
        ShowDialogError(
          text=_('Error opening the file'), 
          showOk=True,
          icon=handlepaths.get_app_logo()
        )
        print 'error loading %s' % filename
      if file:
        file.close()
  
  def on_imgmenuFileSaveAs_activate(self, widget, filename=None):
    "Saves the whole text in the specified filename"
    if not filename:
      dialog = DialogFileSave(
        title=_('Please select where to save the text file'),
        initialDir=os.path.expanduser('~'))
      txtFilter = _('Text files (*.txt)')
      dialog.addFilter(txtFilter, ['*.txt'], None)
      dialog.addFilter(_('All files'), ['*'], None)
      dialog.set_icon_from_file(handlepaths.get_app_logo())
      if dialog.show():
        filename = dialog.filename
        if dialog.lastFilter.get_name() == txtFilter and filename[-4:] != '.txt':
          filename += '.txt'
        dialog.destroy()
    # Save selected filename
    if filename:
      print 'saving text in %s' % filename
      file = None
      try:
        file = open(filename, 'w')
        file.write(TextBuffer_get_text(self.txvBuffer))
        print 'file %s saved' % filename
      except IOError, (errno, strerror):
        ShowDialogError(
          text=_('Error saving the file') + '\n\n%s' % strerror,
          showOk=True,
          icon=handlepaths.get_app_logo()
        )
        print 'unable to save %s (I/O error %s: %s)' % (
          filename, errno, strerror
        )
      except:
        ShowDialogError(
          text=_('Error saving the file'),
          showOk=True,
          icon=handlepaths.get_app_logo()
        )
        print 'error saving %s' % filename
      if file:
        file.close()

  def on_imgmenuEditResetSettings_activate(self, widget, confirm=True):
    "Restore default settings"
    if confirm:
      dialog = DialogYesNo(
        message=_('Do you want to reset the default settings?'),
        default_button=gtk.RESPONSE_NO
      )
      dialog.set_icon_from_file(handlepaths.get_app_logo())
      dialog.show()
    # Reset if confirm was not requested or if the user gave response
    if not confirm or dialog.responseIsYes():
      if self.defaultLanguageIndex:
        self.cboLanguages.set_active(self.defaultLanguageIndex)
      print 'restored default settings'
      if os.path.exists(Settings.conffile):
        os.remove(Settings.conffile)
        print 'removed user settings file: %s' % Settings.conffile
      # Reload default settings
      Settings.load()
      self.loadSettings(True)


  def on_imgmenuEditStop_activate(self, widget, data=None):
    "Press button to stop play, indirect cause button style"
    self.btnPlayStop.set_active(False)

  def on_imgmenuEditPause_activate(self, widget, data=None):
    "Press button to pause or continue"
    self.btnPause.set_active(not self.btnPause.get_active())

  def on_imgmenuFileRec_activate(self, widget, filename=None):
    "Press button to record or disable recording"
    if filename:
      if not self.tlbRecord.get_active():
        # Workaround to press the button without showing the dialog
        self.recordToFileRequested = True
        self.tlbRecord.set_active(True)
        self.recordToFileRequested = False
        self.set_record(filename)
      else:
        return 'recording was already active, no action'
    else:
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
      language = self.listLanguages[self.cboLanguages.get_active()][COL_NAME]
      isMbrola = self.listLanguages[self.cboLanguages.get_active()][COL_MBROLA]
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
      self.imgmenuFileRec.set_sensitive(False)
      self.btnPause.set_sensitive(True)
      self.btnPlayStop.set_label('gtk-media-stop')
      self.tlbRecord.set_sensitive(False)
      if not isMbrola:
        self.espeak.play(cmd, self.cmdPlayer, self.recordToFile)
      else:
        args = {
          '%v': str(int(self.hscVolume.get_value())/100.), 
          '%l': '%s/%s/%s' % (
            Settings.get('VoicesmbPath'), 
            language.replace('mb-', '', 1),
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
    self.imgmenuFileRec.set_sensitive(True)
    self.btnPause.set_sensitive(False)
    self.btnPlayStop.set_label('gtk-media-play')
    if Settings.get('SingleRecord'):
      self.tlbRecord.set_active(False)
    self.tlbRecord.set_sensitive(True)

  def on_imgmenuEditPreferences_activate(self, widget, data=None):
    "Show preferences dialog"
    prefsUI = handlepaths.getPath('ui', 'preferences.glade')
    gladePrefs = gtk.glade.XML(fname=prefsUI, domain=handlepaths.APP_NAME)
    PreferencesWindow.showPreferencesWindow(gladePrefs, self.espeak)
    self.loadSettings(False)

  def on_tlbRecord_toggled(self, widget, data=None):
    # Workaround to avoid dialog show if the record was requested through dbus
    if self.recordToFileRequested:
      return
    self.recordToFile = None
    if self.tlbRecord.get_active():
      dialog = DialogFileSave(
        title=_('Please select where to save the recorded file'),
        initialDir=os.path.expanduser('~'))
      dialog.set_icon_from_file(handlepaths.get_app_logo())
      dialog.addFilter(_('Wave files (*.wav)'), ['*.wav'], None)
      dialog.addFilter(_('All files'), ['*'], None)
      if dialog.show():
        filename = dialog.filename
        if filename[-4:] != '.wav':
          filename += '.wav'
        self.set_record(filename)
      else:
        self.tlbRecord.set_active(False)
      dialog.destroy()
    else:
      self.stbStatus.pop(self.statusContextId)

  def set_record(self, filename):
    "Set record filename"
    print 'record to %s' % filename
    self.recordToFile = filename
    self.stbStatus.push(self.statusContextId, 
      _('Recording audio track to: %s' % self.recordToFile))
    
  def disable_record(self):
    "Disable recording"
    self.tlbRecord.set_active(False)
    
  def on_radioVoice_toggled(self, widget, data=None):
    "Assign variants after voice type change"
    if widget.get_active():
      self.listVariants.clear()
      self.listVariants.append(None)
      for v in self.variants[widget is self.radioVoiceFemale and 1 or 0]:
        self.listVariants.append(v)
      self.cboVariants.set_active(0)

  def set_text(self, text, insert_type=0):
    "Set buffer text"
    if insert_type == 0:
      # Replace previous text
      self.txvBuffer.set_text(text)
    elif insert_type == 1:
      # Insert at cursor
      self.txvBuffer.insert_at_cursor(text)
    elif insert_type == 2:
      # Insert at the begin
      self.txvBuffer.insert(self.txvBuffer.get_start_iter(), text)
    elif insert_type == 3:
      # Insert at the end
      self.txvBuffer.insert(self.txvBuffer.get_end_iter(), text)

  def set_position(self, position):
    "Set window position"
    position = position.split('x', 1)
    return self.winMain.move(int(position[0]), int(position[1]))

  def set_size(self, size):
    "Set window size"
    size = size.split('x', 1)
    return self.winMain.resize(int(size[0]), int(size[1]))

  def set_window(self, action, data=None):
    "Execute window action"
    return_value = None
    if action=='hide':
      return_value = self.winMain.hide()
      plugins.signal_proxy('on_hidden')
    elif action=='show':
      return_value = self.winMain.show()
      plugins.signal_proxy('on_shown')
    elif action=='minimize':
      return_value = self.winMain.iconify()
    elif action=='unminimize':
      return_value = self.winMain.deiconify()
    elif action=='maximize':
      return_value = self.winMain.maximize()
    elif action=='unmaximize':
      return_value = self.winMain.unmaximize()
    elif action=='fullscreen':
      return_value = self.winMain.fullscreen()
    elif action=='unfullscreen':
      return_value = self.winMain.unfullscreen()
    elif action=='stick':
      return_value = self.winMain.stick()
    elif action=='unstick':
      return_value = self.winMain.unstick()
    elif action=='active':
      return_value = self.winMain.is_active()
    elif action=='activate':
      return_value = self.winMain.present()
    elif action=='get-opacity':
      return_value = int(self.winMain.get_opacity() * 100)
    elif action=='set-opacity':
      return_value = self.winMain.set_opacity(0.01 * int(data))
    elif action=='set-keep-above':
      return_value = self.winMain.set_keep_above(True)
    elif action=='unset-keep-above':
      return_value = self.winMain.set_keep_above(False)
    elif action=='set-keep-below':
      return_value = self.winMain.set_keep_below(True)
    elif action=='unset-keep-below':
      return_value = self.winMain.set_keep_below(False)
    elif action=='get-size':
      return_value = 'x'.join(str(i) for i in list(self.winMain.get_size()))
    elif action=='get-position':
      return_value = 'x'.join(str(i) for i in list(self.winMain.get_position()))

    return str(return_value)
