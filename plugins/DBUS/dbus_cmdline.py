##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2010 Fabio Castelli
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
# 
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

import dbus
import sys
from optparse import OptionParser, OptionGroup
import handlepaths

bus = None
actionDone = False
options = {}
interfaces = {
  '/org/gtk/gespeaker': 'org.gtk.gespeaker',
  '/org/gtk/gespeaker/text': 'org.gtk.gespeaker.text',
  '/org/gtk/gespeaker/ui': 'org.gtk.gespeaker.ui',
  '/org/gtk/gespeaker/espeak': 'org.gtk.gespeaker.espeak',
  '/org/gtk/gespeaker/voice': 'org.gtk.gespeaker.voice'
}

def parseArgs():
  "Parse command line arguments"
  parser = OptionParser(usage='usage: %prog [options]')
  parser.add_option('-t', '--tempfilename', action='store_true',
    help='show temporary filename location')
  parser.add_option('-V', '--version', action='store_true',
    help='show version number of the running instance')
  parser.add_option('--ping', action='store_true',
    help='ping if is running')
  parser.add_option('--server', action='store_true',
    help='execute an instance if it not running')
  parser.add_option('--async', action='store_true',
    help='use async methods if possible')

  group = OptionGroup(parser, 'Playing control')
  parser.add_option_group(group)
  group.add_option('-y', '--playing', action='store_true',
    help='check if engine is actually playing')
  group.add_option('-p', '--play', action='store_true',
    help='play the current text')
  group.add_option('-u', '--pause', action='store_true',
    help='pause the current playing')
  group.add_option('-s', '--stop', action='store_true',
    help='stop the current playing')
  group.add_option('--record', action='store', type='string',
    help='record the next play in a wave file')
  group.add_option('--unrecord', action='store_true',
    help='disable the recording for the the next play')

  group = OptionGroup(parser, 'Main window control')
  parser.add_option_group(group)
  group.add_option('-H', '--hide', action='store_true',
    help='hide main window')
  group.add_option('-S', '--show', action='store_true',
    help='show main window')
  group.add_option('-Q', '--quit', action='store_true',
    help='quit running instance')
  group.add_option('-W', '--window', action='store', type='string',
    help='execute window actions')
  group.add_option('--set-opacity', action='store', type='int', dest='opacity',
    help='set window opacity')
  group.add_option('--set-position', action='store', type='string', dest='position',
    help='set window position')
  group.add_option('--set-size', action='store', type='string', dest='size',
    help='set window size')

  group = OptionGroup(parser, 'Text handling')
  parser.add_option_group(group)
  group.add_option('-N', '--new', action='store_true',
    help='clear the whole text')
  group.add_option('-C', '--clear', action='store_true',
    help='clear the whole text')
  group.add_option('-c', '--copy', action='store_true',
    help='copy the selected text')
  group.add_option('-x', '--cut', action='store_true',
    help='cut the selected text')
  group.add_option('-v', '--paste', action='store_true',
    help='paste the text from the clipboard')
  group.add_option('-o', '--open', action='store', type='string',
    help='open a text file')
  group.add_option('-e', '--save', action='store', type='string',
    help='save the current text in a text file')
  group.add_option('--play-text', action='store', type='string',
    help='replace the whole text and play it')
  group.add_option('--append', action='store', type='string',
    help='insert the text at the end')
  group.add_option('--insert', action='store', type='string',
    help='insert the text at the current position')
  group.add_option('--prepend', action='store', type='string',
    help='insert the text at the begin')
  group.add_option('--replace', action='store', type='string',
    help='replace the whole text')

  group = OptionGroup(parser, 'Get voices information')
  parser.add_option_group(group)
  group.add_option('--get-voice', action='store_true',
    help='return the index of the selected voice')
  group.add_option('--get-voices-count', action='store_true', dest='count',
    help='return the list of all available voices')
  group.add_option('--is-mbrola', action='store', type='int',
    help='return True if the voice is a mbrola')
  group.add_option('--get-voice-name', action='store', type='int', dest='name',
    help='return the name of the voice')
  group.add_option('--get-voice-short', action='store', type='int', dest='short',
    help='return the short name of the voice')
  group.add_option('--get-voice-type', action='store_true', dest='type',
    help='return the type of the selected voice')
  group.add_option('--list-all-voices', action='store_true', dest='list_all',
    help='return the list of all available voices')
  group.add_option('--list-mbrola-voices', action='store_true', dest='list_mbrola',
    help='return the list of all available mbrola voices')

  group = OptionGroup(parser, 'Get voices information')
  parser.add_option_group(group)
  group.add_option('--set-voice', action='store', type='int',
    help='set the active voice by its index')
  group.add_option('--set-voice-name', action='store', type='string',
    help='set the active voice by its name')
  group.add_option('--set-voice-type', action='store', type='string',
    help='set the active voice type')

  group = OptionGroup(parser, 'Get voice settings')
  parser.add_option_group(group)
  group.add_option('--get-delay', action='store_true',
    help='get voice delay')
  group.add_option('--get-pitch', action='store_true',
    help='get voice pitch')
  group.add_option('--get-speed', action='store_true',
    help='get voice speed')
  group.add_option('--get-volume', action='store_true',
    help='get voice volume')

  group = OptionGroup(parser, 'Set voice settings')
  parser.add_option_group(group)
  group.add_option('-R', '--reset', action='store_true',
    help='reset the default settings')
  group.add_option('--set-delay', action='store', type='int', dest='delay',
    help='set voice delay')
  group.add_option('--set-pitch', action='store', type='int', dest='pitch',
    help='set voice pitch')
  group.add_option('--set-speed', action='store', type='int', dest='speed',
    help='set voice speed')
  group.add_option('--set-volume', action='store', type='int', dest='volume',
    help='set voice volume')

  global options
  (options, args) = parser.parse_args()
  # Check for mutual exclusive options
  mutex = lambda option1, option2: parser.error(
    'options --%s and --%s are mutually exclusive' % (option1, option2))
  if options.hide and options.show:
    mutex('hide', 'show')
  if options.play and options.pause:
    mutex('play', 'pause')
  if options.play and options.stop:
    mutex('play', 'stop')
  if options.pause and options.stop:
    mutex('pause', 'stop')

  if options.position is not None and 'x' not in options.position:
    parser.error('option --set_position needs position like LEFTxTOP')
  if options.size is not None and 'x' not in options.size:
    parser.error('option --set_size needs size like WIDTHxHEIGHT')

  # Create connection to DBUS
  global bus
  bus = dbus.SessionBus()
  
  # Check for single instance
  if options.server:
    try:
      if callMethod('', 'ping', str)==1:
        # Already running, exit
        sys.exit(0)
    except dbus.exceptions.DBusException:
      options.async = True
      global actionDone
      actionDone = False
  
  # Interface /org/freedesktop/gespeaker
  if options.ping is not None:
    callMethod('', 'ping', str)
  if options.tempfilename is not None:
    callMethod('', 'get_tempfilename', str)
  if options.version is not None:
    callMethod('', 'get_version', str)
  # Interface /org/freedesktop/gespeaker/text
  if options.append is not None:
    callMethod('/text', 'append', None, options.append)
  if options.clear is not None:
    callMethod('/text', 'clear')
  if options.copy is not None:
    callMethod('/text', 'copy')
  if options.cut is not None:
    callMethod('/text', 'cut')
  if options.insert is not None:
    callMethod('/text', 'insert', None, options.insert)
  if options.paste is not None:
    callMethod('/text', 'paste')
  if options.prepend is not None:
    callMethod('/text', 'prepend', None, options.prepend)
  if options.replace is not None:
    callMethod('/text', 'replace', None, options.replace)
  # Interface /org/freedesktop/gespeaker/ui
  if options.hide is not None:
    callMethod('/ui', 'hide')
  if options.position is not None:
    callMethod('/ui', 'set_position', str, options.position)
  if options.size is not None:
    callMethod('/ui', 'set_size', str, options.size)
  if options.new is not None:
    callMethod('/ui', 'new', None, False)
  if options.open is not None:
    callMethod('/ui', 'open', None, options.open)
  if options.play_text is not None:
    callMethod('/ui', 'play_text', None, options.play_text)
  if options.quit is not None:
    callMethod('/ui', 'quit')
  if options.record is not None:
    callMethod('/ui', 'record', None, options.record)
  if options.reset is not None:
    callMethod('/ui', 'reset', None, False)
  if options.save is not None:
    callMethod('/ui', 'save', None, options.save)
  if options.opacity is not None:
    callMethod('/ui', 'set_opacity', str, options.opacity)
  if options.show is not None:
    callMethod('/ui', 'show')
  if options.unrecord is not None:
    callMethod('/ui', 'unrecord')
  if options.window is not None:
    callMethod('/ui', 'set_window', str, options.window)
  # Interface /org/freedesktop/gespeaker/espeak
  if options.playing is not None:
    callMethod('/espeak', 'is_playing', str)
  if options.play is not None:
    callMethod('/espeak', 'play')
  if options.pause is not None:
    callMethod('/espeak', 'pause')
  if options.stop is not None:
    callMethod('/espeak', 'stop')
  # Interface /org/freedesktop/gespeaker/voice
  if options.get_delay is not None:
    callMethod('/voice', 'get_delay', str)
  if options.get_pitch is not None:
    callMethod('/voice', 'get_pitch', str)
  if options.get_speed is not None:
    callMethod('/voice', 'get_speed', str)
  if options.get_voice is not None:
    callMethod('/voice', 'get_voice', str)
  if options.is_mbrola is not None:
    callMethod('/voice', 'get_voice_is_mbrola', str, options.is_mbrola)
  if options.name is not None:
    callMethod('/voice', 'get_voice_name', str, options.name)
  if options.short is not None:
    callMethod('/voice', 'get_voice_short', str, options.short)
  if options.type is not None:
    callMethod('/voice', 'get_voice_type', str)
  if options.count is not None:
    callMethod('/voice', 'get_voices_count', str)
  if options.get_volume is not None:
    callMethod('/voice', 'get_volume', str)
  if options.list_all is not None:
    callMethod('/voice', 'list_all_voices', voices_list)
  if options.list_mbrola is not None:
    callMethod('/voice', 'list_mbrola_voices', voices_list)
  if options.delay is not None:
    callMethod('/voice', 'set_delay', str, options.delay)
  if options.pitch is not None:
    callMethod('/voice', 'set_pitch', str, options.pitch)
  if options.speed is not None:
    callMethod('/voice', 'set_speed', str, options.speed)
  if options.set_voice is not None:
    callMethod('/voice', 'set_voice', str, options.set_voice)
  if options.set_voice_name is not None:
    callMethod('/voice', 'set_voice_by_name', str, options.set_voice_name)
  if options.set_voice_type is not None:
    callMethod('/voice', 'set_voice_type', str, options.set_voice_type)
  if options.volume is not None:
    callMethod('/voice', 'set_volume', str, options.volume)

  # Quit application if a command line action was done
  if actionDone and not options.server:
    sys.exit(0)
    
def voices_list(voices):
  "Format the voices list"
  return [str(voice) for voice in voices]

def callMethod(interface, methodName, result=None, *args):
  "Call a DBUS method and optionally print the result"
  global actionDone
  interface = '/org/gtk/gespeaker%s' % interface
  gespeakerService = bus.get_object('org.gtk.gespeaker', interface)
  method = gespeakerService.get_dbus_method(methodName, interfaces[interface])
   
  if len(args) == 0:
    if options.async:
      return_value = method(reply_handler=async_call, error_handler=async_error)
    else:
      return_value = method()
  elif len(args) == 1:
    if options.async:
      return_value = method(args[0], reply_handler=async_call, error_handler=async_error)
    else:
      return_value = method(args[0])

  # Print result
  if result:
    print '[dbus_cmdline] %s: %s' % (methodName, result(return_value))
  # Don't close if it's running in async mode
  if not options.async:
    actionDone = True
  
  return return_value

def async_call(r=None):
  print 'reply: ', r
  
def async_error(e=None):
  print 'error: ', e
