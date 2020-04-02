#import logfilemanager
print("NICE")
from managers.eventconfigmanager import EventConfigManager
from managers.logfilemanager import LogFileManager
import threading
import os

class CleansingProcess(object):
    def __init__(self):
        #directory where cleansing will be needed 
        #self.directory
        self.eventConfig = EventConfigManager.get_instance().getEventConfig()
        self.logfilemanager = LogFileManager.get_instance()
        #self.fileList = []

    # Hmm start function also in Ingestionprocess...
    # Maybe base class needed?
    def start(self): 
        self.remove_empty()
        self.createLogFiles()

        return True
    
    #Checks to see if file needs cleansing
    def createLogFiles(self):
        print("IN GETFIles")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                self.logfilemanager.addLogFile(fname, dirName + "/" + fname, os.path.splitext(fname))
        

    #Removes empty lines from a file
    #Files coming from event config
    def remove_empty(self):
        print("IN REMOVE EMPTY")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                if (fname != '.DS_Store'):
                    with open(dirName + "/" + fname) as in_file, open((dirName + "/" + fname), 'r+') as out_file:
                        print(fname)
                        out_file.writelines(line for line in in_file if line.strip())
                        out_file.truncate()
                

    #TODO
    #removes unwanted characters from a file
    def remove_characters(self):
        pass
