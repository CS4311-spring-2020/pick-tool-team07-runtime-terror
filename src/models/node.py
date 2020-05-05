class Node(object): 
    def __init__(
        self, 
        id, 
        name,
        timestamp, 
        desc, 
        logEntryRef, 
        logCreator, 
        eventType, 
        icon, 
        source, 
        visible): 
        self.id = id 
        self.name = name
        self.timestamp = timestamp 
        self.desc = desc 
        self.logEntryRef = logEntryRef 
        self.logCreator = logCreator
        self.eventType = eventType
        self.icon = icon 
        self.source = source 
        self.visible = visible 

    #TODO: Add getters and setters for each attribute
    def getId(self):
        return self.id

    def getName(self): 
        return self.name
    
    def getTimeStamp(self): 
        return self.timestamp

    def getDesc(self): 
        return self.desc

    def getLogEntryRef(self):
        return self.logEntryRef

    def getLogCreator(self): 
        return self.logCreator

    def getIcon(self): 
        return self.icon

    def getSource(self): 
        return self.source

    def getVisible(self): 
        return self.visible
