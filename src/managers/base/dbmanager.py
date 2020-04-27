import pymongo

class DataBaseManager(object): 
    def __init__(self): 
        # Do connection to mongo db
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["PICK"]
        self.table = None

    def add(self, entry): 
        if self.table == None: 
            return 
        self.table.insert_one(entry)

    def delete(self, query): 
        if self.table == None: 
            return 
        self.table.delete_one(query)

    def get(self, query): 
        if self.table == None: 
            return 

        if query == None: 
            return self.table.find()
        
        return self.table.find(query)

    def update(self, query, update): 
        if self.table == None: 
            return
        self.table.update_one(query, update)
