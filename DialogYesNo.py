##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import gtk

class DialogYesNo(gtk.MessageDialog):
  def __init__(self, message=None, default_button=gtk.RESPONSE_YES):
    super(self.__class__, self).__init__(parent=None, flags=gtk.DIALOG_MODAL, 
      type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO,
      message_format=message)
    self.response = None
    self.set_default_response(default_button == gtk.RESPONSE_YES 
      and gtk.RESPONSE_YES or gtk.RESPONSE_NO)
    self.connect('response', self._response_callback)
  
  def _response_callback(self, *args):
    self.response = args[1]
    self.destroy()
  
  def show(self):
    super(self.__class__, self).run()
    return self.response

  def responseIsYes(self):
    return self.response == gtk.RESPONSE_YES

  def responseIsNo(self):
    return self.response == gtk.RESPONSE_NO

  def responseIsCancel(self):
    return self.response == gtk.RESPONSE_DELETE_EVENT
