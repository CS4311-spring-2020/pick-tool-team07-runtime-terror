class LogFile(object):
    def __init__(self, logFileName, pathToFile, typeOfFile):
        self.logFileName = logFileName
        self.cleansingStatus = False
        self.validationStatus = False
        self.ingestionStatus = False
        self.acknowledgementStatus = False
        self.pathToFile = pathToFile
        self.typeOfFile = typeOfFile

    def setLogName(self, logFileName):
        self.logFileName = logFileName

    def getLogName(self):
        return self.logFileName

    def getLogCleansingStatus(self):
        return self.cleansingStatus

    def setCleansingStatus(self, status):
        self.cleansingStatus = status 

    def getValidationStatus(self):
        return self.validationStatus

    def getIngestionStatus(self):
        return self.ingestionStatus

    def setIngestionStatus(self, status): 
        self.ingestionStatus = status

    def getAcknowledgementStatus(self):
        return self.acknowledgementStatus

    def setPathToFile(self, pathToFile):
        self.pathToFile = pathToFile

    def getPathToFile(self):
        return self.pathToFile

    def setTypeOfFile(self, typeOfFile):
        self.typeOfFile = typeOfFile

    def getTypeOfFile(self):
        return self.typeOfFile

    def __str__(self): 
        return 'Log File(name=' + self.logFileName+', cleansing status =' + self.cleansingStatus+ ', validation status =' + self.validationStatus+ ', ingestion status =' + self.ingestionStatus+ ', acknowledgement status =' + self.acknowledgementStatus+ ', file path =' + self.pathToFile+ ',type ='+ self.typeOfFile+')'