class LogEntry(object): 
    def __init__(self, host, timestamp, content, source, sourceType): 
        self.number = None
        self.timestamp = timestamp
        self.content = content
        self.host = host
        self.src = source
        self.srcType = sourceType

    def setNumber(self, num):
        self.number = num

    def setTimestamp(self, timestamp): 
        self.timestamp = timestamp

    def setContent(self, content): 
        self.content = content

    def setHost(self, host):
        self.host = host

    def setSource(self, src): 
        self.src = src

    def setSourceType(self, srctype): 
        self.srcType = srctype
