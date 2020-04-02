#import logfilemanager
print("NICE")
from eventconfig import EventConfig
from logfilemanager import LogFileManager
import threading
import os

class CleansingProcess:
    def __init__(self):
        #directory where cleansing will be needed 
        #self.directory
        self.eventConfig = EventConfig()
        self.logfilemanager = LogFileManager()
        self.remove_empty()
        self.createLogFiles()
        #self.fileList = []

    #Checks to see if file needs cleansing
    def createLogFiles(self):
        print("IN GETFIles")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir, topdown=False):
            #print(dirName)
            for fname in filelist:
                #print("TESTING CREATION OF FILES")
                #print(fname)
                #print( dirName + "/" + fname)
                #print(os.path.splitext(fname)[1])
                self.logfilemanager.addLogFile(fname, dirName + "/" + fname, os.path.splitext(fname))
        

    #Removes empty lines from a file
    #Files coming from event config
    def remove_empty(self):
        print("IN REMOVE EMPTY")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir, topdown=False):
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
