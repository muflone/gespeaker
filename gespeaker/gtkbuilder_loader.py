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

import gettext
import logging
import xml.etree.ElementTree

from gi.repository import Gtk


class GtkBuilderLoader(object):
    def __init__(self, *ui_files):
        """
        Load one or more ui files for GtkBuilder
        """
        self.__widgets = {}
        self.builder = Gtk.Builder()
        for ui_filename in ui_files:
            self.builder.add_from_file(ui_filename)
            self._translate_widgets(
                xml=xml.etree.ElementTree.parse(ui_filename).getroot())

    def __getattr__(self, key):
        """
        Get a widget from GtkBuilder using class member name
        """
        if key not in self.__widgets:
            self.__widgets[key] = self.builder.get_object(key)
            assert (self.__widgets[key])
        return self.__widgets[key]

    def get_object(self, key):
        """
        Get a widget from GtkBuilder using a method
        """
        return self.__getattr__(key)

    def get_objects(self):
        """Get the widgets list from GtkBuilder"""
        return self.builder.get_objects()

    def get_objects_by_type(self, type):
        """Get the widgets list with a specific type from GtkBuilder"""
        return [w for w in self.get_objects() if isinstance(w, type)]

    def connect_signals(self, handlers):
        """
        Connect all the Gtk signals to a group of handlers
        """
        self.builder.connect_signals(handlers)

    def _translate_widgets(self, xml):
        """
        Translate widgets by cycling objects from the XML document recursively
        """
        # Cycle over every object in the xml node
        for item in xml.findall('object'):
            widget = self.get_object(item.attrib['id'])
            # Find all properties for the object
            for prop in item.findall('property'):
                # Translatable strings have context attribute
                if 'context' in prop.attrib:
                    if '.' in prop.attrib['context']:
                        # Message with domain.context
                        domain, context = prop.attrib['context'].split('.', 1)
                        message = '{CONTEXT}\x04{MESSAGE}'.format(
                            CONTEXT=context,
                            MESSAGE=prop.text)
                    else:
                        # Message with no context (domain only)
                        domain = prop.attrib['context']
                        message = prop.text
                    # Translate message
                    translation = gettext.dgettext(domain=domain,
                                                   message=message)
                    # Set the widget properties
                    if prop.attrib['name'] == 'label':
                        # Translate label from widget
                        widget.set_label(translation)
                    else:
                        # Unexpected property for widget
                        logging.error(
                            'Unexpected property "{PROPERTY}" '
                            'to translate from widget "{WIDGET}"'
                            ''.format(PROPERTY=prop.attrib['name'],
                                      WIDGET=item.attrib['id']))
            # Process every children in object
            for child in item.findall('child'):
                self._translate_widgets(child)
