from models.logentry import LogEntry

class LogEntryManager: 
    __instance = None

    def __init__(self):
        if LogEntryManager.__instance == None: 
            LogEntryManager.__instance = self
            self.logEntries = []
        else: 
            raise Exception("Trying to create another instance of a singelton class") 
    
    @staticmethod
    def get_instance(): 
        if LogEntryManager.__instance == None: 
            LogEntryManager()
        return LogEntryManager.__instance

    def addEntry(
        self, 
        host, 
        timestamp, 
        content, 
        source, 
        sourceType): 

        # Create Entry
        logEntry = LogEntry(host, timestamp, content, source, sourceType)

        self.logEntries.append(logEntry)

        # TODO: Need to add this log entry to log entry database in the case we do 
        # have a db for log entries
    
    def getEntryByContent(self, content):   
        for entry in self.logEntries: 
            if content == entry.getContent(): 
                return entry
        return None
