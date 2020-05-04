class Vector(object):
    def __init__(self, name, desc, nodes):
        self.name = name
        self.description = desc
        self.nodes = nodes

    def setName(self, name): 
        self.name = name

    def setDesc(self, desc): 
        self.description = desc

    def getName(self): 
        return self.name

    def getDesc(self): 
        return self.description

    def addNode(self): 
        # TODO: Create Node class
        # self.nodes.append()
        pass

    def getNodes(self):
        return self.nodes 

    def __str__(self): 
        return 'Vector(name='+self.name+', desc='+self.description+')'