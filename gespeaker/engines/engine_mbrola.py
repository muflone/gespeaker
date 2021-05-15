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

import logging
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
KEY_ESPEAK_GENDER = 'gender'
KEY_ESPEAK_MBROLA = 'mbrola'


class EngineMBROLA(EngineBase):
    name = 'eSpeak + MBROLA'
    required_executables = ('espeak', 'paplay')

    def __init__(self, settings):
        """
        Initialize the engine
        """
        super(self.__class__, self).__init__(settings, globals())
        self.dir_languages = '/usr/share/espeak-data/voices/mb'
        self.dir_mbrola_voices = '/usr/share/mbrola'

    def get_languages(self):
        """
        Get the list of all the supported languages
        """
        result = super(self.__class__, self).get_languages()
        for filename in os.listdir(self.dir_languages):
            filepath = os.path.join(self.dir_languages, filename)
            if not os.path.isdir(filepath):
                # Get and add new language from filename
                new_language = self.get_language_from_filename(filepath)
                if new_language:
                    result.append(new_language)
        return result

    def get_language_from_filename(self, filename):
        """
        Get language information from the specified filename
        """
        info = None
        # Only process files whose size is less than max file size
        if os.path.getsize(filename) <= MAX_FILE_SIZE:
            with open(filename, 'r') as f:
                info = {KEY_ENGINE: self.name,
                        KEY_NAME: os.path.basename(filename),
                        KEY_GENDER: '',
                        KEY_ESPEAK_MBROLA: ''}
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
                            description = description.replace('-mbrola-', ' ')
                            description = description.replace('mbrola-', '')
                            description = description.replace('-mbrola', '')
                            description = description.replace('-mb-', ' ')
                            description = description.replace('en-', '')
                            description = description.title()
                            description = description.replace('Us ', 'US ')
                            info[KEY_LANGUAGE] = description
                        elif key == KEY_ESPEAK_GENDER:
                            # Save the gender
                            info[KEY_GENDER] = values[1]
                        elif key == KEY_ESPEAK_MBROLA:
                            # Save the MBROLA data file
                            info[KEY_ESPEAK_MBROLA] = values[1]
        # Check if the MBROLA data file exists
        dir_voice = os.path.join(self.dir_mbrola_voices,
                                 info[KEY_ESPEAK_MBROLA])
        if info[KEY_ESPEAK_MBROLA]:
            if os.path.isdir(dir_voice):
                if os.path.isfile(os.path.join(dir_voice,
                                               info[KEY_ESPEAK_MBROLA])):
                    return info
                else:
                    # MBROLA voice file not found
                    mbrola_filename = os.path.join(dir_voice,
                                                   info[KEY_ESPEAK_MBROLA])
                    logging.debug('MBROLA data file {FILE} not found for '
                                  'voice {VOICE}'.format(FILE=mbrola_filename,
                                                         VOICE=info[KEY_NAME]))
            else:
                # MBROLA voice directory not found
                logging.debug('MBROLA data directory {DIRECTORY} not found '
                              'for voice {VOICE}'.format(DIRECTORY=dir_voice,
                                                         VOICE=info[KEY_NAME]))
            return None

    def play(self, text, language, on_play_completed):
        """
        Play a text using the specified language
        """
        super(self.__class__, self).play(text, language, on_play_completed)
        espeak_arguments = ['espeak', '--stdout', '-v', language]
        logging.debug(espeak_arguments)
        self.process_speaker = subprocess.Popen(args=espeak_arguments,
                                                stdin=subprocess.PIPE,
                                                stdout=subprocess.PIPE)
        self.process_speaker.stdin.write(text.encode('utf-8'))
        self.process_speaker.stdin.flush()
        self.process_speaker.stdin.close()
        player_arguments = ('paplay',)
        self.process_player = subprocess.Popen(
            args=player_arguments,
            stdin=self.process_speaker.stdout)

    def is_playing(self, on_play_completed):
        """
        Check if the engine is playing and call on_play_completed callback
        when the playing has been completed
        """
        if self.process_player and self.process_player.poll() is not None:
            self.playing = False
            self.process_player = None
        return super(self.__class__, self).is_playing(on_play_completed)

    def stop(self):
        """
        Stop any previous play
        """
        if self.process_player:
            logging.info('Terminate engine {ENGINE} with pid {PID}'.format(
                ENGINE=self.name,
                PID=self.process_player.pid))
            self.process_player.terminate()
        return super(self.__class__, self).stop()

    def pause(self, status_pause):
        """
        Pause a previous play or resume after pause
        """
        super(self.__class__, self).pause(status_pause)
        for process in (self.process_speaker, self.process_player):
            if process:
                logging.info('{STATUS} engine {ENGINE} with pid {PID}'.format(
                    STATUS='Pause' if status_pause else 'Resume',
                    ENGINE=self.name,
                    PID=process.pid))
                psprocess = psutil.Process(process.pid)
                if status_pause:
                    psprocess.suspend()
                else:
                    psprocess.resume()
        return True


engine_classes = (EngineMBROLA,)
