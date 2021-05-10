Gespeaker
=========
**Description:** A GTK frontend for espeak

**Copyright:** 2009-2021 Fabio Castelli

**License:** GPL-3+

**Source code:** https://github.com/muflone/gespeaker

**Documentation:** https://www.muflone.com/gespeaker

**Translations:** https://www.transifex.com/projects/p/gespeaker/

Description
-----------

Gespeaker allows you to play a text in many languages with settings for voice,
pitch, volume and speed.

The text that has been read can also be recorded to WAV file for future
listening.

Since version 0.6 it supports the speech synthesizer MBROLA for a better speech
experience.

System Requirements
-------------------

* Python 3.x (developed and tested for Python 3.9.4)
* XDG library for Python 3 ( https://pypi.org/project/pyxdg/ )
* GTK+ 3.0 libraries for Python 3
* GObject libraries for Python 3 ( https://pypi.org/project/PyGObject/ )
* PSUtil library for Python 3 ( https://pypi.org/project/psutil/ )
* Google Text-to-Speech library for Python 3 ( https://pypi.org/project/gTTS/ )
* Distutils library for Python 3 (usually shipped with Python distribution)
* espeak for basic eSpeak voices
* MBROLA for enhanced MBROLA voices and at least one of the MBROLA voices
* Pulseaudio player (technically `paplay` command line)

Installation
------------

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python3 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python3 setup.py install --root NEW_PATH

Usage
-----

If the application is not installed please use:

    cd /path/to/folder
    python3 gespeaker.py

If the application was installed simply use the gespeaker command.
