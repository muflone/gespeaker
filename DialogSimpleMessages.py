##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import gtk

def ShowDialogGeneric(type, title=None, text=None, showOk=True):
  dialog = gtk.MessageDialog(
    parent=None, flags=gtk.DIALOG_MODAL, type=type, 
    buttons=showOk and gtk.BUTTONS_OK or gtk.BUTTONS_NONE,
    message_format=text
  )
  if title:
    dialog.set_title(title)
  dialog.connect('response', lambda self, args: self.destroy())
  dialog.run()

def ShowDialogWarning(title=None, text=None, showOk=True):
  return ShowDialogGeneric(gtk.MESSAGE_WARNING, title=title, text=text, showOk=showOk)

def ShowDialogError(title=None, text=None, showOk=True):
  return ShowDialogGeneric(gtk.MESSAGE_ERROR, title=title, text=text, showOk=showOk)

def ShowDialogInfo(title=None, text=None, showOk=True):
  return ShowDialogGeneric(gtk.MESSAGE_INFO, title=title, text=text, showOk=showOk)

def ShowDialogQuestion(title=None, text=None, showOk=True):
  return ShowDialogGeneric(gtk.MESSAGE_QUESTION, title=title, text=text, showOk=showOk)
