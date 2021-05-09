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
import tempfile

import gtts
import psutil

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import (KEY_ENGINE,
                                    KEY_NAME,
                                    KEY_LANGUAGE,
                                    KEY_GENDER)


class EngineGoogleTTS(EngineBase):
    name = 'Google TTS'
    required_executables = ('mpg123',)
    required_modules = ('gtts',)

    def __init__(self, settings):
        """
        Initialize the engine
        """
        super(self.__class__, self).__init__(settings, globals())
        self._tmp_filename = None

    def get_languages(self):
        """
        Get the list of all the supported languages
        """
        result = super(self.__class__, self).get_languages()
        # Languages map for gender
        languages_map = {
            'male': (
                'af', 'sq', 'hy', 'bn', 'bs', 'ca', 'hr', 'eo', 'et', 'is',
                'it', 'ko', 'la', 'lv', 'mk', 'pl', 'sr', 'sw', 'cy'),
            'female': ('ar', 'cs', 'da', 'nl', 'en', 'tl', 'fi', 'fr', 'de',
                       'el', 'gu', 'hi', 'hu', 'id', 'ja', 'jw', 'kn', 'km',
                       'ml', 'mr', 'ne', 'nl', 'no', 'pt', 'ro', 'ru', 'si',
                       'sk', 'es', 'su', 'sv', 'ta', 'te', 'th', 'tr', 'uk',
                       'ur', 'vi', 'zh', 'zh-cn', 'zh-tw', 'en-us', 'en-ca',
                       'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in', 'en-ie',
                       'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz', 'fr-ca',
                       'fr-fr', 'pt-br', 'pt-pt', 'es-es', 'es-us')
        }
        # Get gTTS languages
        try:
            languages = gtts.lang.tts_langs()
            for name, description in languages.items():
                new_language = {KEY_ENGINE: self.name,
                                KEY_NAME: name,
                                KEY_LANGUAGE: description,
                                KEY_GENDER: 'unknown'}
                for gender in 'male', 'female':
                    if name in languages_map[gender]:
                        new_language[KEY_GENDER] = gender
                        break
                result.append(new_language)
        except RuntimeError:
            # No languages returned
            pass
        return result

    def play(self, text, language, on_play_completed):
        """
        Play a text using the specified language
        """
        super(self.__class__, self).play(text, language, on_play_completed)
        self._tmp_filename = \
            tempfile.mkstemp(prefix='gespeaker_', suffix='.mp3')[1]
        self.process_speaker = gtts.gTTS(text=text,
                                         lang=language,
                                         lang_check=False)
        self.process_speaker.save(self._tmp_filename)
        self.process_speaker = None

        arguments = ['mpg123', '-q', self._tmp_filename]
        self.settings.debug_line(arguments)
        self.process_player = subprocess.Popen(args=arguments)

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
            # Show terminate message when debug is activated
            self.settings.debug_line(
                'Terminate engine {ENGINE} with pid {PID}'.format(
                    ENGINE=self.name,
                    PID=self.process_player.pid))
            self.process_player.terminate()
        # Remove stale temporary file
        if os.path.isfile(self._tmp_filename):
            os.remove(self._tmp_filename)
        return super(self.__class__, self).stop()

    def pause(self, status_pause):
        """
        Pause a previous play or resume after pause
        """
        super(self.__class__, self).pause(status_pause)
        for process in (self.process_speaker, self.process_player):
            if process:
                # Show pause message when debug is activated
                self.settings.debug_line(
                    '{STATUS} engine {ENGINE} with pid {PID}'.format(
                        STATUS='Pause' if status_pause else 'Resume',
                        ENGINE=self.name,
                        PID=process.pid))
                psprocess = psutil.Process(process.pid)
                if status_pause:
                    psprocess.suspend()
                else:
                    psprocess.resume()
        return True


engine_classes = (EngineGoogleTTS,)
