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

import ConfigParser
import os
from xdg.BaseDirectory import xdg_config_home
from gettext import gettext as _

cmdEspeak = '/usr/bin/espeak'
argsEspeak = '-a %v -p %p -s %s -g %d -v %l -f %f'
cmdMbrola = '/usr/bin/mbrola'
argsMbrola = '-e %l -'

config = None
confdir = os.path.join(xdg_config_home, 'gespeaker')

conffile = os.path.join(confdir, 'settings.conf')
pluginsfile = os.path.join(confdir, 'plugins.conf')
__sectionSettings = 'settings'
__sectionWindowSize = 'window size'
__sectionVoiceSetting = 'voice settings'
__sectionMbrola = 'mbrola'
__defSettings = None

if not os.path.exists(confdir):
  os.mkdir(confdir)

def load(filename=conffile):
  "Load settings from the configuration file"
  global config
  config = ConfigParser.RawConfigParser()
  loadDefaults()
  if os.path.exists(filename):
    config.read(filename)
  # Settings lookup is made upon __defSettings
  for setting in __defSettings.keys():
    # Add section if doesn't exist
    if not config.has_section(__defSettings[setting][2]):
      config.add_section(__defSettings[setting][2])
    if not config.has_option(__defSettings[setting][2], setting):
      config.set(__defSettings[setting][2], setting, str(__defSettings[setting][1]))

def loadDefaults():
  global __defSettings
  strbool = lambda value: value == 'True'
  __defSettings = {
    'PlayMethod': [int, 0, __sectionSettings],
    'PlayCommand': [str, 'aplay', __sectionSettings],
    'PlayWelcomeText': [strbool, True, __sectionSettings],
    'UseCustomWelcome': [strbool, False, __sectionSettings],
    'WelcomeText': [str, _('Welcome in Gespeaker'), __sectionSettings],
    'SaveVoiceSettings': [strbool, True, __sectionSettings],
    'SaveWindowSize': [strbool, False, __sectionSettings],
    'SingleRecord': [strbool, True, __sectionSettings],
    'WordWrap': [strbool, False, __sectionSettings],
    'LoadVariants': [strbool, True, __sectionSettings],
    'MainWindowWidth': [int, 440, __sectionWindowSize],
    'MainWindowHeight': [int, 470, __sectionWindowSize],
    'MainWindowLeft': [int, 10, __sectionWindowSize],
    'MainWindowTop': [int, 20, __sectionWindowSize],
    'SettingsExpander': [strbool, True, __sectionWindowSize],
    'VoiceVolume': [int, 100, __sectionVoiceSetting],
    'VoicePitch': [int, 50, __sectionVoiceSetting],
    'VoiceSpeed': [int, 170, __sectionVoiceSetting],
    'VoiceDelay': [int, 10, __sectionVoiceSetting],
    'VoiceTypeMale': [strbool, True, __sectionVoiceSetting],
    'VoiceLanguage': [str, _('default language'), __sectionVoiceSetting],
    'VoicesmbPath': [str, '/usr/share/mbrola/voices', __sectionMbrola]
  }

def save(filename=conffile, clearDefaults=False):
  "Save settings into the configuration file"
  file = open(filename, mode='w')
  if clearDefaults:
    for setting in __defSettings.keys():
      if config.has_option(__defSettings[setting][2], setting):
        if get(setting) == __defSettings[setting][1]:
          config.remove_option(__defSettings[setting][2], setting)
  config.write(file)
  file.close

def get(setting):
  "Returns a specified setting from the configuration or default values"
  if config.has_option(__defSettings[setting][2], setting):
    return __defSettings[setting][0](config.get(__defSettings[setting][2], setting))
  elif __defSettings.has_key(setting):
    return __defSettings[setting][1]
  else:
    print 'unknown setting: %s' % setting

def default(setting):
  "Returns the default value for a specified setting"
  if __defSettings.has_key(setting):
    return __defSettings[setting][1]

def set(setting, value):
  "Sets a specific setting to the value."
  #" If it's the default then delete it"
  #if __defSettings.has_key(setting) and value == __defSettings[setting][1]:
  #  config.remove_option(__defSettings[setting][2], setting)
  #else:
  #print __defSettings[setting][2], setting, str(value)
  config.set(__defSettings[setting][2], setting, str(value))
