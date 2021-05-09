##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2021 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from gi.repository import Gtk
from gi.repository import Gio

from gespeaker.constants import APP_ID
from gespeaker.functions import get_ui_file
from gespeaker.gtkbuilder_loader import GtkBuilderLoader
from gespeaker.backend import Backend
from gespeaker.ui.main import MainWindow


class Application(Gtk.Application):
    def __init__(self, settings):
        super(self.__class__, self).__init__(application_id=APP_ID)
        self.backend = Backend(settings)
        self.settings = settings
        self.connect("activate", self.activate)
        self.connect('startup', self.startup)
        self.ui = None

    def startup(self, application):
        """
        Configure the application during the startup
        """
        self.ui = MainWindow(self, self.backend)
        # Add the actions related to the app menu
        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.on_app_about_activate)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", self.on_app_quit_activate)
        self.add_action(action)
        # Add the app menu
        builder = GtkBuilderLoader(get_ui_file('appmenu.ui'))
        self.set_app_menu(builder.app_menu)

    def activate(self, application):
        """
        Execute the application
        """
        self.ui.run()

    def on_app_about_activate(self, action, data):
        """
        Show the about dialog from the app menu
        """
        self.ui.on_action_about_activate(action)

    def on_app_quit_activate(self, action, data):
        """
        Quit the application from the app menu
        """
        self.ui.on_action_quit_activate(action)
