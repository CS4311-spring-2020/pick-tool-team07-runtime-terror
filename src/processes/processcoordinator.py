from .cleansingprocess import CleansingProcess
from .ingestionprocess import IngestionProcess


# This will certainly change
class ProcessCoordinator(object): 
    def __init__(self):
        self.cleansing = CleansingProcess()
        self.ingestion = IngestionProcess()

    def exec(self):
        self.cleansing.start()  
        self.ingestion.start()