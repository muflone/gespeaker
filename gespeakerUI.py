##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require("2.0")

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

cmdEspeak = '/usr/bin/espeak'
cmdPlayer = 'aplay'
argsEspeak = '--stdout -a %d -p %d -s %d -g %d -v %s -f %s'

class gespeakerUI(object):
  def __init__(self, app_name, app_title, app_version):
    print 'starting gespeaker'
    self.espeak = EspeakFrontend()
    # Create temporary filename
    self.tempFilename = tempfile.mkstemp(prefix='gespeaker')[1]
    gladeUI = 'gespeaker.glade'
    self.app_name = app_name
    self.app_title = app_title
    self.app_version = app_version
    self.timeoutCheck = None
    print 'loading interface from %s' % gladeUI
    self.gladeFile = gtk.glade.XML(fname=gladeUI, domain=self.app_name)
    # Signals handler
    segnali = {
      'on_imgmenuFileQuit_activate': self.on_imgmenuFileQuit_activate,
      'on_imgmenuEditPlay_activate': self.on_imgmenuEditPlay_activate,
      'on_imgmenuFileNew_activate': self.on_imgmenuFileNew_activate,
      'on_imgmenuFileOpen_activate': self.on_imgmenuFileOpen_activate,
      'on_imgmenuFileSaveAs_activate': self.on_imgmenuFileSaveAs_activate,
      'on_imgmenuEditStop_activate': self.on_imgmenuEditStop_activate,
      'on_btnPlayStop_toggled': self.on_btnPlayStop_toggled,
      'on_btnPause_toggled': self.on_btnPause_toggled,
      'on_imgmenuEditPause_activate': self.on_imgmenuEditPause_activate,
      'on_imgmenuEditResetSettings_activate': self.on_imgmenuEditResetSettings_activate,
      'on_imgmenuHelpAbout_activate': self.on_imgmenuHelpAbout_activate
    }
    self.gladeFile.signal_autoconnect(segnali)
    # Load window and controls
    self.loadControls()
    self.winMain.show()
    # Play default message
    self.btnPlayStop.set_active(True)
    gtk.main()
  
  def loadControls(self):
    "Load controls and other values"
    # Load controls from gladeFile
    print 'loading controls from UI'
    gw = self.gladeFile.get_widget
    self.winMain = gw('winMain')
    self.winMain.set_title(self.app_title)
    self.winMain.set_icon_from_file('gespeaker.svg')
    self.winMain.set_focus(gw('txvText'))
    self.txvBuffer = gw('txvText').get_buffer()
    self.hscVolume = gw('hscVolume')
    self.hscPitch = gw('hscPitch')
    self.hscSpeed = gw('hscSpeed')
    self.hscDelay = gw('hscDelay')
    self.cboLanguages = gw('cboLanguages')
    self.radioVoiceMale = gw('radioVoiceMale')
    self.radioVoiceFemale = gw('radioVoiceFemale')
    self.imgmenuEditPlay = gw('imgmenuEditPlay')
    self.imgmenuEditStop = gw('imgmenuEditStop')
    self.tlbStop = gw('tlbStop')
    self.btnPlayStop = gw('btnPlayStop')
    self.btnPause = gw('btnPause')
    self.imgmenuEditPause = gw('imgmenuEditPause')
    # Useful lambda to get txvBuffer's text
    self.getText = lambda buffer=self.txvBuffer: buffer.get_text(
      buffer.get_start_iter(), buffer.get_end_iter()
    )
    # Create model for cboLanguages by (language, shortname)
    listLanguages = gtk.ListStore(str, str)
    self.cboLanguages.set_model(listLanguages)
    cell = gtk.CellRendererText()
    self.cboLanguages.pack_start(cell, True)
    self.cboLanguages.add_attribute(cell, 'text', 0)
    # Load languages list from espeak --voices
    self.defaultLanguage = 0
    for langs in self.espeak.loadLanguages(cmdEspeak):
      lang = langs[22:52].rsplit(None, 1)
      listLanguages.append(lang)
      if lang[0] == _('default language'):
        self.defaultLanguage = listLanguages.iter_n_children(None) - 1
    # Sets default language
    self.cboLanguages.set_active(self.defaultLanguage)
  
  def on_imgmenuFileQuit_activate(self, widget, data=None):
    "Close the program"
    print 'quitting'
    if self.tempFilename and os.path.exists(self.tempFilename):
      os.remove(self.tempFilename)
    gtk.main_quit()
    return 0
  
  def on_imgmenuEditPlay_activate(self, widget, data=None):
    "Press button to start play, indirect cause button style"
    self.btnPlayStop.set_active(True)
  
  def on_imgmenuFileNew_activate(self, widget, data=None):
    "Clears the whole text"
    if self.getText(self.txvBuffer):
      dialog = DialogYesNo(
        message=_('Do you want to delete the current text?'), 
        default_button=gtk.RESPONSE_NO
      )
      dialog.set_icon_from_file('gespeaker.svg')
      dialog.show()
      if dialog.responseIsYes():
        self.txvBuffer.set_text('')
        print 'text cleared'
  
  def on_imgmenuFileOpen_activate(self, widget, data=None):
    "Loads an external file"
    dialog = DialogFileOpen(title=_('Please select the file to open'))
    dialog.set_icon_from_file('gespeaker.svg')
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
        print "unable to load %s (I/O error %s: %s)" % (
          dialog.filename, errno, strerror
        )
      except:
        ShowDialogError(text=_('Error opening the file'), showOk=True)
        print 'error loading %s' % dialog.filename
      if file:
        file.close()
  
  def on_imgmenuFileSaveAs_activate(self, widget, data=None):
    "Saves the whole text in the specified filename"
    dialog = DialogFileSave(title=_('Please select where to save the file'))
    dialog.set_icon_from_file('gespeaker.svg')
    if dialog.show():
      print 'saving text in %s' % dialog.filename
      file = None
      try:
        file = open(dialog.filename, 'w')
        file.write(self.getText(self.txvBuffer))
        print 'file %s saved' % dialog.filename
      except IOError, (errno, strerror):
        ShowDialogError(
          text=_('Error saving the file') + '\n\n%s' % strerror,
          showOk=True
        )
        print "unable to save %s (I/O error %s: %s)" % (
          dialog.filename, errno, strerror
        )
      except:
        ShowDialogError(text=_('Error saving the file'), showOk=True)
        print 'error saving %s' % dialog.filename
      if file:
        file.close()

  def on_imgmenuEditResetSettings_activate(self, widget, data=None):
    "Restore default settings"
    dialog = DialogYesNo(
      message=_('Do you want to reset the default settings?'),
      default_button=gtk.RESPONSE_NO
    )
    dialog.set_icon_from_file('gespeaker.svg')
    dialog.show()
    if dialog.responseIsYes():
      self.hscVolume.set_value(100)
      self.hscPitch.set_value(50)
      self.hscSpeed.set_value(170)
      self.hscDelay.set_value(10)
      self.radioVoiceMale.set_active(True)
      if self.defaultLanguage:
        self.cboLanguages.set_active(self.defaultLanguage)
      print 'restored default settings'

  def on_imgmenuHelpAbout_activate(self, widget, data=None):
    "Shows the about dialog"
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
      logo='gespeaker.svg',
      icon='gespeaker.svg'
    )

  def on_imgmenuEditStop_activate(self, widget, data=None):
    "Press button to stop play, indirect cause button style"
    self.btnPlayStop.set_active(False)

  def on_imgmenuEditPause_activate(self, widget, data=None):
    "Press button to pause or continue"
    self.btnPause.set_active(not self.btnPause.get_active())

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
    if self.btnPlayStop.get_active():
      # Button active so we have to start to play
      self.startPlaying()
    else:
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
    self.playText(self.getText(self.txvBuffer))

  def playText(self, text):
    if text:
      # Save buffer text on temporary filename and play it
      tmpFile = open(self.tempFilename, mode='w')
      tmpFile.write(text)
      tmpFile.close()
      cmd = '%s %s' % (cmdEspeak, argsEspeak % (
          self.hscVolume.get_value(), 
          self.hscPitch.get_value(),
          self.hscSpeed.get_value(),
          self.hscDelay.get_value(),
          self.cboLanguages.get_model()[self.cboLanguages.get_active()][1] +
          (self.radioVoiceFemale.get_active() and '+12' or ''),
          self.tempFilename
        )
      )
      print cmd
      self.espeak.play(cmd, cmdPlayer)
      # Enable stop buttons on menu and toolbar
      self.imgmenuEditPlay.set_sensitive(False)
      self.imgmenuEditStop.set_sensitive(True)
      self.imgmenuEditPause.set_sensitive(True)
      self.btnPause.set_sensitive(True)
      self.btnPlayStop.set_label('gtk-media-stop')
      # Enable check for running processes
      self.setStopCheck(True)

  def stopPlaying(self):
    if self.espeak.stop():
      # If stopped then disable buttons and menus
      self.setStopCheck(False)
      self.imgmenuEditPlay.set_sensitive(True)
      self.imgmenuEditStop.set_sensitive(False)
      self.imgmenuEditPause.set_sensitive(False)
      self.btnPause.set_sensitive(False)
      self.btnPlayStop.set_label('gtk-media-play')

