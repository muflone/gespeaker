##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
##

import SubprocessWrapper
import os

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
    procPlay = SubprocessWrapper.Popen(cmdPlayer.split(), 
      stdin=procEspeak.stdout,
      stdout=SubprocessWrapper.PIPE,
      stderr=SubprocessWrapper.PIPE)
    # Save both processes espeak and player
    self.procTalk = (procEspeak, procPlay)

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
