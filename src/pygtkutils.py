##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
# Copyright: 2009-2015 Fabio Castelli
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
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import gtk

def TextBuffer_get_text(buffer):
  "Return the whole text on the TextBuffer"
  return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())

def Radio_get_active(group):
  "Return the currently active radio button on the group"
  for button in group:
    if button.get_active():
      return button

def Pixbuf_load_file(filename, size=None):
  "Load an image file with the desired size if requested"
  if size and len(size) == 2:
    return gtk.gdk.pixbuf_new_from_file_at_size(filename, size[0], size[1])
  else:
    return gtk.gdk.pixbuf_new_from_file(filename)

def Window_change_cursor(window, cursor, refresh=False):
  "Change a window's cursor and optionally forces the refresh"
  window.set_cursor(cursor and gtk.gdk.Cursor(cursor) or None)
  if refresh:
    gtk.gdk.flush()

def Button_change_stock_description(button, caption, use_underline=None):
  "Change stock button description"
  alignment = button.get_children()[0]
  box = alignment.get_children()[0]
  first, second = box.get_children()
  # Find label
  if type(first) is gtk.Label:
    label = first
  elif type(second) is gtk.Label:
    label = second
  else:
    label = None
  if label:
    label.set_text(caption)
    # Set use_underline
    if use_underline is not None:
      label.set_use_underline(use_underline)

def TreeModel_find_text(model, column, text):
  "Return the path of the found text in the model"
  iter = model.get_iter_first()
  while iter:
    if model.get_value(iter, column) == text:
      return int(model.get_string_from_iter(iter))
    iter = model.iter_next(iter)

def ComboBox_set_item_from_text(combo, column, text):
  path = TreeModel_find_text(combo.get_model(), column, text)
  if not path is None:
    combo.set_active(path)
    return path

def ComboBox_get_text(combo, column):
  active = combo.get_active()
  if not active is None:
    return combo.get_model()[active][column]
