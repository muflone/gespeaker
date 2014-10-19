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
  def __init__(self, application, backend, settings):
    self.application = application
    self.ui = GtkBuilderLoader(FILE_UI_MAIN)
    self.backend = backend
    self.settings = settings
    self.loadUI()
    # Restore the saved size and position
    if self.settings.get_value('width', 0) and self.settings.get_value('height', 0):
      self.ui.winMain.set_default_size(
        self.settings.get_value('width', -1),
        self.settings.get_value('height', -1))
    if self.settings.get_value('left', 0) and self.settings.get_value('top', 0):
      self.ui.winMain.move(
        self.settings.get_value('left', 0),
        self.settings.get_value('top', 0))
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
      return model.get_value(iter, self.modelVariants.COL_ENGINE) in (current_engine, '') and \
        model.get_value(iter, self.modelVariants.COL_GENDER) in genders
    # Load available languages
    self.modelLanguages = ModelLanguages(self.ui.modelLanguages)
    for language in self.backend.get_languages():
      self.modelLanguages.add(
        engine=language[KEY_ENGINE],
        description='%s (%s)' % (language[KEY_LANGUAGE], language[KEY_NAME]),
        name=language[KEY_NAME]
        )
    self.ui.sortmodelLanguages.set_sort_column_id(
      self.modelLanguages.COL_DESCRIPTION, Gtk.SortType.ASCENDING)
    self.ui.cboLanguages.set_active(0)
    # Load available variants
    self.modelVariants = ModelVariants(self.ui.modelVariants)
    self.modelVariants.clear()
    for language in self.backend.get_variants():
      self.modelVariants.add(
        engine=language[KEY_ENGINE],
        description='%s (%s)' % (language[KEY_LANGUAGE], language[KEY_NAME]),
        name=language[KEY_NAME],
        gender=language[KEY_GENDER]
        )
    self.ui.sortmodelVariants.set_sort_column_id(
      self.modelVariants.COL_DESCRIPTION, Gtk.SortType.ASCENDING)
    self.ui.filtermodelVariants.set_visible_func(filter_variants_cb)
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
    # Save settings for window size
    self.settings.set_sizes(self.ui.winMain)
    self.settings.save()
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
    if self._get_current_language_engine() != self.ui.lblEngineName.get_text():
      self.on_optionVoice_toggled(widget)

  def on_optionVoice_toggled(self, widget):
    """Refresh variants for language or gender change"""
    current_engine = self._get_current_language_engine()
    # Check voice engine
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
