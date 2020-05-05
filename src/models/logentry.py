class LogEntry(object): 
    def __init__(self, number, host, timestamp, content, source, sourceType): 
        self.number = None
        self.team = None
        self.timestamp = timestamp
        self.content = content
        self.host = host
        self.src = source
        self.srcType = sourceType

    def setNumber(self, number): 
        self.number = number
    
    def getNumber(self):
        return self.number

    def getTimestamp(self): 
        return self.timestamp 

    def getContent(self): 
        return self.content

    def getHost(self):
        return self.host

    def getSource(self): 
        return self.src

    def getSourceType(self): 
        return self.srcType
