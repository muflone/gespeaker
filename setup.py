#!/usr/bin/env python
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

import glob
import itertools
import os
import shutil
import subprocess

from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data
from distutils.core import setup, Command
from distutils.log import info

from gespeaker.constants import (APP_NAME,
                                 APP_VERSION,
                                 APP_AUTHOR,
                                 APP_AUTHOR_EMAIL,
                                 APP_URL,
                                 APP_DESCRIPTION,
                                 DOMAIN_NAME)


class InstallScripts(install_scripts):
    def run(self):
        install_scripts.run(self)
        self.rename_python_scripts()

    def rename_python_scripts(self):
        """
        Rename main executable python script without .py extension
        """
        for script in self.get_outputs():
            if script.endswith(".py"):
                info('renaming the python script %s -> %s' % (script,
                                                              script[:-3]))
                shutil.move(script, script[:-3])


class InstallData(install_data):
    def run(self):
        self.install_icons()
        cmd_translations = CommandTranslations(self.distribution)
        cmd_translations.initialize_options()
        cmd_translations.finalize_options()
        cmd_translations.data_files = self.data_files
        cmd_translations.run()
        install_data.run(self)

    def install_icons(self):
        info('Installing icons...')
        dir_icons = 'icons'
        for icon_format in os.listdir(dir_icons):
            icon_dir = os.path.join(dir_icons, icon_format)
            self.data_files.append((
                os.path.join('share', 'icons', 'hicolor', icon_format, 'apps'),
                glob.glob(os.path.join(icon_dir, '*'))))


class CommandTranslation(Command):
    description = "compile a translation"
    user_options = [
        ('input=', None, 'Define input file'),
        ('output=', None, 'Define output file'),
    ]

    def initialize_options(self):
        self.input = None
        self.output = None
        self.data_files = []

    def finalize_options(self):
        assert self.input, 'Missing input file'
        assert self.output, 'Missing output file'

    def run(self):
        """Compile a single translation using self.input and self.output"""
        lang = os.path.basename(self.input[:-3])
        dir_lang = os.path.dirname(self.output)
        if not os.path.exists(dir_lang):
            os.makedirs(dir_lang)
        subprocess.call(('msgfmt', '--output-file', self.output, self.input))
        self.data_files.append((os.path.join('share',
                                             'locale',
                                             lang,
                                             'LC_MESSAGES'),
                                [self.output]))


class CommandTranslations(Command):
    description = "build translations"
    user_options = []

    def initialize_options(self):
        self.data_files = []

    def finalize_options(self):
        self.dir_base = os.path.dirname(os.path.abspath(__file__))
        self.dir_po = os.path.join(self.dir_base, 'po')
        self.dir_mo = os.path.join(self.dir_base, 'locale')

    def run(self):
        """Compile every translation and add it to the data files"""
        for file_po in glob.glob(os.path.join(self.dir_po, '*.po')):
            file_mo = os.path.join(self.dir_mo,
                                   os.path.basename(file_po[:-3]),
                                   'LC_MESSAGES',
                                   '%s.mo' % DOMAIN_NAME)
            cmd_translation = CommandTranslation(self.distribution)
            cmd_translation.initialize_options()
            cmd_translation.input = file_po
            cmd_translation.output = file_mo
            cmd_translation.finalize_options()
            # Add the translation files to the data files
            cmd_translation.data_files = self.data_files
            cmd_translation.run()


setup(
    name=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    author=APP_AUTHOR,
    author_email=APP_AUTHOR_EMAIL,
    maintainer=APP_AUTHOR,
    maintainer_email=APP_AUTHOR_EMAIL,
    url=APP_URL,
    license='GPL v3',
    scripts=['gespeaker.py'],
    packages=['gespeaker',
              'gespeaker.engines',
              'gespeaker.ui',
              'gespeaker.ui.models'],
    data_files=[
        ('share/applications', ['data/gespeaker.desktop']),
        ('share/gespeaker/data', ['data/testing.wav',
                                  'data/gespeaker.png']),
        ('share/gespeaker/data/icons', glob.glob('data/icons/*')),
        ('share/gespeaker/ui', list(itertools.chain(
            glob.glob('ui/*.glade'),
            glob.glob('ui/*.ui')))),
        ('share/doc/gespeaker', list(itertools.chain(glob.glob('doc/*'),
                                                     glob.glob('*.md')))),
        ('share/man/man1', ['man/gespeaker.1']),
    ],
    cmdclass={
        'install_scripts': InstallScripts,
        'install_data': InstallData,
        'translation': CommandTranslation,
        'translations': CommandTranslations
    }
)
