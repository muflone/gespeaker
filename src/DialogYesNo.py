##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2010 Fabio Castelli
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
