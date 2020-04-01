#import logfilemanager
from .eventconfigmanager import EventConfig
from .logfilemanager import LogFileManager
import threading
import os

class CleansingProcess:
    def __init__(self):
        #directory where cleansing will be needed 
        #self.directory
        pass

    #Checks to see if file needs cleansing
    def check_file(self):
        pass

    #Removes empty lines from a file
    #Files coming from event config
    def remove_empty(self):
        with open(filePath) as in_file, open(filePath, 'r+') as out_file:
            out_file.writelines(line for line in in_file if line.strip())
            out_file.truncate()

    #removes unwanted characters from a file
    def remove_characters(self):
        pass

