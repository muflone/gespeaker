#!/usr/bin/env python

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

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.log import info
from glob import glob
import os
import sys


class InstallData(install_data):
    def run(self):
        self.data_files.extend(self._compile_po_files())
        install_data.run(self)

    def _compile_po_files(self):
        data_files = []

        # Don't install language files on win32
        if sys.platform == 'win32':
            return data_files

        PO_DIR = 'po'
        for lang in open(os.path.join(PO_DIR, 'availables'), 'r').readlines():
            lang = lang.strip()
            if lang:
                po = os.path.join(PO_DIR, '%s.po' % lang)
                mo = os.path.join('build', 'mo', lang, 'gespeaker.mo')

                directory = os.path.dirname(mo)
                if not os.path.exists(directory):
                    info('creating %s' % directory)
                    os.makedirs(directory)

                if newer(po, mo):
                    # True if mo doesn't exist
                    cmd = 'msgfmt -o %s %s' % (mo, po)
                    info('compiling %s -> %s' % (po, mo))
                    if os.system(cmd) != 0:
                        raise SystemExit('Error while running msgfmt')

                dest = os.path.dirname(
                    os.path.join('share', 'locale', lang, 'LC_MESSAGES',
                                 'gespeaker.mo'))
                data_files.append((dest, [mo]))

        return data_files


setup(
    name='Gespeaker',
    version='0.8.5',
    description='A GTK+ frontend for eSpeak and mbrola',
    author='Fabio Castelli',
    author_email='muflone@vbsimple.net',
    url='http://www.muflone.com/gespeaker/',
    license='GPL v2',
    scripts=['gespeaker'],
    data_files=[
        ('share/applications', ['data/gespeaker.desktop']),
        ('share/gespeaker/data', ['data/testing.wav']),
        ('share/gespeaker/data/icons', glob('data/icons/*')),
        ('share/gespeaker/data/ui', glob('data/ui/*.glade')),
        ('share/doc/gespeaker',
         ['doc/README', 'doc/changelog', 'doc/translators']),
        ('share/man/man1', ['man/gespeaker.1']),
        ('share/gespeaker/src', glob('src/*.py'))
    ],
    cmdclass={'install_data': InstallData}
)
