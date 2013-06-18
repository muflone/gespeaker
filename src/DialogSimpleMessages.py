##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2013 Fabio Castelli
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
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

import gtk

def ShowDialogGeneric(type, title=None, text=None, showOk=True, icon=None):
  dialog = gtk.MessageDialog(
    parent=None, flags=gtk.DIALOG_MODAL, type=type, 
    buttons=showOk and gtk.BUTTONS_OK or gtk.BUTTONS_NONE,
    message_format=text
  )
  if title:
    dialog.set_title(title)
  if icon:
    dialog.set_icon_from_file(icon)
  dialog.connect('response', lambda self, args: self.destroy())
  dialog.run()

def ShowDialogWarning(title=None, text=None, showOk=True, icon=None):
  return ShowDialogGeneric(gtk.MESSAGE_WARNING, title=title, text=text, showOk=showOk, icon=icon)

def ShowDialogError(title=None, text=None, showOk=True, icon=None):
  return ShowDialogGeneric(gtk.MESSAGE_ERROR, title=title, text=text, showOk=showOk, icon=icon)

def ShowDialogInfo(title=None, text=None, showOk=True, icon=None):
  return ShowDialogGeneric(gtk.MESSAGE_INFO, title=title, text=text, showOk=showOk, icon=icon)

def ShowDialogQuestion(title=None, text=None, showOk=True, icon=None):
  return ShowDialogGeneric(gtk.MESSAGE_QUESTION, title=title, text=text, showOk=showOk, icon=icon)
