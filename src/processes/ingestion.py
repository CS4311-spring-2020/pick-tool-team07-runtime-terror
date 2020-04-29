from PyQt5.QtCore import QThread, pyqtSignal 

from splunk.splunkinterface import SplunkClient

from managers.logentrymanager import LogEntryManager
from managers.logfilemanager import LogFileManager
from managers.eventconfigmanager import EventConfigManager

from queue import Queue
from dateutil.parser import parse

ingestion_queue = Queue()
cleansing_done = object()

class IngestionThread(QThread): 
    logfile_callback = pyqtSignal(object, object)
    logentry_callback = pyqtSignal(object)

    def __init__(self):
        super(IngestionThread, self).__init__()
        self.splunk = SplunkClient()
        self.fileManager = LogFileManager()
        self.eventConfig = EventConfigManager.get_instance()
        self.entryManager = LogEntryManager.get_instance()

    def run(self): 
        while True: 
            if ingestion_queue.empty(): 
                continue
            
            logFile = ingestion_queue.get()

            # If the item that we got form the queue is the cleansing done 
            # object then end the thread
            if logFile is cleansing_done: 
                break

            print("Ingestion: Processing")
            print(logFile.getIngestionStatus())
            if logFile.getIngestionStatus() == "True": 
                continue
            
            logpath = logFile.getPathToFile()

            self.splunk.upload(logpath)

            results = self.splunk.results(logpath)

            for result in results: 
                # time = self.eventConfig.getEventTime()
                # logentryTime = parse(result["timestamp"])
                
                # If the log entry time stamp is less than of the start time in the event configuration, 
                # or if it is greater than of the end time in the event configuration, do not ingest this
                # log entry
                # TODO check if a log entry doesnt pass this check, should we notify the user? 
                # if logentryTime < time[0] or logentryTime > time[1]:
                #     continue

                # TODO Need to convert the time into zulu time

                # TODO Need to add to which team this log entry belongs to
                self.entryManager.addEntry(
                    result["host"], 
                    result["timestamp"], 
                    result["content"], 
                    result["source"], 
                    result["sourcetype"] 
                )
                self.logentry_callback.emit(
                    self.entryManager.getEntryByContent(result["content"])
                )

            self.fileManager.updateIngestionStatus(logFile.getLogName(), True)
            self.logfile_callback.emit(
                self.fileManager.getLogFile(logFile.getLogName()), 
                "ingestion"
            )
        
        print("Ingestion Done")