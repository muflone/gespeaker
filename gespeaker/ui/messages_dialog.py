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

from gespeaker.constants import APP_NAME

class MessagesDialog(object):
  def __init__(self, winParent):
    self.parent = winParent
    self.title = APP_NAME
    self.primary_text = ''
    self.secondary_text = None

  def show_info(self, buttons=Gtk.ButtonsType.OK):
    """Show an information dialog"""
    return self.__show_dialog(message_type=Gtk.MessageType.INFO,
      buttons=buttons)

  def show_warning(self, buttons=Gtk.ButtonsType.OK):
    """Show a warning dialog"""
    return self.__show_dialog(message_type=Gtk.MessageType.WARNING,
      buttons=buttons)

  def show_error(self, buttons=Gtk.ButtonsType.OK):
    """Show an error dialog"""
    return self.__show_dialog(message_type=Gtk.MessageType.ERROR,
      buttons=buttons)

  def show_question(self, buttons=Gtk.ButtonsType.OK_CANCEL):
    """Show a question dialog"""
    return self.__show_dialog(message_type=Gtk.MessageType.QUESTION,
      buttons=buttons)

  def show_simple(self, buttons=Gtk.ButtonsType.OK):
    """Show a simple dialog with no icons"""
    return self.__show_dialog(message_type=Gtk.MessageType.OTHER,
      buttons=buttons)

  def __show_dialog(self, message_type, buttons):
    """Create and show the dialog"""
    dialog = Gtk.MessageDialog(
      parent=self.parent,
      flags=Gtk.DialogFlags.MODAL,
      message_type=message_type,
      buttons=buttons,
      text=self.primary_text,
      secondary_text=self.secondary_text
    )
    if self.title:
      dialog.set_title(self.title)
    dialog.set_transient_for(self.parent)
    result = dialog.run()
    dialog.destroy()
    return result
