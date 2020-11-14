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

import os
import subprocess

import psutil

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import (KEY_ENGINE,
                                    KEY_NAME,
                                    KEY_LANGUAGE,
                                    KEY_GENDER)

MAX_FILE_SIZE = 2000

KEY_ESPEAK_NAME = 'name'

DIR_VARIANTS = '!v'
DIR_MBROLA = 'mb'
DIR_TEST = 'test'


class EngineEspeak(EngineBase):
    name = 'eSpeak'
    required_executables = ('espeak',)

    def __init__(self, settings):
        """
        Initialize the engine
        """
        super(self.__class__, self).__init__(settings, globals())
        self.include_test_voices = False
        self.dir_languages = '/usr/share/espeak-data/voices'

    def get_languages(self):
        """
        Get the list of all the supported languages
        """
        result = super(self.__class__, self).get_languages()
        self.get_languages_from_path(self.dir_languages, result)
        return result

    def get_languages_from_path(self, path, languages):
        """
        Get all the languages from the specified path
        """
        for filename in os.listdir(path):
            # Skip variants and MBROLA voices
            # If requested, also skip test voices
            if filename not in (DIR_VARIANTS, DIR_MBROLA) and \
                    (self.include_test_voices or filename != DIR_TEST):
                filepath = os.path.join(path, filename)
                if os.path.isdir(filepath):
                    # Iter each subdirectory
                    self.get_languages_from_path(filepath, languages)
                else:
                    # Get and add new language from filename
                    new_language = self.get_language_from_filename(filepath)
                    if new_language:
                        languages.append(new_language)
                        new_language = dict(new_language)
                        new_language[KEY_NAME] = '{LANGUAGE}+12'.format(
                            LANGUAGE=new_language[KEY_NAME])
                        new_language[KEY_GENDER] = 'female'
                        languages.append(new_language)

    def get_language_from_filename(self, filename):
        """
        Get language information from the specified filename
        """
        info = None
        # Only process files whose size is less than max file size
        if os.path.getsize(filename) <= MAX_FILE_SIZE:
            with open(filename, 'r') as f:
                info = {}
                info[KEY_ENGINE] = self.name
                info[KEY_NAME] = os.path.basename(filename)
                info[KEY_GENDER] = 'male'
                # Extract information from the voice file
                for line in f.readlines():
                    # Remove newline characters
                    line = line.replace('\r', '')
                    line = line.replace('\n', '')
                    if ' ' in line:
                        values = line.split(' ')
                        key = values[0]
                        if key == KEY_ESPEAK_NAME:
                            # Save the language name
                            description = values[1]
                            description = description.replace('-', ' ')
                            description = description.replace('_', ' ')
                            info[KEY_LANGUAGE] = description.title()
        return info

    def play(self, text, language, on_play_completed):
        """
        Play a text using the specified language
        """
        super(self.__class__, self).play(text, language, on_play_completed)
        arguments = ['espeak', '-v']
        arguments.append(language)
        self.settings.debug_line(arguments)
        self.process_speaker = subprocess.Popen(args=arguments,
                                                stdin=subprocess.PIPE)
        self.process_speaker.stdin.write(text.encode('utf-8'))
        self.process_speaker.stdin.flush()
        self.process_speaker.stdin.close()

    def is_playing(self, on_play_completed):
        """
        Check if the engine is playing and call on_play_completed callback
        when the playing has been completed
        """
        if self.process_speaker and self.process_speaker.poll() is not None:
            self.playing = False
            self.process_speaker = None
        return super(self.__class__, self).is_playing(on_play_completed)

    def stop(self):
        """
        Stop any previous play
        """
        if self.process_speaker:
            # Show terminate message when debug is activated
            self.settings.debug_line(
                'Terminate engine {ENGINE} with pid {PID}'.format(
                    ENGINE=self.name,
                    PID=self.process_speaker.pid))
            self.process_speaker.terminate()
        return super(self.__class__, self).stop()

    def pause(self, status_pause):
        """
        Pause a previous play or resume after pause
        """
        super(self.__class__, self).pause(status_pause)
        if self.process_speaker:
            # Show pause message when debug is activated
            self.settings.debug_line(
                '{STATUS} engine {ENGINE} with pid {PID}'.format(
                    STATUS='Pause' if status_pause else 'Resume',
                    ENGINE=self.name,
                    PID=self.process_speaker.pid))
            psprocess = psutil.Process(self.process_speaker.pid)
            if status_pause:
                psprocess.suspend()
            else:
                psprocess.resume()
        return True


engine_classes = (EngineEspeak,)
