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

import Plugin
import dbus

class MainClass(Plugin.Plugin):
    description = _('Emesene voice plugin for Gespeaker')
    authors = {'Fabio Castelli': 'muflone@vbsimple.net',}
    website = 'http://code.google.com/p/gespeaker/'
    displayName = _('Gespeaker via DBUS')
    name = 'Gespeaker'
    require = []
    def __init__(self, controller, msn):
        Plugin.Plugin.__init__(self, controller, msn)
        self.newMsgId = None
        bus = dbus.SessionBus()
        self.Gespeaker = bus.get_object('org.gtk.gespeaker', '/org/gtk/gespeaker/ui')

    def start(self):
        self.newMsgId = self.connect('switchboard::message', self.newMsg)
        self.enabled = True

    def stop(self):
        self.disconnect(self.newMsgId)
        self.enabled = False

    def check(self):
        return (True, 'Ok')

    def newMsg(self, msn, switchboard, signal, args, stamp=None):
        email, nick, text, format, charset, p4c = args
        self.Gespeaker.get_dbus_method('play_text', 'org.gtk.gespeaker.ui')(text)
        return

