import os

from PIL import Image
import pytesseract
import filetype

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
                    output = pytesseract.image_to_string(Image.open(dirName+'/'+fname))
                    with open(dirName+'/'+fname+'.txt', 'w') as newF: 
                        newF.write(output)
                    f = fname+'.txt'
                #TODO handle audio files
                self.createLogFile(dirName, f)
                
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
                if (fname != '.DS_Store'):
                    with open(dirName + "/" + fname) as in_file, open((dirName + "/" + fname), 'r+') as out_file:
                        out_file.writelines(line for line in in_file if line.strip())
                        out_file.truncate()