#!/usr/bin/wish
##
#   Project: Gespeaker - A GTK frontend for espeak  
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

namespace eval ::Gespeaker {
	proc Init { plugin_dir } {
		::plugins::RegisterPlugin Gespeaker
		::plugins::RegisterEvent Gespeaker chat_msg_received newmessage
		if { 1 > 1 } {
		}
	}

	proc newmessage {event arguments} {
		upvar 2 $arguments args
		upvar 2 $args(msg) msg
		upvar 2 $args(user) user

		# Exclude messages from meself
		if { ($user != [::config::getKey login]) } {
			# Call via dbus-send
			exec dbus-send --type=method_call --dest=org.gtk.gespeaker \
				/org/gtk/gespeaker/ui org.gtk.gespeaker.ui.play_text \
				string:$msg
		}
	}
}
