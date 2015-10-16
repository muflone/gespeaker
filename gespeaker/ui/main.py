##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2015 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from .about import AboutWindow
from .files_dialog import FilesDialog
from .messages_dialog import MessagesDialog

from gespeaker.constants import *
from gespeaker.functions import _
from gespeaker.models.engines import ModelEngines
from gespeaker.models.languages import ModelLanguages
from gespeaker.gtkbuilder_loader import GtkBuilderLoader
from gespeaker.engines.base import KEY_ENGINE, KEY_LANGUAGE, KEY_NAME, KEY_GENDER

class MainWindow(object):
  def __init__(self, application, backend):
    self.application = application
    self.ui = GtkBuilderLoader(FILE_UI_MAIN)
    self.backend = backend
    self.backend.on_play_complete = self.on_backend_play_complete
    self.loadUI()
    # Restore the saved size and position
    if self.backend.settings.get_value('width', 0) and \
        self.backend.settings.get_value('height', 0):
      self.ui.winMain.set_default_size(
        self.backend.settings.get_value('width', -1),
        self.backend.settings.get_value('height', -1))
    if self.backend.settings.get_value('left', 0) and \
        self.backend.settings.get_value('top', 0):
      self.ui.winMain.move(
        self.backend.settings.get_value('left', 0),
        self.backend.settings.get_value('top', 0))
    # Load the others dialogs
    self.about = AboutWindow(self.ui.winMain, False)

  def run(self):
    """Show the UI"""
    self.ui.winMain.show_all()

  def loadUI(self):
    """Load the interface UI"""
    # Load available engines
    self.modelEngines = ModelEngines(self.ui.modelEngines)
    for engine_name, obj_engine in self.backend.engines.items():
      # Add a new CheckMenuItem for each engine
      menuengine = Gtk.CheckMenuItem(engine_name)
      # Load the engine status from the settings
      obj_engine.enabled = self.backend.settings.get_engine_status(engine_name)
      menuengine.set_active(obj_engine.enabled)
      menuengine.connect('toggled', self.on_actionEnableEngine_toggled, obj_engine)
      self.ui.menuEngines.append(menuengine)
    # Load available languages
    self.modelLanguages = ModelLanguages(self.ui.modelLanguages,
      GdkPixbuf.Pixbuf.new_from_file_at_size(FILE_GENDER_MALE, 24, 24),
      GdkPixbuf.Pixbuf.new_from_file_at_size(FILE_GENDER_FEMALE, 24, 24),
      GdkPixbuf.Pixbuf.new_from_file_at_size(FILE_GENDER_UNKNOWN, 24, 24))
    self.ui.sortmodelLanguages.set_sort_column_id(
      self.modelLanguages.COL_DESCRIPTION, Gtk.SortType.ASCENDING)
    self.on_actionRefresh_activate(None)
    self.on_cboEngines_changed(None)
    # Set various properties
    self.ui.winMain.set_title(APP_NAME)
    self.ui.winMain.set_icon_from_file(FILE_ICON)
    self.ui.winMain.set_application(self.application)
    # Set the actions accelerator group
    for group_name in ('actionsApplication', 'actionsEdit', 'actionsFile',
        'actionsMedia'):
      if isinstance(self.ui.get_object(group_name), Gtk.ActionGroup):
        for action in self.ui.get_object(group_name).list_actions():
          action.set_accel_group(self.ui.accelerators)
    # Define the clipboard object for cut/copy/paste actions
    self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    # Connect signals from the glade file to the functions with the same name
    self.ui.connect_signals(self)

  def on_winMain_delete_event(self, widget, event):
    """Close the application"""
    self.on_actionQuit_activate(widget)

  def on_actionAbout_activate(self, action):
    """Show the about dialog"""
    self.about.show()

  def on_actionQuit_activate(self, action):
    """Quit the application"""
    # Stop any previous play
    self.ui.actionPlayStop.set_active(False)
    # Save settings for window size
    self.backend.settings.set_sizes(self.ui.winMain)
    self.backend.settings.save()
    self.about.destroy()
    self.ui.winMain.destroy()
    self.application.quit()

  def _get_current_engine(self):
    """Return the currently selected engine"""
    if self.ui.cboEngines.get_active_iter():
      return self.modelEngines.get_engine(
        self.ui.cboEngines.get_active_iter())
    else:
      return None

  def _get_current_language_engine(self):
    """Return the engine used for the currently selected language"""
    return self.modelLanguages.get_engine(
      self.ui.sortmodelLanguages.convert_iter_to_child_iter(
      self.ui.cboLanguages.get_active_iter()))

  def _get_current_language_name(self):
    """Return the name for the currently selected language"""
    return self.modelLanguages.get_name(
      self.ui.sortmodelLanguages.convert_iter_to_child_iter(
      self.ui.cboLanguages.get_active_iter()))

  def on_cboEngines_changed(self, widget):
    """Update languages list after engine change"""
    self.modelLanguages.clear()
    current_engine = self._get_current_engine()
    for obj_engine in self.backend.engines.values():
      # Load languages only for selected engine
      if obj_engine.name == current_engine and obj_engine.enabled:
        for language in obj_engine.get_languages():
          self.modelLanguages.add(
            engine=obj_engine.name,
            description='%s%s (%s)' % (
              language[KEY_LANGUAGE],
              ' (%s)' % language[KEY_NAME] if self.backend.settings.is_debug() \
              else '',
              {'male': _('Male'), 'female': _('Female'),
              'other': _('Unknown')}.get(language[KEY_GENDER], 'other')),
            name=language[KEY_NAME],
            gender=language[KEY_GENDER]
            )
    self.on_bufferText_changed(None)
    self.ui.cboLanguages.set_tooltip_text('%d languages available' % 
      self.modelLanguages.count())
    self.ui.cboLanguages.set_active(0)

  def on_actionClipboard_activate(self, action):
    """Cut and copy the selected text or paste it"""
    bEditable = self.ui.txtText.get_editable()
    if action is self.ui.actionCut:
      self.ui.bufferText.cut_clipboard(self.clipboard, bEditable)
    elif action is self.ui.actionCopy:
      self.ui.bufferText.copy_clipboard(self.clipboard)
    elif action is self.ui.actionPaste:
      self.ui.bufferText.paste_clipboard(self.clipboard, None, bEditable)

  def on_actionPlayStop_toggled(self, action):
    """Play or stop play"""
    if self.ui.actionPlayStop.get_active():
      self.ui.actionPlayStop.set_label(self.ui.actionStop.get_label())
      self.ui.btnPlay.set_image(self.ui.imageStop)
      # Play the text
      self.backend.set_current_engine(self._get_current_language_engine())
      self.backend.play(
        text=self.ui.bufferText.get_text(self.ui.bufferText.get_start_iter(),
          self.ui.bufferText.get_end_iter(), False),
        language=self._get_current_language_name())
      self.ui.actionPause.set_active(False)
      self.ui.actionPause.set_sensitive(True)
      self.ui.actionRecord.set_sensitive(False)
    else:
      # Stop any previous play
      self.ui.btnPlay.set_image(self.ui.imagePlay)
      self.ui.actionPlayStop.set_label(self.ui.actionPlay.get_label())
      self.ui.actionRecord.set_sensitive(True)
      self.backend.stop()

  def on_actionPause_toggled(self, action):
    """Pause or resume"""
    if self.ui.actionPlayStop.get_active():
      # Pause or resume
      self.backend.pause(self.ui.actionPause.get_active())
    else:
      # Uncheck the Pause button if no playing is active
      self.ui.actionPause.set_active(False)

  def on_actionRefresh_activate(self, action):
    """Reload the available voices list"""
    self.modelEngines.clear()
    self.modelLanguages.clear()
    for obj_engine in self.backend.engines.values():
      # Load languages only for enabled engines
      if obj_engine.enabled:
        self.modelEngines.add(obj_engine.name, obj_engine.name)
    # Select the first item
    self.ui.cboEngines.set_active(0)
    self.ui.cboLanguages.set_active(0)

  def on_actionEnableEngine_toggled(self, action, engine):
    """Enable or disable an engine"""
    engine.enabled = action.get_active()
    self.backend.settings.set_engine_status(engine.name, engine.enabled)
    self.on_actionRefresh_activate(action)

  def on_backend_play_complete(self):
    """Whenever a playing is completed uncheck the Play button and
    disable the Pause button"""
    self.ui.actionPlayStop.set_active(False)
    self.ui.actionPause.set_active(False)
    self.ui.actionPause.set_sensitive(False)

  def on_actionOpen_activate(self, action):
    """Load an external text file"""
    dialog = FilesDialog(self.ui.winMain)
    dialog.add_filter(_('Text files'), ('text/*', ), ('*.txt', ), )
    dialog.add_filter(_('All files'), None, ('*', ))
    dialog.title = _('Please select the text file to open')
    filename = dialog.show_open()
    if filename:
      try:
        # Open the selected text file
        with open(filename, 'r') as f:
          self.backend.settings.debug_line('loading text from %s' % filename)
          self.ui.bufferText.set_text(f.read())
      except Exception, error:
        # Handle any exception
        self.backend.settings.debug_line('Error loading %s (Error: %s)' % (
          filename, error))
        dialog = MessagesDialog(self.ui.winMain)
        dialog.primary_text = _('Error opening the file')
        dialog.secondary_text = error
        dialog.show_error()

  def on_actionSaveAs_activate(self, action):
    """Save the text to an external text file"""
    dialog = FilesDialog(self.ui.winMain)
    dialog.add_filter(_('Text files'), ('text/*', ), ('*.txt', ), )
    dialog.add_filter(_('All files'), None, ('*', ))
    dialog.title = _('Please select where to save the text file')
    filename = dialog.show_save()
    if filename:
      try:
        # Save to the selected text file
        with open(filename, 'w') as f:
          self.backend.settings.debug_line('saving text in %s' % filename)
          f.write(self.ui.bufferText.get_text(
            start=self.ui.bufferText.get_start_iter(),
            end=self.ui.bufferText.get_end_iter(),
            include_hidden_chars=False))
      except Exception, error:
        # Handle any exception
        self.backend.settings.debug_line('Error saving to %s (Error: %s)' % (
          filename, error))
        dialog = MessagesDialog(self.ui.winMain)
        dialog.primary_text = _('Error saving the file')
        dialog.secondary_text = error
        dialog.show_error()

  def on_actionNew_activate(self, action):
    """Clear the text buffer"""
    if len(self.ui.bufferText.get_text(
        start=self.ui.bufferText.get_start_iter(),
        end=self.ui.bufferText.get_end_iter(),
        include_hidden_chars=False)) > 0:
      dialog = MessagesDialog(self.ui.winMain)
      dialog.title = ''
      dialog.primary_text = _('Do you want to delete the current text?')
      if dialog.show_question() == Gtk.ResponseType.OK:
        self.backend.settings.debug_line('text cleared')
        self.ui.bufferText.set_text('')

  def on_actionRecord_activate(self, action):
    """Record the text to play"""
    dialog = MessagesDialog(self.ui.winMain)
    dialog.primary_text = _('Not implemented yet!')
    dialog.show_warning()
    self.ui.actionPlayStop.activate()
    
  def on_actionPreferences_activate(self, action):
    """Show the preferences dialog"""
    dialog = MessagesDialog(self.ui.winMain)
    dialog.primary_text = _('Not implemented yet!')
    dialog.show_warning()

  def on_bufferText_changed(self, widget):
    """Enable or disable the New and Save actions on text change"""
    text = self.ui.bufferText.get_text(
      self.ui.bufferText.get_start_iter(),
      self.ui.bufferText.get_end_iter(),
      True)
    has_text = len(text) > 0
    # New and Save actions depend on the written text
    self.ui.actionNew.set_sensitive(has_text)
    self.ui.actionSaveAs.set_sensitive(has_text)
    # For voices settings and Play action check the number of languages
    has_languages = self.modelLanguages.count() > 0
    self.ui.lblEngine.set_sensitive(has_languages)
    self.ui.cboLanguages.set_sensitive(has_languages)
    self.ui.lblLanguage.set_sensitive(has_languages)
    self.ui.actionPlayStop.set_sensitive(has_text and has_languages)
    self.ui.actionRecord.set_sensitive(has_text and has_languages)
