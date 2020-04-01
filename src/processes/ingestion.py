import os, sys
sys.path.append("..")

from splunk.splunkinterface import SplunkClient

from managers.logentrymanager import LogEntryManager
from managers.logfilemanager import LogFileManager
 
def ingestion(): 
    splunk = SplunkClient()

    entryManager = LogEntryManager.get_instance()
    fileManager = LogFileManager.get_instance()

    for logFile in fileManager.getLogFiles(): 
        if logFile.getIngestionStatus(): 
            continue

        logFilePath = logFile.getPathToFile() + "/" + logFile.getLogName()

        splunk.upload(logFilePath)

        results = splunk.results(logFilePath)

        for result in results: 
            entryManager.addEntry(
                result["host"], 
                result["timestamp"], 
                result["content"], 
                result["source"], 
                result["sourcetype"] 
            )
        
        # We need some form to verify if we actually got results from splunk
        logFile.setIngestionStatus(True)

if __name__ == '__main__': 
    ingestion()
    # t1 = Thread(target=cleansing, args=(ingestion_queue,))
    # t2 = Thread(target=ingestion, args=(ingestion_queue,))
    # t1.start()
    # t2.start()

    # ingestion_queue.join()