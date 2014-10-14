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
    self.modelLanguages = ModelLanguages(self.ui.modelLanguages)
    for language in self.backend.get_languages():
      self.modelLanguages.add(
        engine=language[KEY_ENGINE],
        description='%s (%s)' % (language[KEY_LANGUAGE], language[KEY_NAME]),
        name=language[KEY_NAME]
        )
    self.ui.sortmodelLanguages.set_sort_column_id(
      self.modelLanguages.COL_DESCRIPTION, Gtk.SortType.ASCENDING)

    self.modelVariants = ModelVariants(self.ui.modelVariants)
    self.modelVariants.add(engine='', 
      description='Normal voice', name='')
    for language in self.backend.get_variants():
      self.modelVariants.add(
        engine=language[KEY_ENGINE],
        description='%s (%s)' % (language[KEY_LANGUAGE], language[KEY_NAME]),
        name=language[KEY_NAME]
        )
    self.ui.sortmodelVariants.set_sort_column_id(
      self.modelVariants.COL_DESCRIPTION, Gtk.SortType.ASCENDING)

    # Set various properties
    self.ui.winMain.set_title(APP_NAME)
    self.ui.winMain.set_icon_from_file(FILE_ICON)
    self.ui.winMain.set_application(self.application)
    # Connect signals from the glade file to the functions with the same name
    self.ui.connect_signals(self)

  def on_winMain_delete_event(self, widget, event):
    """Close the application"""
    self.on_actionQuit_activate(widget)

  def on_actionAbout_activate(self, widget):
    """Show the about dialog"""
    self.about.show()

  def on_actionQuit_activate(self, widget):
    """Quit the application"""
    # Save settings for window size, intercepted syscalls and visible columns
    self.settings.set_sizes(self.ui.winMain)
    self.settings.save()
    self.about.destroy()
    self.ui.winMain.destroy()
    self.application.quit()
