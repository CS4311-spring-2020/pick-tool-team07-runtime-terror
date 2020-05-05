from app.views.graph.graphgenerator import GraphGenerator
from managers.nodemanager import NodeManager
class GraphManager(object): 

    def __init__(self):
        self.graphs = dict()
        self.nodeManager = NodeManager()

    def getGraph(self, vector):
        if vector.getName() in self.graphs.keys(): 
            return self.graphs[vector.getName()].getGraph()

        # Generate the graph if we havent generated it for the vecotr
        self.generateGraph(vector)
        return self.graphs[vector.getName()].getGraph()

    def generateGraph(self, vector): 
        gGenerator = GraphGenerator(vector.getName())
        nodes = vector.getNodes()

        for nodeid in nodes: 
            node = self.nodeManager.getNode(nodeid)
            gGenerator.addNode(**{
                "name": node.getName(), 
                "label": "", 
                "shape": node.getIcon()
            })
        gGenerator.build()
        self.graphs[vector.getName()] = gGenerator

    def addNode(self, vector, **kwargs): 
        self.graphs[vector.getName()].addNode(**kwargs)
        self.graphs[vector.getName()].build()

    def addEdge(self, vector, src, dest): 
        self.graphs[vector.getName()].addEdge(src, dest)
        self.graphs[vector.getName()].build()

     