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

import os
import sys

__base_path__ = os.path.dirname(os.path.abspath(__file__))
APP_NAME = 'gespeaker'
APP_TITLE = 'Gespeaker'
APP_VERSION = '0.8.1'

PATHS = {
  'locale': [
    '%s/../po' % __base_path__,
    '%s/share/locale' % sys.prefix],
  'ui': [
    '%s/../data/ui' % __base_path__],
  'icons': [
    '%s/../data/icons' % __base_path__],
  'data': [
    '%s/../data' % __base_path__],
  'doc': [
    '%s/../doc' % __base_path__,
    '%s/share/doc/%s' % (sys.prefix, APP_NAME)],
  'plugins': [
    '%s/../plugins' % __base_path__,
    '%s/share/plugins' % sys.prefix]
}

def getPath(key, append = ''):
  "Returns the correct path for the specified key"
  for path in PATHS[key]:
    if os.path.isdir(path):
      if append:
        return os.path.abspath(os.path.join(path, append))
      else:
        return os.path.abspath(path)

def get_app_logo():
  "Returns the path of the icon logo"
  return getPath('icons', '%s.svg' % APP_NAME)

def read_text_file(key, append = ''):
  "Returns the content of the indicated text file"
  try:
    f = open(getPath(key, append), 'r')
    text = f.read()
    f.close()
  except:
    text = ''
  return text
