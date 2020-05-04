import os


import filetype
# Imports for image to text conversion 
import pytesseract
from PIL import Image

# Imports for audio to text
import speech_recognition as sr

from PyQt5.QtCore import QThread, pyqtSignal 

from managers.logfilemanager import LogFileManager
from managers.eventconfigmanager import EventConfigManager


from .ingestion import ingestion_queue, cleansing_done

class CleansingThread(QThread): 
    logfileadd_callback = pyqtSignal(object)
    # TODO add error callback, so that we could add it to action report
    

    def __init__(self): 
        super(CleansingThread, self).__init__()
        self.logfilemanager = LogFileManager()
        self.eventConfig = EventConfigManager.get_instance().getEventConfig()

    def run(self):
        self.remove_empty()
        self.processFiles()
        ingestion_queue.put(cleansing_done)
    

    def processFiles(self): 
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                f = fname
                if filetype.image_match(dirName+'/'+fname): 
                    f = self.imgHandel(dirName, f)
                #TODO handle audio files
                # if filetype.video_match(dirName+'/'+fname):
                #     f = self.audioHandel(dirName, fname, isVideo=True) 

                # if filetype.audio_match(dirName+'/'+fname): 
                #     f = self.audioHandel(dirName, fname)
                self.createLogFile(dirName, f)

    def imgHandel(self, dirName, fname): 
        output = pytesseract.image_to_string(Image.open(dirName+'/'+fname))
        with open(dirName+'/'+fname+'.txt', 'w') as newF: 
            newF.write(output)
        return fname+'.txt'

    def audioHandel(self, dirName, fname, isVideo=False): 
        pathfile = dirName+'/'+fname
        inputf = pathfile
        if isVideo == True: 
            inputf = output = pathfile + '.mp3'
            os.system("ffmpeg -i" + pathfile + " " + output)
        
        output = pathfile+'.wav'
        os.system("ffmpeg -i" + inputf + " " + output)

        recog = sr.Recognizer()
        audio = sr.AudioFile(output)

        import subprocess
        import re

        process = subprocess.Popen(['ffmpeg',  '-i', output], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        matches = re.search(
            r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),",
            stdout.decode(), 
            re.DOTALL).groupdict()

        totalsec = int(matches['hours']) * 3600
        totalsec += int(matches['minutes']) * 60
        totalsec += float(matches['seconds'])

    def createLogFile(self, dirName, fname):
        self.logfilemanager.addLogFile(fname, dirName + "/" + fname, os.path.splitext(fname))
        logfile = self.logfilemanager.getLogFile(fname)
        ingestion_queue.put(logfile)

        self.logfilemanager.updateCleanseStatus(fname, True)
        self.logfileadd_callback.emit(self.logfilemanager.getLogFile(fname))

    def remove_empty(self):
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                if filetype.image_match(dirName+'/'+fname): 
                    continue
                if filetype.video_match(dirName+'/'+fname): 
                    continue
                if filetype.audio_match(dirName+'/'+fname): 
                    continue
                if (fname != '.DS_Store'):
                    with open(dirName + "/" + fname) as in_file, open((dirName + "/" + fname), 'r+') as out_file:
                        out_file.writelines(line for line in in_file if line.strip())
                        out_file.truncate()