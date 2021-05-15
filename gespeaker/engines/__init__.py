##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2021 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import importlib
import logging


def detect_engines():
    """
    Dynamic import of engines modules
    """
    engines = {}
    engine_modules = ('engine_dummy',
                      'engine_espeak',
                      'engine_mbrola',
                      'engine_google_tts')

    logging.debug('Detecting available engines')
    # Dynamic import of engines modules
    for module_name in engine_modules:
        try:
            module = importlib.import_module(
                'gespeaker.engines.{MODULE}'.format(MODULE=module_name))
            engine_classes = getattr(module, 'engine_classes')
            # Cycle each engine class
            for engine_class in engine_classes:
                if engine_class.check_requirements():
                    engines[engine_class.name] = engine_class
                else:
                    logging.info('Skipping engine {ENGINE} for unmet '
                                 'requirements'.format(ENGINE=module_name))
        except ImportError:
            logging.info('Skipping engine {ENGINE}'.format(ENGINE=module_name))
    return engines
