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
import multiprocessing
import time

import psutil

from gespeaker.engines.base import EngineBase
from gespeaker.engines.base import (KEY_ENGINE,
                                    KEY_NAME,
                                    KEY_LANGUAGE,
                                    KEY_GENDER)


class EngineDummy(EngineBase):
    name = 'Dummy'

    def __init__(self, settings):
        """
        Initialize the engine
        """
        super(self.__class__, self).__init__(settings, globals())

    def get_languages(self):
        """
        Get the list of all the supported languages
        """
        result = super(self.__class__, self).get_languages()
        result.append({
            KEY_ENGINE: self.name,
            KEY_NAME: 'dummy',
            KEY_LANGUAGE: 'A dummy language',
            KEY_GENDER: 'unknown'
        })
        return result

    def play(self, text, language, on_play_completed):
        """
        Play a text using the specified language
        """
        super(self.__class__, self).play(text, language, on_play_completed)
        self.process_speaker = multiprocessing.Process(
            target=self._do_play, args=(text,))
        self.process_speaker.start()

    def _do_play(self, text):
        """
        Play the text
        """
        for letter in text:
            logging.debug(letter)
            time.sleep(0.1)

    def is_playing(self, on_play_completed):
        """
        Check if the engine is playing and call on_play_completed callback
        when the playing has been completed
        """
        if self.process_speaker and not self.process_speaker.is_alive():
            self.playing = False
            self.process_speaker = None
        return super(self.__class__, self).is_playing(on_play_completed)

    def stop(self):
        """
        Stop any previous play
        """
        if self.process_speaker:
            logging.info('Terminate engine {ENGINE} with pid {PID}'.format(
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
            logging.info('{STATUS} engine {ENGINE} with pid {PID}'.format(
                STATUS='Pause' if status_pause else 'Resume',
                ENGINE=self.name,
                PID=self.process_speaker.pid))
            psprocess = psutil.Process(self.process_speaker.pid)
            if status_pause:
                psprocess.suspend()
            else:
                psprocess.resume()
        return True


engine_classes = (EngineDummy,)
