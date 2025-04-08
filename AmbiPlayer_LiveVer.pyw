
import time
from pycaw.pycaw import AudioUtilities
import soundfile as sf
import sounddevice as sd
import os
import keyboard
import random as rd
import re
import multiprocessing as  mp
from pygame import mixer
import logging
logging.basicConfig(filename=os.getcwd()+'\\AmbiCrash.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
PlaylistFileDirectory = "Ambience Playlists" # Directory to grab the music from 
playing =False # variable to track if ambient sound is playing to stop sd.stop() from triggering constantly 
playList=[] #list of lists that will contain all the absolute paths of music to be played
Sessions =[]

mixer.init()
## Helper functions
def is_audio_playing():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.State == 1 and "python" not in str(session.Process):  # State == 1 means the audio session is active
            return True
    return False
def SetSong():
    Song = rd.choice(playList[foldval])
    SongLength = mixer.Sound(Song).get_length()
    mixer.music.unload()
    mixer.music.load(Song)
    mixer.music.play(fade_ms=9000)
    return [Song,SongLength]

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def fadeoutCurrenSong(SongData,stoppedAt):
    if (mixer.music.get_pos()+stoppedAt)/1000>= SongData[1]-3:
        mixer.music.fadeout(3000)

def SetPlayListPaths():
    for root, dirs, files in os.walk(os.path.abspath("Ambience Playlists")):
        folder =[]
        for file in sorted_alphanumeric(files):
            folder.append(os.path.join(root, file))
        if files != []:
            playList.append(folder)

SetPlayListPaths()
foldval = rd.randint(1,len(playList)-1) # Sets the default folder to a random one in the directory 
SongData = SetSong()
playing=True
stoppedAt =0

while not keyboard.is_pressed('=+k+o'):
    try:
        if keyboard.is_pressed('=+-'):
            for i in range(len(playList)):
                if keyboard.is_pressed(str(i+1)):
                    foldval=i
                    SongData = SetSong()
                    stoppedAt=0
                    if not playing: 
                        mixer.music.pause()
                    time.sleep(2)
        

        time.sleep(0.5) #check twice per second 
        if is_audio_playing():
            if playing:
                stoppedAt += (1000+mixer.music.get_pos())/1000
                mixer.music.fadeout(1000)
                playing=False
        

        else:
            if (mixer.music.get_pos()+(stoppedAt*1000))>= (SongData[1]-4)*1000:
                mixer.music.fadeout(3800)
                playing=False
                stoppedAt=0
            if not mixer.music.get_busy():
                time.sleep(2)
                if not is_audio_playing():
                    if stoppedAt >0 and playing == False: 
                        mixer.music.play(start=stoppedAt,fade_ms=9000)
                
                    else:
                        SongData=SetSong()
                        stoppedAt=0
                    playing=True
    except Exception as err:
        logger.error(err)
        logger.error(SongData[0])