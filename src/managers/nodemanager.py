from managers.base.dbmanager import DataBaseManager
from models.node import Node

class NodeManager(DataBaseManager):
    TABLE = "Node"

    def __init__(self):
        super().__init__()
        self.table = self.db[NodeManager.TABLE]

    # We will take a log entry since nodes are log entires.
    def addNode(self, logentry): 
        node = {
            'name': '', 
            'timestamp': logentry.getTimestamp(),
            'desc': logentry.getContent(), 
            'logEntryRef': logentry.getNumber(),
            'logCreator': '',
            # 'eventType': '',
            'icon': 'null',
            'source':'', 
            'visible': True
        }
        self.add(node)

    def getNodeByLogRef(self, logEntryRef): 
        query = {"logEntryRef": logEntryRef}
        results = self.get(query)

        return self.getSingleResult(results)

    def getNode(self, id): 
        query = {"_id": id}
        results = self.get(query)
        
        return self.getSingleResult(results)

    def getSingleResult(self, results): 
        for result in results: 
            node = Node(
                result['_id'], 
                result['name'],
                result['timestamp'], 
                result['desc'], 
                result['logEntryRef'],
                result['logCreator'], 
                "", 
                result['icon'], 
                result['source'], 
                result['visible']
            )
            return node