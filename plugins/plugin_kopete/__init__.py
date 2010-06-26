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

PLUGIN_NAME = 'Kopete'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Kopete plugin'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = 'http://www.ubuntutrucchi.it/'

from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Kopete(GespeakerPlugin):
  pass

plugin = GespeakerPlugin_Kopete(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
