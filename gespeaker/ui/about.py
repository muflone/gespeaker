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

import logging

from gi.repository.GdkPixbuf import Pixbuf

from gespeaker.constants import (APP_NAME,
                                 APP_VERSION,
                                 APP_DESCRIPTION,
                                 APP_AUTHOR,
                                 APP_AUTHOR_EMAIL,
                                 APP_COPYRIGHT,
                                 APP_URL,
                                 FILE_ICON,
                                 FILE_LICENSE,
                                 FILE_RESOURCES,
                                 FILE_TRANSLATORS)
from gespeaker.functions import get_ui_file, readlines
from gespeaker.gtkbuilder_loader import GtkBuilderLoader


class AboutWindow(object):
    def __init__(self, parent_window, show=False):
        logging.debug('Loading about dialog')
        # Retrieve the translators list
        translators = []
        for line in readlines(FILE_TRANSLATORS, False):
            if ':' in line:
                line = line.split(':', 1)[1]
            line = line.replace('(at)', '@').strip()
            if line not in translators:
                translators.append(line)
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('about.glade'))
        # Set various properties
        self.ui.dialog_about.set_program_name(APP_NAME)
        self.ui.dialog_about.set_version('Version {VERSION}'.format(
            VERSION=APP_VERSION))
        self.ui.dialog_about.set_comments(APP_DESCRIPTION)
        self.ui.dialog_about.set_website(APP_URL)
        self.ui.dialog_about.set_copyright(APP_COPYRIGHT)
        self.ui.dialog_about.set_authors(
            ['{AUTHOR} <{EMAIL}>'.format(AUTHOR=APP_AUTHOR,
                                         EMAIL=APP_AUTHOR_EMAIL)])
        self.ui.dialog_about.set_license(
            '\n'.join(readlines(FILE_LICENSE, True)))
        self.ui.dialog_about.set_translator_credits('\n'.join(translators))
        # Retrieve the external resources links
        for line in readlines(FILE_RESOURCES, False):
            resource_type, resource_url = line.split(':', 1)
            self.ui.dialog_about.add_credit_section(resource_type,
                                                    (resource_url,))
        icon_logo = Pixbuf.new_from_file(FILE_ICON)
        self.ui.dialog_about.set_logo(icon_logo)
        self.ui.dialog_about.set_transient_for(parent_window)
        # Optionally show the dialog
        if show:
            self.show()

    def show(self):
        """
        Show the About dialog
        """
        logging.debug('Showing about dialog')
        self.ui.dialog_about.run()
        self.ui.dialog_about.hide()

    def destroy(self):
        """
        Destroy the About dialog
        """
        logging.debug('Closing about dialog')
        self.ui.dialog_about.destroy()
