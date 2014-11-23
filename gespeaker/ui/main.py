##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2014 Fabio Castelli
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

from .about import AboutWindow

from gespeaker.constants import *
from gespeaker.functions import *
from gespeaker.models.languages import ModelLanguages
from gespeaker.models.variants import ModelVariants
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
    def filter_variants_cb(model, iter, data):
      """Filter the variants for the current voice engine"""
      current_engine = self._get_current_language_engine()
      genders = ['', ]
      if self.backend.engines[current_engine].has_gender:
        genders.append(self.ui.optionVoiceMale.get_active() and 'male' or 'female')
      # Return True if the variant is the normal voice (without engine name)
      # or it's of the currently selected engine
      # and of the currently selected gender or gender agnostic
      engines = ['', current_engine]
      return model.get_value(iter, self.modelVariants.COL_ENGINE) in engines and \
        model.get_value(iter, self.modelVariants.COL_GENDER) in genders
    # Load available engines
    for engine_name, obj_engine in self.backend.engines.items():
      # Add a new CheckMenuItem for each engine
      menuengine = Gtk.CheckMenuItem(engine_name)
      # Load the engine status from the settings
      obj_engine.enabled = self.backend.settings.get_engine_status(engine_name)
      menuengine.set_active(obj_engine.enabled)
      menuengine.connect('toggled', self.on_actionEnableEngine_toggled, obj_engine)
      self.ui.menuEngines.append(menuengine)
    # Load available languages
    self.modelLanguages = ModelLanguages(self.ui.modelLanguages)
    self.ui.sortmodelLanguages.set_sort_column_id(
      self.modelLanguages.COL_DESCRIPTION, Gtk.SortType.ASCENDING)
    # Load available variants
    self.modelVariants = ModelVariants(self.ui.modelVariants)
    self.modelVariants.clear()
    for language in self.backend.get_variants():
      self.modelVariants.add(
        engine=language[KEY_ENGINE],
        description='%s%s' % (language[KEY_LANGUAGE],
          self.backend.settings.is_debug() and ' (%s)' % language[KEY_NAME] or ''),
        name=language[KEY_NAME],
        gender=language[KEY_GENDER]
        )
    self.ui.sortmodelVariants.set_sort_column_id(
      self.modelVariants.COL_DESCRIPTION, Gtk.SortType.ASCENDING)
    self.ui.filtermodelVariants.set_visible_func(filter_variants_cb)
    self.on_actionRefresh_activate(None)
    self.on_cboLanguages_changed(None)
    # Set various properties
    self.ui.winMain.set_title(APP_NAME)
    self.ui.winMain.set_icon_from_file(FILE_ICON)
    self.ui.winMain.set_application(self.application)
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

  def _get_current_variant_name(self):
    """Return the name for the currently selected variant"""
    return self.modelVariants.get_name(
      self.ui.filtermodelVariants.convert_iter_to_child_iter(
      self.ui.sortmodelVariants.convert_iter_to_child_iter(
      self.ui.cboVariants.get_active_iter())))

  def on_cboLanguages_changed(self, widget):
    """Update widgets after a language change"""
    if self.ui.cboLanguages.get_sensitive() and \
        self.ui.cboLanguages.get_active_iter() and \
        self._get_current_language_engine() != self.ui.lblEngineName.get_text():
      self.on_optionVoice_toggled(widget)

  def on_optionVoice_toggled(self, widget):
    """Refresh variants for language or gender change"""
    current_engine = self._get_current_language_engine()
    self.ui.lblEngineName.set_text(current_engine)
    if self.backend.engines.has_key(current_engine):
      has_gender = self.backend.engines[current_engine].has_gender
    else:
      # This shouldn't happen
      has_gender = False
    # Set widgets gender sensitive
    self.ui.lblVoice.set_sensitive(has_gender)
    self.ui.optionVoiceMale.set_sensitive(has_gender)
    self.ui.optionVoiceFemale.set_sensitive(has_gender)
    # Update variants list
    self.ui.filtermodelVariants.refilter()
    self.ui.cboVariants.set_tooltip_text(
      '%d variant(s) available' % len(self.ui.filtermodelVariants))
    if self.ui.cboVariants.get_active() == -1:
      # Position the variant again to the normal voice variant
      treepath = self.modelVariants.get_row_from_description(
        self.modelVariants.NORMAL_VOICE_DESCRIPTION).path
      self.ui.cboVariants.set_active(int(
        self.ui.sortmodelVariants.convert_child_path_to_path(
        treepath).to_string()))

  def on_actionClipboard_activate(self, action):
    """Cut and copy the selected text or paste it"""
    bEditable = self.ui.txtText.get_editable()
    if action is self.ui.actionCut:
      self.ui.bufferText.cut_clipboard(self.clipboard, bEditable)
    elif action is self.ui.actionCopy:
      self.ui.bufferText.copy_clipboard(self.clipboard)
    elif action is self.ui.actionPaste:
      self.ui.bufferText.paste_clipboard(self.clipboard, None, bEditable)

  def on_actionPlay_activate(self, action):
    """Play the text in the buffer"""
    self.ui.actionPlayStop.set_active(True)

  def on_actionStop_activate(self, action):
    """Stop any previous play"""
    self.ui.actionPlayStop.set_active(False)

  def on_actionPlayStop_toggled(self, action):
    """Play or stop play"""
    if self.ui.actionPlayStop.get_active():
      # Play the text
      self.backend.set_current_engine(self._get_current_language_engine())
      self.backend.play(
        text=self.ui.bufferText.get_text(self.ui.bufferText.get_start_iter(),
          self.ui.bufferText.get_end_iter(), False),
        language=self._get_current_language_name(),
        variant=self._get_current_variant_name())
      self.ui.actionPause.set_active(False)
      self.ui.actionPause.set_sensitive(True)
    else:
      # Stop any previous play
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
    self.modelLanguages.clear()
    for obj_engine in self.backend.engines.values():
      # Load languages only for enabled engines
      if obj_engine.enabled:
        for language in obj_engine.get_languages():
          self.modelLanguages.add(
            engine=obj_engine.name,
            description='%s%s' % (
              language[KEY_LANGUAGE],
              self.backend.settings.is_debug() and \
              ' (%s)' % language[KEY_NAME] or ''),
            name=language[KEY_NAME]
            )
    # Enable or disable widgets if at least a language is available
    enabled_engines = self.modelLanguages.count() > 0
    self.ui.actionPlayStop.set_sensitive(enabled_engines)
    self.ui.actionPause.set_sensitive(enabled_engines)
    self.ui.actionRecord.set_sensitive(enabled_engines)
    self.ui.actionPlay.set_sensitive(enabled_engines)
    self.ui.actionStop.set_sensitive(enabled_engines)
    self.ui.cboLanguages.set_sensitive(enabled_engines)
    self.ui.lblLanguage.set_sensitive(enabled_engines)
    self.ui.lblVoice.set_sensitive(enabled_engines)
    self.ui.optionVoiceMale.set_sensitive(enabled_engines)
    self.ui.optionVoiceFemale.set_sensitive(enabled_engines)
    self.ui.lblEngine.set_sensitive(enabled_engines)
    self.ui.lblEngineName.set_sensitive(enabled_engines)
    self.ui.cboLanguages.set_tooltip_text('%d languages available' % 
      self.modelLanguages.count())
    # Add dummy option
    if self.modelLanguages.count() == 0:
      self.modelLanguages.add('', 'No enabled engines', '')
      self.ui.lblEngineName.set_text('Unknown')
    # Select the first item
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
    self.ui.actionPause.set_sensitive(False)
