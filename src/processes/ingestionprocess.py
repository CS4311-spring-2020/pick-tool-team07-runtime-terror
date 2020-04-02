import os, sys
sys.path.append("..")

from splunk.splunkinterface import SplunkClient

from managers.logentrymanager import LogEntryManager
from managers.logfilemanager import LogFileManager

class IngestionProcess(object): 
    def __init__(self): 
        self.splunk = SplunkClient()
        self.entryManager = LogEntryManager.get_instance()
        self.fileManager = LogFileManager.get_instance()

    def start(self):
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
        
            # We need some form to verify if we actually got results from splunk
            logFile.setIngestionStatus(True)
        
        return True


# if __name__ == '__main__': 
#     ingestion()
#     # t1 = Thread(target=cleansing, args=(ingestion_queue,))
#     # t2 = Thread(target=ingestion, args=(ingestion_queue,))
#     # t1.start()
#     # t2.start()

#     # ingestion_queue.join()