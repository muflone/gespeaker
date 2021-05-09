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

import os.path
from gi.repository import Gtk

from gespeaker.constants import APP_NAME


class FilesDialog(object):
    def __init__(self, parent_window):
        self.parent = parent_window
        self.title = APP_NAME
        self.filters = []
        self.last_used_filter = None
        self.current_folder = os.path.expanduser('~')

    def show_open(self):
        """
        Show the Open file dialog
        """
        return self.__show_dialog(action=Gtk.FileChooserAction.OPEN)

    def show_save(self):
        """
        Show the Save file dialog
        """
        return self.__show_dialog(action=Gtk.FileChooserAction.SAVE)

    def __show_dialog(self, action):
        """
        Create and show the dialog
        """
        dialog = Gtk.FileChooserDialog(
            parent=self.parent,
            action=action,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.WindowType.TOPLEVEL,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )
        dialog.set_title(self.title)
        dialog.set_transient_for(self.parent)
        dialog.set_local_only(True)
        dialog.set_select_multiple(False)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_create_folders(False)
        dialog.set_current_folder(self.current_folder)
        for new_filter in self.filters:
            dialog.add_filter(new_filter)
        if dialog.run() == Gtk.ResponseType.OK:
            result = dialog.get_filename()
        else:
            result = None
        self.last_used_filter = dialog.get_filter()
        dialog.destroy()
        return result

    def add_filter(self, name, mime_types, patterns):
        """
        Add a new filter for the dialog
        """
        new_filter = Gtk.FileFilter()
        new_filter.set_name(name)
        # Add mime types
        if mime_types:
            for mime_type in mime_types:
                new_filter.add_mime_type(mime_type)
        # Add globing patterns
        if patterns:
            for pattern in patterns:
                new_filter.add_pattern(pattern)
        self.filters.append(new_filter)

    def clear_filters(self):
        """
        Remove every filter
        """
        while len(self.filters) > 0:
            self.filters.pop()
