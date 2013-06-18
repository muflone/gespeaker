#!/usr/bin/env python
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

import sys
import dbus

# Read pure text from stdin
text = sys.stdin.read()
# Transmit text back to kopete
sys.stdout.write(text)

# Get dbus interface
bus = dbus.SessionBus()
self.Gespeaker = bus.get_object('org.gtk.gespeaker', '/org/gtk/gespeaker/ui')
self.Gespeaker.get_dbus_method('play_text', 'org.gtk.gespeaker.ui')(text)
