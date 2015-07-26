##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
# Copyright: 2009-2015 Fabio Castelli
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
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import SubprocessWrapper
import os
import handlepaths
from gettext import gettext as _
from DialogSimpleMessages import ShowDialogError

class EspeakFrontend(object):
  def __init__(self):
    self.procTalk = None
    print 'python version detected: %d.%d' % (
      SubprocessWrapper.PYTHON_VERSION[0], SubprocessWrapper.PYTHON_VERSION[1])

  def isPlaying(self):
    "Check if a process is still running"
    return self.procTalk and (
      self.procTalk[0].poll() == None or self.procTalk[1].poll() == None)

  def pauseOrResume(self, status):
    "Pause or Resume the playing, based on status"
    if self.procTalk:
      # Check if espeak is still runnning
      if self.procTalk[0].poll() == None:
        if status:
          self.procTalk[0].stop()
        else:
          self.procTalk[0].resume()
      # Check if player is still runnning
      if self.procTalk[1].poll() == None:
        if status:
          self.procTalk[1].stop()
        else:
          self.procTalk[1].resume()

  def play(self, cmdEspeak, cmdPlayer, fileToRecord=None):
    "Play the command provided"
    # If save to file has been requested add -w else --stdout
    cmdEspeak += fileToRecord and ['-w', fileToRecord] or ['--stdout']

    # Execute espeak and pipe it with player
    print cmdEspeak, cmdPlayer.split()
    procEspeak = SubprocessWrapper.Popen(cmdEspeak, 
      stdout=SubprocessWrapper.PIPE)
    # Save to file has been requested so we have to wait for espeak end
    # and to pipe filename content to the player
    if fileToRecord:
      procEspeak.wait()
      procEspeak = SubprocessWrapper.Popen(['cat', fileToRecord],
        stdout=SubprocessWrapper.PIPE)
    self.__playAudio(procEspeak, cmdPlayer)

  def playMbrola(self, cmdEspeak, cmdPlayer, cmdMbrola, fileToRecord=None):
    "Play the command provided"
    # If save to file has been requested add filename else -
    if not fileToRecord:
      fileToRecord = '/tmp/gespeaker.wav'
    cmdMbrola += [fileToRecord]

    # Execute espeak and pipe it with mbrola and then the player)
    print cmdEspeak, cmdMbrola, cmdPlayer.split()
    procEspeak = SubprocessWrapper.Popen(cmdEspeak, 
      stdout=SubprocessWrapper.PIPE)

    try:
      procMbrola = SubprocessWrapper.Popen(cmdMbrola,
        stdin=procEspeak.stdout, stdout=SubprocessWrapper.PIPE)
    except OSError, (errno, strerror):
      # Error during communicate"
      ShowDialogError(
        title=_('Audio testing'),
        showOk=True,
        text=_('There was an error during the test for the audio player.\n\n'
          'Error %s: %s') % (errno, strerror),
        icon=handlepaths.get_app_logo()
      )
      procMbrola = None

    # Save to file has been requested so we have to wait for espeak end
    # and to pipe filename content to the player
    if procMbrola:
      procMbrola.wait()
      procMbrola = SubprocessWrapper.Popen(['cat', fileToRecord],
        stdout=SubprocessWrapper.PIPE)
      self.__playAudio(procMbrola, cmdPlayer)

  def __playAudio(self, procFrom, cmdPlayer):
    "Play audio with the player piping from a process"
    try:
      procPlay = SubprocessWrapper.Popen(cmdPlayer.split(), 
        stdin=procFrom.stdout,
        stdout=SubprocessWrapper.PIPE,
        stderr=SubprocessWrapper.PIPE)
    except OSError, (errno, strerror):
      # Error during communicate"
      ShowDialogError(
        title=_('Audio testing'),
        showOk=True,
        text=_('There was an error during the test for the audio player.\n\n'
          'Error %s: %s') % (errno, strerror),
        icon=handlepaths.get_app_logo()
      )
      procPlay = None
    # Save both processes espeak and player
    if procPlay:
      self.procTalk = (procFrom, procPlay)

  def stop(self):
    "Stop audio killing espeak and player"
    # If played at least once then we have procTalk
    if self.procTalk:
      # Check if espeak is still running
      if self.procTalk[0].poll() == None:
        print 'killing espeak with pid %d' % self.procTalk[0].pid
        self.procTalk[0].terminate()
      # Check if player is still runnning
      if self.procTalk[1].poll() == None:
        print 'killing player with pid %d' % self.procTalk[1].pid
        self.procTalk[1].terminate()
      # We don't need processes anymore
      self.procTalk = None
      return True
    else:
      return False

  def loadLanguages(self, cmdEspeak):
    "Load languages list from espeak"
    print 'loading languages from %s --voices' % cmdEspeak
    proc = SubprocessWrapper.Popen((cmdEspeak, '--voices'), 
      stdout=SubprocessWrapper.PIPE)
    return proc.communicate()[0].split('\n')[1:-1]

  def loadVariants(self, cmdEspeak):
    "Load variants list from espeak"
    vardir = '/usr/share/espeak-data/voices/!v'
    print 'loading variants from %s' % vardir
    variantsM = []
    variantsF = []
    # Check if voice variants dir exists
    if os.path.exists(vardir) and os.path.isdir(vardir):
      # Load files from vardir
      for f in os.listdir(vardir):
        # Only files
        if os.path.isfile(os.path.join(vardir, f)):
          varfile = open(os.path.join(vardir, f), mode='r')
          varcontent = varfile.read().split('\n')
          varfile.close()
          # Check if it's a valid variant
          if varcontent[0] == 'language variant' and \
            varcontent[1][:5] == 'name ' and \
            varcontent[2][:7] == 'gender ':
            # Check gender
            if varcontent[2][7:] == 'female':
              variantsF.append((f, varcontent[1][5:]))
            else:
              variantsM.append((f, varcontent[1][5:]))
    return (variantsM, variantsF)

  def loadMbrolaVoices(self, pathVoicesmb):
    "Load mbrola languages list"
    voicesmb = []
    espeak_data_paths = (
      '/usr/share/espeak-data/voices/mb/',
      '/usr/lib/x86_64-linux-gnu/espeak-data/voices/mb/',
      '/usr/lib/i386-linux-gnu/espeak-data/voices/mb/',
    )
    for pathVoices in espeak_data_paths:
      if os.path.isdir(pathVoices):
        break
    else:
      print 'Cannot find any espeak-data voices folder, unable to detect MBROLA voices'
      pathVoices = ''
    if not pathVoicesmb or not os.path.isdir(pathVoicesmb):
      pathVoicesmb = '/usr/share/mbrola'
    if os.path.isdir(pathVoices) and os.path.isdir(pathVoicesmb):
      for voice in os.listdir(pathVoices):
        # Only files
        if os.path.isfile(os.path.join(pathVoices, voice)):
          voicefile = open(os.path.join(pathVoices, voice), mode='r')
          voicecontent = voicefile.read().split('\n')
          voicefile.close()
          # Check if it's a valid voice
          for line in voicecontent:
            if line[:5] == 'name ':
              voicesmb.append((line[5:], voice, os.path.isfile(os.path.join(pathVoicesmb, voice[3:], voice[3:]))))
              break
    return voicesmb

  def mbrolaExists(self, cmdMbrola):
    "Return mbrola existance"
    try:
      # Try to call mbrola executable
      mbrola = SubprocessWrapper.Popen(cmdMbrola, 
        stdout=SubprocessWrapper.PIPE, stderr=SubprocessWrapper.PIPE)
      mbrola.communicate()
      status = True
    except:
      # Error during communicate"
      status = False
    return status
