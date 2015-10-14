#!/usr/bin/env python2
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

import gettext
import locale

from gespeaker.settings import Settings
from gespeaker.app import Application
from gespeaker.constants import *

if __name__ == '__main__':
  # Load domain for translation
  for module in (gettext, locale):
    if hasattr(module, 'bindtextdomain'):
      module.bindtextdomain(DOMAIN_NAME, DIR_LOCALE)
    if hasattr(module, 'textdomain'):
      module.textdomain(DOMAIN_NAME)

  # Load the settings from the configuration file
  settings = Settings()
  settings.load()

  # Start the application
  app = Application(settings)
  app.run(None)
