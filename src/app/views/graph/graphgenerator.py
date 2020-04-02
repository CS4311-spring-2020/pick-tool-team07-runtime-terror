from QGraphViz.QGraphViz import QGraphViz
from QGraphViz.DotParser import Graph
from QGraphViz.Engines import Dot

class GraphGenerator(object):
    def __init__(self): 
        self.setup()

    def setup(self):
        self.avlbIndex = 0
        self.nodes = dict()
        self.qgv = QGraphViz(node_invoked_callback=self.nodeInvoked)
        self.qgv.new(Dot(Graph("Main_Graph")))

        n1 = self.qgv.addNode(self.qgv.engine.graph, "Node1", label="N1")
        n2 = self.qgv.addNode(self.qgv.engine.graph, "Node2", label="N2")
        n3 = self.qgv.addNode(self.qgv.engine.graph, "Node3", label="N3")
        n4 = self.qgv.addNode(self.qgv.engine.graph, "Node4", label="N4")
        n5 = self.qgv.addNode(self.qgv.engine.graph, "Node5", label="N5")
        n6 = self.qgv.addNode(self.qgv.engine.graph, "Node6", label="N6")

        self.qgv.addEdge(n1, n2, {})
        self.qgv.addEdge(n3, n2, {})
        self.qgv.addEdge(n2, n4, {"width":2})
        self.qgv.addEdge(n4, n5, {"width":4})
        self.qgv.addEdge(n4, n6, {"width":5,"color":"red"})
        self.qgv.addEdge(n3, n6, {"width":2})

        self.build()

    def generateVectorGraph(self, vector):
        pass 

    def addNode(self, name, label=(False, None)):
        if name == None: 
            name = "Node" + self.avlbIndex
            self.avlbIndex += 1
        
        lbl = None
        if label[0]:
            if label[1] == None:  
                lbl = "N" + self.avlbIndex
            else: 
                lbl = label[1]
        
        node = self.qgv.addNode(self.qgv.engine.graph, name, label=lbl)
        self.nodes[name] = node

    def addEdge(self, source, dest): 
        if source in self.nodes: 
            srcNode = self.nodes[source]
        else: 
            raise Exception("No such node exists")

        if dest in self.nodes: 
            dstNode = self.nodes[dest]
        else: 
            raise Exception("No such node exists")

        self.qgv.addEdge(srcNode, dstNode, {})

    def build(self):
        self.qgv.build()

    def save(self, name):
        filename = name + ".gv"
        self.qgv.save(filename)

    def getGraph(self): 
        return self.qgv 

    def nodeInvoked(self, node): 
        print(node)
