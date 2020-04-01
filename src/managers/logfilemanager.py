from models.logfile import LogFile

from controllers.logfilecontroller import LogFilesController
class LogFileManager: 
    __instance = None

    def __init__(self):
        if LogFileManager.__instance == None: 
            LogFileManager.__instance = self
            self.controller = LogFilesController()
            self.logEntries = []
        else: 
            raise Exception("Trying to create another instance of a singelton class") 
    
    @staticmethod
    def get_instance(): 
        if LogFileManager.__instance == None: 
            LogFileManager()
        return LogFileManager.__instance

    def addLogFile(
        self, 
        fileName, 
        path, 
        type): 
        logfile = LogFile(fileName, path, type)
        self.logEntries.append(logfile)
        self.controller.update(**{'action':'add', 'data':logfile})