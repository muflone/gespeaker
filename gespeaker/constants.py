##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2009-2015 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import sys
import os.path
from xdg import BaseDirectory

# Application constants
APP_NAME = 'Gespeaker'
APP_VERSION = '2.0.0'
APP_DESCRIPTION = 'A GTK frontend for espeak'
APP_ID = 'gespeaker.muflone.com'
APP_URL = 'http://www.muflone.com/gespeaker'
APP_AUTHOR = 'Fabio Castelli (Muflone)'
APP_AUTHOR_EMAIL = 'muflone@vbsimple.net'
APP_COPYRIGHT = 'Copyright 2009-2015 %s' % APP_AUTHOR
# Other constants
DOMAIN_NAME = 'gespeaker'
VERBOSE_LEVEL_QUIET = 0
VERBOSE_LEVEL_NORMAL = 1
VERBOSE_LEVEL_MAX = 2

# Paths constants
# If there's a file data/gespeaker.png then the shared data are searched
# in relative paths, else the standard paths are used
if os.path.isfile(os.path.join('data', 'gespeaker.png')):
  DIR_PREFIX = '.'
  DIR_LOCALE = os.path.join(DIR_PREFIX, 'locale')
  DIR_DOCS = os.path.join(DIR_PREFIX, 'doc')
else:
  DIR_PREFIX = os.path.join(sys.prefix, 'share', 'gespeaker')
  DIR_LOCALE = os.path.join(sys.prefix, 'share', 'locale')
  DIR_DOCS = os.path.join(sys.prefix, 'share', 'doc', 'gespeaker')
# Set the paths for the folders
DIR_DATA = os.path.join(DIR_PREFIX, 'data')
DIR_UI = os.path.join(DIR_PREFIX, 'ui')
DIR_SETTINGS = BaseDirectory.save_config_path(DOMAIN_NAME)
DIR_ICONS = os.path.join(DIR_DATA, 'icons')
# Set the paths for the UI files
FILE_UI_MAIN = os.path.join(DIR_UI, 'main.glade')
FILE_UI_ABOUT = os.path.join(DIR_UI, 'about.glade')
FILE_UI_SERVICES = os.path.join(DIR_UI, 'services.glade')
FILE_UI_PREFERENCES = os.path.join(DIR_UI, 'preferences.glade')
FILE_UI_APPMENU = os.path.join(DIR_UI, 'appmenu.ui')
# Set the paths for the data files
FILE_ICON = os.path.join(DIR_DATA, 'gespeaker.png')
FILE_TRANSLATORS = os.path.join(DIR_DOCS, 'translators')
FILE_LICENSE = os.path.join(DIR_DOCS, 'license')
FILE_RESOURCES = os.path.join(DIR_DOCS, 'resources')
FILE_GENDER_MALE = os.path.join(DIR_ICONS, 'gender-male.svg')
FILE_GENDER_FEMALE = os.path.join(DIR_ICONS, 'gender-female.svg')
FILE_GENDER_UNKNOWN = os.path.join(DIR_ICONS, 'gender-unknown.svg')
# Set the paths for configuration files
FILE_SETTINGS_NEW = os.path.join(DIR_SETTINGS, 'settings.conf')

# Signals for pause and resume
SIGCONT = 18
SIGSTOP = 19
