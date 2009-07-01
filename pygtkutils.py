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
