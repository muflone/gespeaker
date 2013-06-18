##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2013 Fabio Castelli
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
import Settings
import SubprocessWrapper
import os.path
import handlepaths
import plugins
import pango
from gettext import gettext as _
from DialogSimpleMessages import ShowDialogError
from DialogAbout import DialogAbout
from pygtkutils import *

COL_ACTIVE, COL_ICON, COL_NAME, COL_MARKUP = range(4)

def showPreferencesWindow(gladeFile, espeak):
  prefsWindow = PreferencesWindow(gladeFile, espeak)

class PreferencesWindow(object):
  def __init__(self, gladeFile, espeak):
    self.gladeFile = gladeFile
    self.espeak = espeak
    self.loadControls()
    self.dlgPrefs.set_icon_from_file(handlepaths.get_app_logo())
    signals = {
      'on_cboPlayer_changed': self.on_cboPlayer_changed,
      'on_btnPlayerTest_clicked': self.on_btnPlayerTest_clicked,
      'on_chkCustomWelcome_toggled': self.on_chkCustomWelcome_toggled,
      'on_btnRefresh_clicked': self.on_btnRefresh_clicked,
      'on_btnOk_clicked': self.on_btnOk_clicked,
      'on_btnPluginInfo_clicked': self.on_btnPluginInfo_clicked,
      'on_tvwPlugins_row_activated': self.on_tvwPlugins_row_activated
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
    self.chooserLanguagePath.set_current_folder(Settings.get('VoicesmbPath'))
    # Before to use the window property the realize method must be called
    self.dlgPrefs.realize()
    # Change WM buttons making the window only movable with the closing button
    self.dlgPrefs.window.set_functions(gtk.gdk.FUNC_CLOSE | gtk.gdk.FUNC_MOVE)
    # Reload mbrola languages list
    self.btnRefresh.clicked()
    # Load plugins list
    self.modelPlugins.clear()
    for pl in plugins.plugins.itervalues():
      self.modelPlugins.append([
        pl.active,
        pl.render_icon(),
        pl.name,
        '<b>%s</b>\n%s' % (pl.name, pl.description)
      ])
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
    self.tvwLanguages = gw('tvwLanguages')
    self.chooserLanguagePath = gw('chooserLanguagePath')
    self.btnRefresh = gw('btnRefresh')
    self.btnOk = gw('btnOk')
    self.imgExecutableMbrola = gw('imgExecutableMbrola')
    self.lblExecutableMbrolaStatus = gw('lblExecutableMbrolaStatus')
    self.lblLanguagesDetected = gw('lblLanguagesDetected')
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
      handlepaths.getPath('icons', 'alsalogo.png'), (24, 24)), 
      _('ALSA - Advanced Linux Sound Architecture'), False])
    listStore.append([Pixbuf_load_file(
      handlepaths.getPath('icons', 'palogo.png'), (24, 24)), 
      _('PulseAudio sound server'), False])
    listStore.append([None, '_', True])
    listStore.append([None, _('Custom sound application'), False])
    # Change testing button caption
    Button_change_stock_description(self.btnPlayerTest, _('_Test'), True)
    # Create model and sorted model for mbrola languages
    self.modelMbrola = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str)
    #self.tvwLanguages.set_model(self.modelMbrola)
    sortedModel = gtk.TreeModelSort(self.modelMbrola)
    sortedModel.set_sort_column_id(1, gtk.SORT_ASCENDING)
    self.tvwLanguages.set_model(sortedModel)
    # Create columns for tvwLanguages
    COL_LANG_IMG, COL_LANG_LANG, COL_LANG_RES, COL_LANG_STATUS = range(4)
    cell = gtk.CellRendererPixbuf()
    column = gtk.TreeViewColumn('')
    column.pack_start(cell)
    column.set_attributes(cell, pixbuf=COL_LANG_IMG)
    self.tvwLanguages.append_column(column)
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn(_('Language'), cell, text=COL_LANG_LANG)
    column.set_sort_column_id(COL_LANG_LANG)
    column.set_resizable(True)
    self.tvwLanguages.append_column(column)

    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn(_('Resource'), cell, text=COL_LANG_RES)
    column.set_sort_column_id(COL_LANG_RES)
    column.set_resizable(True)
    self.tvwLanguages.append_column(column)

    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn(_('Status'), cell, text=COL_LANG_STATUS)
    column.set_sort_column_id(COL_LANG_STATUS)
    column.set_resizable(True)
    self.tvwLanguages.append_column(column)
    # Order by Language column
    #column = self.tvwLanguages.get_column(COL_LANG_LANG)
    #column.set_sort_column_id(COL_LANG_LANG)
    #column.set_sort_order(gtk.SORT_ASCENDING)
    #column.set_sort_indicator(True)
    
    # Plugins
    self.tvwPlugins = gw('tvwPlugins')
    self.btnPluginInfo = gw('btnPluginInfo')
    self.btnPluginConfigure = gw('btnPluginConfigure')
    Button_change_stock_description(self.btnPluginInfo, _('_About plugin'), True)
    Button_change_stock_description(self.btnPluginConfigure, _('_Configure plugin'), True)
    # Create model for plugins list
    self.modelPlugins = gtk.ListStore(
      bool,           # active
      gtk.gdk.Pixbuf, # icon
      str,            # name
      str             # markup
    )
    sortedModel = gtk.TreeModelSort(self.modelPlugins)
    sortedModel.set_sort_column_id(COL_NAME, gtk.SORT_ASCENDING)
    self.tvwPlugins.set_model(sortedModel)
    cell = gtk.CellRendererToggle()
    cell.connect('toggled', self.on_pluginenable_toggle)
    column = gtk.TreeViewColumn(None, cell, active=COL_ACTIVE)
    self.tvwPlugins.append_column(column)
    
    cell = gtk.CellRendererPixbuf()
    column = gtk.TreeViewColumn(None, cell, pixbuf=COL_ICON)
    self.tvwPlugins.append_column(column)
    
    cell = gtk.CellRendererText()
    cell.set_property('ellipsize', pango.ELLIPSIZE_END)
    column = gtk.TreeViewColumn(None, cell, markup=COL_MARKUP)
    column.set_resizable(True)
    self.tvwPlugins.append_column(column)   

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
    Settings.set('VoicesmbPath', self.chooserLanguagePath.get_filename())

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
    filename = handlepaths.getPath('data', 'testing.wav')
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
      ShowDialogError(
        title=_('Audio testing'),
        showOk=True,
        text=_('There was an error during the test for the audio player.\n\n'
          'Error %s: %s') % (errno, strerror),
        icon=handlepaths.get_app_logo()
      )
    # Terminate test if it's still running, follows a broken pipe error
    if test.poll() is None:
      test.terminate()
    # Restore default cursor
    Window_change_cursor(self.dlgPrefs.window, None, False)

  def on_btnRefresh_clicked(self, widget, data=None):
    "Reload mbrola languages from the selected folder"
    self.modelMbrola.clear()
    selectedFolder = self.chooserLanguagePath.get_filename()
    if not selectedFolder:
      # Calling before the dialog is shown results in None path
      selectedFolder = Settings.get('VoicesmbPath')
    mbrolaVoices = self.espeak.loadMbrolaVoices(selectedFolder)
    voicesFound = 0
    for voice in mbrolaVoices:
      if voice[2]:
        voicesFound += 1
      self.modelMbrola.append((
        widget.render_icon(voice[2] and gtk.STOCK_YES or gtk.STOCK_NO, 
        gtk.ICON_SIZE_BUTTON), voice[0], voice[1],
        voice[2] and _('Installed') or _('Not installed')))
    # lblLanguagesDetected
    self.lblLanguagesDetected.set_text(_("%d languages of %d detected") % (
      voicesFound, len(mbrolaVoices)))
    # Check if mbrola exists
    status = self.espeak.mbrolaExists(Settings.cmdMbrola)
    self.imgExecutableMbrola.set_from_stock(size=gtk.ICON_SIZE_BUTTON,
      stock_id=status and gtk.STOCK_YES or gtk.STOCK_NO)
    self.lblExecutableMbrolaStatus.set_label('<b>%s</b>' % (status and 
      _('Package mbrola installed') or _('Package mbrola not installed')))

  def on_pluginenable_toggle(self, renderer, path, data=None):
    "Select or deselect a plugin"
    path = self.tvwPlugins.get_model().convert_path_to_child_path(path)
    p = self.modelPlugins[path]
    p[COL_ACTIVE] = not p[COL_ACTIVE]
    plugins.plugins[p[COL_NAME]].active = not plugins.plugins[p[COL_NAME]].active


  def on_btnPluginInfo_clicked(self, widget, data=None):
    "Show information about plugin"
    model, iter = self.tvwPlugins.get_selection().get_selected()
    if model:
      plugin = plugins.plugins[model[iter][COL_NAME]]
      DialogAbout(
        name=model[iter][COL_NAME],
        version=plugin.version,
        comment=plugin.description,
        copyright='Copyright %s' % plugin.author,
        website=plugin.website,
        website_label=plugin.website,
        logo=model[iter][COL_ICON],
        icon=handlepaths.get_app_logo()
      )

  def on_tvwPlugins_row_activated(self, widget, path, column, data=None):
    self.on_btnPluginInfo_clicked(widget, data)
