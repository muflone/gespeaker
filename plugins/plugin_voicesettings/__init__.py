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

PLUGIN_NAME = 'Save voice settings'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Save voice settings on close'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = ''

import Settings
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_SaveVoiceSettings(GespeakerPlugin):
  def on_uiready(self, ui):
    self.ui = ui
  
  def on_closing(self):
    # Save voice settings if SaveVoiceSettings is set
    if Settings.get('SaveVoiceSettings'):
      self.logger('Save voice settings')
      Settings.set('VoiceVolume', int(self.ui.hscVolume.get_value()))
      Settings.set('VoicePitch', int(self.ui.hscPitch.get_value()))
      Settings.set('VoiceSpeed', int(self.ui.hscSpeed.get_value()))
      Settings.set('VoiceDelay', int(self.ui.hscDelay.get_value()))
      Settings.set('VoiceTypeMale', self.ui.radioVoiceMale.get_active())
      # Save language only if different from defaultLanguageIndex
      active = self.ui.cboLanguages.get_active()
      if not active is None:
        language = self.ui.cboLanguages.get_model()[active][0]
        language = self.ui.listLanguages[self.ui.cboLanguages.get_active()][0]
        Settings.set('VoiceLanguage', language)

plugin = GespeakerPlugin_SaveVoiceSettings(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
