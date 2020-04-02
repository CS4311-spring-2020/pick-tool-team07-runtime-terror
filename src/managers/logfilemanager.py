from models.logfile import LogFile
from controllers.logfilecontroller import LogFilesController

class LogFileManager:
    __instance = None

    def __init__(self):
        if LogFileManager.__instance == None:
            LogFileManager.__instance = self
            self.logFiles = []
            self.controller = LogFilesController()
        else:
            raise Exception("Trying to create another instance of a singelton class")

    @staticmethod
    def get_instance():
        if LogFileManager.__instance == None:
            LogFileManager()
        return LogFileManager.__instance

    def addLogFile(
        self,
        logFileName,
        pathToFile,
        typeOfFile
    ):

        # Create File
        logFile = LogFile(logFileName, pathToFile, typeOfFile)
        self.logFiles.append(logFile)
        #self.controller.update(**{'action':'add', 'data':logFile})

    def getLogFiles(self): 
        return self.logFiles

    def getLogFile(self, name):
        for file in self.logFiles: 
            if name == file.getLogName(): 
                return file 
        return None

    def updateCleanseStatus(self, name, status):
        for file in self.logFiles: 
            if name == file.getLogName(): 
                file.setCleansingStatus(status) 


