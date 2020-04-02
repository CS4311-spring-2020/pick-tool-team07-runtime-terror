
class EventConfig(object): 
    def __init__(self):
        self.name = None 
        self.desc = None
        self.start = None 
        self.end = None
        self.rootDir = None    
        self.redFolder = None 
        self.blueFolder = None
        self.whiteFolder = None
        self.lead = None 
        self.leadIp = None 
        self.connections = None 
    
    def setName(self, name):
        self.name = name

    def setDesc(self, desc): 
        self.desc = desc

    def setStart(self, start): 
        self.start = start

    def setEnd(self, end): 
        self.end = end

    def setRootDir(self, rootDir): 
        self.rootDir = rootDir

    def setRed(self, red):
        self.redFolder = red

    def setBlue(self, blue): 
        self.blueFolder = blue

    def setWhite(self, white):
        self.whiteFolder = white

    def setLead(self, lead): 
        self.lead = lead

    def setLeadIp(self, ip):
        self.leadIp = ip

    def setConnections(self, conn):
        self.connections = conn     
    
    def getName(self):
        return self.name 

    def getDesc(self): 
        return self.desc

    def getStart(self): 
        return self.start

    def getEnd(self): 
        return self.end

    def getRootDir(self): 
        return self.rootDir

    def getRed(self):
        return self.redFolder 

    def getBlue(self): 
        return self.blueFolder

    def getWhite(self):
        return self.whiteFolder

    def getLead(self): 
        return self.lead

    def getLeadIp(self):
        return self.leadIp

    def getConnections(self, conn):
        self.connections = conn     
    

    
