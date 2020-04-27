import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PICK"]
table = db["LogFiles"]
table.drop()

table = db["Vectors"]
table.drop()