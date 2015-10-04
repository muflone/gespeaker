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

import importlib

engine_modules = (
  'engine_dummy',
  'engine_espeak',
  'engine_mbrola',
  'engine_google_tts',
)

def detect_engines():
  """Dynamic import of engines modules"""
  engines = {}
  # Dynamic import of engines modules
  for module_name in engine_modules:
    try:
      module = importlib.import_module('gespeaker.engines.%s' % module_name)
      engine_classes = getattr(module, 'engine_classes')
      # Cycle each engine class
      for engine_class in engine_classes:
        if engine_class.check_requirements():
          engines[engine_class.name] = engine_class
        else:
          print ('  > Skipping engine %s for unmet requirements' % module_name)
    except ImportError:
      print ('  > Skipping engine %s' % module_name)
  return engines
