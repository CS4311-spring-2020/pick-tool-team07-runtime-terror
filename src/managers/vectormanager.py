from models.vector import Vector

class VectorManager: 
    __instance = None

    def __init__(self):
        if VectorManager.__instance == None: 
            VectorManager.__instance = self
            self.vectors = []
            # TODO: This is bad implementation will change later
            self.curVec = None
        else: 
            raise Exception("Trying to create another instance of a singelton class") 
    
    @staticmethod
    def get_instance(): 
        if VectorManager.__instance == None: 
            VectorManager()
        return VectorManager.__instance

    def addVector(self, name, desc): 
        v = Vector(name, desc)
        self.vectors.append(v)

    def vectorExists(self, name): 
        for vector in self.vectors: 
            if vector.getName() == name: 
                return True
        return False

    def getVectors(self): 
        return self.vectors

    def getVectorByName(self, name): 
        for vector in self.getVectors(): 
            if vector.getName() == name: 
                return vector
        return None

    def updateVector(self, vector_name, name, desc): 
        for vector in self.vectors: 
            if vector.getName() == vector_name: 
                vector.setName(name)
                vector.setDesc(desc)

    def deleteVector(self, name):
        if self.vectorExists(name): 
            for vector in self.vectors: 
                if vector.getName() == name: 
                    self.vectors.remove(vector) 
                    del vector

    def setCurrentVector(self, name):
        self.curVec = self.getVectorByName(name) 

    def getCurrentVector(self): 
        return self.curVec