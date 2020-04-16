from PyQt5.QtCore import QThread, pyqtSignal 

from managers.logfilemanager import LogFileManager
from managers.eventconfigmanager import EventConfigManager

class CleansingThread(QThread): 
    logfileadd_callback = pyqtSignal(object)

    def __init__(self): 
        super(CleansingThread, self).__init__()
        self.logfilemanager = LogFileManager.get_instance()
        self.eventConfig = EventConfigManager.get_instance().getEventConfig()
        

    def run(self): 
        self.remove_empty()
        self.createLogFiles()

    def createLogFiles(self):
        import os
        print("IN GETFIles")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                self.logfilemanager.addLogFile(fname, dirName + "/" + fname, os.path.splitext(fname))
                self.logfilemanager.updateCleanseStatus(fname, True)
                self.logfileadd_callback.emit(self.logfilemanager.getLogFile(fname))

    def remove_empty(self):
        import os
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                if (fname != '.DS_Store'):
                    with open(dirName + "/" + fname) as in_file, open((dirName + "/" + fname), 'r+') as out_file:
                        print(fname)
                        out_file.writelines(line for line in in_file if line.strip())
                        out_file.truncate()