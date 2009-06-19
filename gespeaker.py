#!/usr/bin/env python

##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import sys
import gettext
import gtk.glade
import gespeakerUI

APP_NAME = 'gespeaker'
APP_TITLE = 'Gespeaker'
APP_VERSION = '0.1'
LOCALE_DIR = '/usr/share/locale'

if __name__ == '__main__':
  for module in (gettext, gtk.glade):
    module.bindtextdomain(APP_NAME, LOCALE_DIR)
    module.textdomain(APP_NAME)
  main = gespeakerUI.gespeakerUI(APP_NAME, APP_TITLE, APP_VERSION)
