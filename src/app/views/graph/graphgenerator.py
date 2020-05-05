from QGraphViz.QGraphViz import QGraphViz
from QGraphViz.DotParser import Graph
from QGraphViz.Engines import Dot

class GraphGenerator(object):
    def __init__(self, name): 
        self.name = name
        self.avlbIndex = 0
        self.nodes = dict()
        self.qgv = QGraphViz(node_invoked_callback=self.nodeInvoked)
        self.setup()

    def setup(self):
        self.qgv.new(Dot(Graph(self.name)))

        # Leaving this here for examples
        # n1 = self.qgv.addNode(self.qgv.engine.graph, "Node1", label="N1")
        # n2 = self.qgv.addNode(self.qgv.engine.graph, "Node2", label="N2")
        # n3 = self.qgv.addNode(self.qgv.engine.graph, "Node3", label="N3")
        # n4 = self.qgv.addNode(self.qgv.engine.graph, "Node4", label="N4")
        # n5 = self.qgv.addNode(self.qgv.engine.graph, "Node5", label="N5")
        # n6 = self.qgv.addNode(self.qgv.engine.graph, "Node6", label="N6")

        # self.qgv.addEdge(n1, n2, {})
        # self.qgv.addEdge(n3, n2, {})
        # self.qgv.addEdge(n2, n4, {"width":2})
        # self.qgv.addEdge(n4, n5, {"width":4})
        # self.qgv.addEdge(n4, n6, {"width":5,"color":"red"})
        # self.qgv.addEdge(n3, n6, {"width":2})

        # self.build()

    def addNode(self, **kwargs):
        if kwargs['name']:
            name = kwargs['name']
        else:  
            name = "Node" + str(self.avlbIndex)
        
        if kwargs['label']:
            label= kwargs['label']
        else:
            label = "N" + str(self.avlbIndex)
        
        if kwargs['shape']: 
            shape = kwargs['shape']
        else: 
            shape = "square"

        node = self.qgv.addNode(self.qgv.engine.graph, name, label=label, shape=shape)
        self.nodes[node] = []

    def addEdge(self, source, destination): 
        src = None
        for node in self.nodes.keys(): 
            if node.name == source: 
                src = node
                break
        
        if src == None: 
            raise Exception("No such node")
        
        dest = None
        for node in self.nodes.keys(): 
            if node.name == destination: 
                dest = node

        if dest == None: 
            raise Exception("No such node")
        
        self.nodes[src].append(dest)
        self.qgv.addEdge(src, dest, {})

    def build(self):
        self.qgv.build()

    def save(self):
        filename = self.name + ".gv"
        self.qgv.save(filename)

    def getGraph(self): 
        return self.qgv 

    def getNodes(self):
        return self.nodes.keys() 

    def nodeInvoked(self, node): 
        print(node)
