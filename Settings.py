import ConfigParser
import os
from gettext import gettext as _

config = None
confdir = os.path.join(os.path.expanduser('~/.gespeaker'))
conffile = os.path.join(confdir, 'settings.conf')
__sectionSettings = 'settings'
__sectionWindowSize = 'window size'
__sectionVoiceSetting = 'voice settings'
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
    'SettingsExpander': [strbool, True, __sectionWindowSize],
    'VoiceVolume': [int, 100, __sectionVoiceSetting],
    'VoicePitch': [int, 50, __sectionVoiceSetting],
    'VoiceSpeed': [int, 170, __sectionVoiceSetting],
    'VoiceDelay': [int, 10, __sectionVoiceSetting],
    'VoiceTypeMale': [strbool, True, __sectionVoiceSetting],
    'VoiceLanguage': [int, -1, __sectionVoiceSetting]
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
