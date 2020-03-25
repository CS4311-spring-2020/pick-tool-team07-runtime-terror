class LogFile(object):
    def __init__(self, logFileName, cleansingStatus, validationStatus, ingestionStatus, acknowledgementStatus, pathToFile, typeOfFile):
        self.logFileName = logFileName
        self.cleansingStatus = cleansingStatus
        self.validationStatus = validationStatus
        self.ingestionStatus = ingestionStatus
        self.acknowledgementStatus = acknowledgementStatus
        self.pathToFile = pathToFile
        self.typeOfFile = typeOfFile

def setLogName(self, logFileName):
    self.logFileName = logFileName

def getLogName(self):
    return self.logFileName

def setLogCleansingStatus(self, cleansingStatus):
    self.cleansingStatus = cleansingStatus

def getLogCleansingStatus(self):
    return self.cleansingStatus

def setValidationStatus(self, validationStatus):
    self.validationStatus = validationStatus

def getValidationStatus(self):
    return self.validationStatus

def setIngestionStatus(self, ingestionStatus):
    self.ingestionStatus = ingestionStatus

def getIngestionStatus(self):
    return self.ingestionStatus

def setAcknowledgementStatus(self, acknowledgementStatus):
    self.acknowledgementStatus = acknowledgementStatus

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