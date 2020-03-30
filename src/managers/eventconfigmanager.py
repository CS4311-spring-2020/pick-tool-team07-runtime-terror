import sys
sys.path.append('..')

from models.eventconfig import EventConfig

class EventConfigManager: 
    __instance = None
    def __init__(self):
        if EventConfigManager.__instance == None: 
            EventConfigManager.__instance = self
            self.eventconfig = EventConfig()
        else: 
            raise Exception("Trying to create another instance of a singelton class") 
    
    @staticmethod
    def get_instance(): 
        if EventConfigManager.__instance == None: 
            EventConfigManager()
        return EventConfigManager.__instance

    def setEventAttributes(self, name, desc, start, end): 
        self.eventconfig.setName(name)
        self.eventconfig.setDesc(desc)
        self.eventconfig.setStart(start)
        self.eventconfig.setEnd(end)

    def setTeamAttributes(self, lead, leadip, conn): 
        self.eventconfig.setLead(lead)
        self.eventconfig.setLeadIp(leadip)
        self.eventconfig.setConnections(conn)

    def setDirAttributes(self, rootDir, red, blue, white): 
        self.eventconfig.setRootDir(rootDir)
        self.eventconfig.setRed(red)
        self.eventconfig.setBlue(blue)
        self.eventconfig.setWhite(white)

    def getEventConfig(self): 
        return self.eventconfig