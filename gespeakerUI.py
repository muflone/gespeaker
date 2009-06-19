##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import gtk
import gtk.glade
import pygtk
pygtk.require("2.0")

import subprocess
from gettext import gettext as _

from DialogYesNo import DialogYesNo
from DialogFileOpenSave import DialogFileOpen, DialogFileSave
from DialogSimpleMessages import *
from DialogAbout import DialogAbout

espeakcmd = '/usr/bin/espeak'
espeakargs = '--stdout -a %d -p %d -s %d -g %d -v %s "%s" | aplay 2> /dev/null'

class gespeakerUI():
  def __init__(self, app_name, app_title, app_version):
    print 'starting gespeaker'
    gladeUI = 'gespeaker.glade'
    self.app_name = app_name
    self.app_title = app_title
    self.app_version = app_version
    print 'loading interface from %s' % gladeUI
    self.gladeFile = gtk.glade.XML(fname=gladeUI, domain=self.app_name)
    # Signals handler
    segnali = {
      'on_imgmenuFileQuit_activate': self.on_imgmenuFileQuit_activate,
      'on_imgmenuEditPlay_activate': self.on_imgmenuEditPlay_activate,
      'on_imgmenuFileNew_activate': self.on_imgmenuFileNew_activate,
      'on_imgmenuFileOpen_activate': self.on_imgmenuFileOpen_activate,
      'on_imgmenuFileSaveAs_activate': self.on_imgmenuFileSaveAs_activate,
      'on_imgmenuEditResetSettings_activate': self.on_imgmenuEditResetSettings_activate,
      'on_imgmenuHelpAbout_activate': self.on_imgmenuHelpAbout_activate
    }
    self.gladeFile.signal_autoconnect(segnali)
    # Load window and controls
    self.loadControls()
    self.winMain.show()
    gtk.main()
  
  def loadControls(self):
    "Load controls and other values"
    # Load controls from gladeFile
    print 'loading controls from UI'
    self.winMain = self.gladeFile.get_widget('winMain')
    self.winMain.set_title(self.app_title)
    self.winMain.set_icon_from_file('gespeaker.png')
    self.txvBuffer = self.gladeFile.get_widget('txvText').get_buffer()
    self.hscVolume = self.gladeFile.get_widget('hscVolume')
    self.hscPitch = self.gladeFile.get_widget('hscPitch')
    self.hscSpeed = self.gladeFile.get_widget('hscSpeed')
    self.hscDelay = self.gladeFile.get_widget('hscDelay')
    self.cboLanguages = self.gladeFile.get_widget('cboLanguages')
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
    print 'loading languages from %s --voices' % espeakcmd
    p = subprocess.Popen((espeakcmd, '--voices'), stdout=subprocess.PIPE)
    self.defaultLanguage = 0
    for langs in p.communicate()[0].split('\n')[1:-1]:
      lang = langs[22:52].rsplit(None, 1)
      listLanguages.append(lang)
      if lang[0] == _('default language'):
        self.defaultLanguage = listLanguages.iter_n_children(None) - 1
    # Sets default language
    self.cboLanguages.set_active(self.defaultLanguage)
  
  def on_imgmenuFileQuit_activate(self, widget, data=None):
    "Close the program"
    print 'quitting'
    gtk.main_quit()
    return 0
  
  def on_imgmenuEditPlay_activate(self, widget, data=None):
    "Play whole text"
    text = self.getText(self.txvBuffer)
    text = text.replace('\\', '\\\\')
    text = text.replace('`', '\\`')
    text = text.replace('"', '\\"')
    text = text.replace('$', '\\$')
    print text
    if text:
      cmd = '%s %s' % (espeakcmd, espeakargs % (
          self.hscVolume.get_value(), 
          self.hscPitch.get_value(),
          self.hscSpeed.get_value(),
          self.hscDelay.get_value(),
          self.cboLanguages.get_model()[self.cboLanguages.get_active()][1],
          text
        )
      )
      print cmd
      processPlay = subprocess.Popen(cmd, shell=True)
  
  def on_imgmenuFileNew_activate(self, widget, data=None):
    "Clears the whole text"
    if self.getText(self.txvBuffer):
      dialog = DialogYesNo(
        message=_('Do you want to delete the current text?'), 
        default_button=gtk.RESPONSE_NO
      )
      dialog.set_icon_from_file('gespeaker.png')
      dialog.show()
      if dialog.responseIsYes():
        self.txvBuffer.set_text('')
        print 'text cleared'
  
  def on_imgmenuFileOpen_activate(self, widget, data=None):
    "Loads an external file"
    dialog = DialogFileOpen(title=_('Please select the file to open'))
    dialog.set_icon_from_file('gespeaker.png')
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
      finally:
        if file:
          file.close()
  
  def on_imgmenuFileSaveAs_activate(self, widget, data=None):
    "Saves the whole text in the specified filename"
    dialog = DialogFileSave(title=_('Please select where to save the file'))
    dialog.set_icon_from_file('gespeaker.png')
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
      finally:
        if file:
          file.close()

  def on_imgmenuEditResetSettings_activate(self, widget, data=None):
    "Restore default settings"
    dialog = DialogYesNo(
      message=_('Do you want to reset the default settings?'),
      default_button=gtk.RESPONSE_NO
    )
    dialog.set_icon_from_file('gespeaker.png')
    dialog.show()
    if dialog.responseIsYes():
      self.hscVolume.set_value(100)
      self.hscPitch.set_value(50)
      self.hscSpeed.set_value(170)
      self.hscDelay.set_value(10)
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
      logo='gespeaker.png',
      icon='gespeaker.png'
    )
