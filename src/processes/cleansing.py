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
        self.createLogFiles()
        ingestion_queue.put(cleansing_done)

    def createLogFiles(self):
        import os
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                self.logfilemanager.addLogFile(fname, dirName + "/" + fname, os.path.splitext(fname))
                logfile = self.logfilemanager.getLogFile(fname)
                ingestion_queue.put(logfile)

                self.logfilemanager.updateCleanseStatus(fname, True)
                self.logfileadd_callback.emit(self.logfilemanager.getLogFile(fname))

    def remove_empty(self):
        import os
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                if (fname != '.DS_Store'):
                    with open(dirName + "/" + fname) as in_file, open((dirName + "/" + fname), 'r+') as out_file:
                        out_file.writelines(line for line in in_file if line.strip())
                        out_file.truncate()