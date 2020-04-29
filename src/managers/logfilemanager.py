from managers.base.dbmanager import DataBaseManager

from models.logfile import LogFile

class LogFileManager(DataBaseManager):
    # __instance = None

    # def __init__(self):
    #     if LogFileManager.__instance == None:
    #         LogFileManager.__instance = self
    #         self.logFiles = []
    #     else:
    #         raise Exception("Trying to create another instance of a singelton class")

    # @staticmethod
    # def get_instance():
    #     if LogFileManager.__instance == None:
    #         LogFileManager()
    #     return LogFileManager.__instance

    TABLE = "LogFiles"
    def __init__(self): 
        super().__init__()
        self.table = self.db[LogFileManager.TABLE]


    def addLogFile(
        self,
        logFileName,
        pathToFile,
        typeOfFile
    ):

        # Create File
        # TODO add the rest of the attributes that make up 
        # a log file
        logFile = {
            "name": logFileName,
            "path": pathToFile,
            "type": typeOfFile, 
            "cleansingStatus": "null",  
            "validationStatus": "null", 
            "ingestionStatus": "null", 
            "acknowledgementStatus": False
        }
        
        # LogFile(logFileName, pathToFile, typeOfFile)
        self.add(logFile)
        # self.logFiles.append(logFile)

    def getLogFiles(self): 
        logFiles = []
        for log in self.get(None): 
            logFile = LogFile(
                log['name'], 
                log['path'], 
                log['type'], 
                log['cleansingStatus'], 
                log['validationStatus'], 
                log['ingestionStatus'], 
                log['acknowledgementStatus']
            ) 
            logFiles.append(logFile)
        return logFiles

    def getLogFile(self, name):
        query = {"name": name}
        results = self.get(query)
        
        logFile = None
        for result in results: 
            logFile = LogFile(
                result['name'], 
                result['path'], 
                result['type'], 
                result['cleansingStatus'], 
                result['validationStatus'], 
                result['ingestionStatus'], 
                result['acknowledgementStatus']
            )
            break
        
        return logFile

    def updateCleanseStatus(self, name, status):
        query = {"name": name}
        update = {"$set": {"cleansingStatus": status}}

        self.update(query, update)

    def updateValidationStatus(self, name, status): 
        query = {"name": name}
        update = {"$set": {"validationStatus": status}}

        self.update(query, update)

    def updateIngestionStatus(self, name, status): 
        query = {"name": name}
        update = {"$set": {"ingestionStatus": status}}

        self.update(query, update)

    def updateAcknowledgementStatus(self, name, status): 
        query = {"name": name}
        update = {"$set": {"acknowledgementStatus": status}}

        self.update(query, update)
