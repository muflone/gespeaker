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

from gi.repository import GObject

from gespeaker.find_executable import find_executable

KEY_ENGINE = 'engine'
KEY_NAME = 'name'
KEY_LANGUAGE = 'language'
KEY_GENDER = 'gender'


class EngineBase(object):
    required_executables = ()
    required_modules = ()

    @classmethod
    def check_requirements(cls):
        """
        Check the module requirements to enable it
        """
        print('Checking requirements for engine %s' % cls.name)
        # Check for required Python modules to import
        for module_name in cls.required_modules:
            try:
                importlib.import_module(module_name)
            except ImportError:
                print('  > Module %s not found' % module_name)
                return False
        # Check for required executable files
        for executable_name in cls.required_executables:
            if not find_executable(executable_name):
                print('  > Executable %s not found in the path' %
                      executable_name)
                return False
        return True

    def __init__(self, settings, module_globals):
        """
        Initialize the engine
        """
        self.playing = False
        self.settings = settings
        self.enabled = True
        self.process_speaker = None
        self.process_player = None
        # Inject required modules into the module global namespace
        for module_name in self.required_modules:
            module_globals[module_name] = importlib.import_module(module_name)

    def get_languages(self):
        """
        Get the list of all the supported languages
        """
        return []

    def play(self, text, language, on_play_completed):
        """
        Play a text using the specified language
        """
        self.playing = True
        # Add a timer to check when the playing has stopped
        GObject.timeout_add(500, self.is_playing, on_play_completed)

    def is_playing(self, on_play_completed):
        """
        Check if the engine is playing and call on_play_completed callback
        when the playing has been completed
        """
        if self.playing:
            return True
        else:
            # Call the callback if provided
            if on_play_completed:
                on_play_completed()
            # Stop iterations
            return False

    def stop(self):
        """
        Stop any previous play
        """
        self.playing = False

    def pause(self, status):
        """
        Pause a previous play or resume after pause
        """
        return True
