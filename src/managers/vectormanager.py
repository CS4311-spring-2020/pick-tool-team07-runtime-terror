from managers.base.dbmanager import DataBaseManager
from managers.nodemanager import NodeManager
from models.vector import Vector

class VectorManager(DataBaseManager): 
    TABLE = "Vectors"
    def __init__(self):
        super().__init__()
        self.table = self.db[VectorManager.TABLE]
        self.nodeManager = NodeManager()

    def addVector(self, name, desc): 
        v = {
            "name": name, 
            "desc": desc, 
            "nodes": []
        }# Vector(name, desc)
        self.add(v)

    def vectorExists(self, name): 
        for vector in self.get(None): 
            if vector["name"] == name: 
                return True
        return False

    def getVectors(self): 
        vectors = [
            Vector(vector["name"], vector["desc"], vector["nodes"]) for vector in self.get(None)
        ]
        return vectors

    def getVectorByName(self, name): 
        query = {"name":name}
        results = self.get(query)
        vector = None
        for result in results: 
            vector = Vector(
                result["name"], 
                result["desc"], 
                result["nodes"]
            )
            break
        return vector

    def associateLogEntry(self, logentry, vector):
        self.nodeManager.addNode(logentry)
        node = self.nodeManager.getNodeByLogRef(logentry.getNumber())

        self.table.update({"name": vector.getName()}, {"$push": {"nodes":node.getId()}})

    def updateVector(self, vector_name, name, desc): 
        query = {"name": vector_name}
        update = {"$set": {"name": name, "desc": desc} }
        self.update(query, update)

    def deleteVector(self, name):
        query = {"name": name}
        self.delete(query)

    def setCurrentVector(self, name):
        self.curVec = self.getVectorByName(name) 

    def getCurrentVector(self): 
        return self.curVec