from definition import CONFIG_PATH
from configparser import ConfigParser

class ConfigManager(object): 

    def __init__(self): 
        self.parser = ConfigParser()
        self.parser.read(CONFIG_PATH)

    def getConfig(self, config): 
        return self.parser[config]

    def writeConfig(self, section, config): 
        self.parser[section] = config
        with open(CONFIG_PATH, 'w') as f: 
            self.parser.write(f)

    def updateSection(self, section, attribute, value): 
        self.parser[section][attribute] = value
        with open(CONFIG_PATH, 'w') as f: 
            self.parser.write(f)