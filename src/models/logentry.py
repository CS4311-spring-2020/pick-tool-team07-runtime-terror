class LogEntry(object): 
    def __init__(self, host, timestamp, content, source, sourceType): 
        self.number = None
        self.timestamp = timestamp
        self.content = content
        self.host = host
        self.src = source
        self.srcType = sourceType

    # def getNumber(self, num):
    #     self.number = num

    # def getTimestamp(self, timestamp): 
    #     self.timestamp = timestamp

    # def getContent(self, content): 
    #     self.content = content

    # def getHost(self, host):
    #     self.host = host

    # def getSource(self, src): 
    #     self.src = src

    # def getSourceType(self, srctype): 
    #     self.srcType = srctype

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
