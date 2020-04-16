from PyQt5.QtCore import QThread, pyqtSignal 

from splunk.splunkinterface import SplunkClient

from managers.logentrymanager import LogEntryManager
from managers.logfilemanager import LogFileManager

class IngestionThread(QThread): 
    logfile_callback = pyqtSignal(object)
    logentry_callback = pyqtSignal(object)

    def __init__(self):
        super(IngestionThread, self).__init__()
        self.splunk = SplunkClient()
        self.fileManager = LogFileManager.get_instance()
        self.entryManager = LogEntryManager.get_instance()

    def run(self): 
        logFiles = self.fileManager.getLogFiles()

        for logFile in logFiles: 
            if logFile.getIngestionStatus(): 
                continue

            logFilePath = logFile.getPathToFile()
            print(logFilePath)
            self.splunk.upload(logFilePath)

            results = self.splunk.results(logFilePath)

            for result in results: 
                self.entryManager.addEntry(
                    result["host"], 
                    result["timestamp"], 
                    result["content"], 
                    result["source"], 
                    result["sourcetype"] 
                )
                self.logentry_callback.emit(
                    self.entryManager.getEntryByContent(result["content"]))

            # We need some form to verify if we actually got results from splunk
            logFile.setIngestionStatus(True)