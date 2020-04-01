from models.logfile import LogFile

class LogFileManager:
    __instance = None

    def __init__(self):
        if LogFileManager.__instance == None:
            LogFileManager.__instance = self
            self.logFiles = []
        else:
            raise Exception("Trying to create another instance of a singelton class")

    @staticmethod
    def get_instance():
        if LogFileManager.__instance == None:
            LogFileManager()
        return LogFileManager.__instance

    def addEntry(
            self,
            logFileName,
            pathToFile,
            typeOfFile
            ):

        # Create File
        logFile = LogFile(logFileName, pathToFile, typeOfFile)

        self.logFiles.append(logFile)

