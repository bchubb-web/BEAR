import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['Bear']
collection = db["Bear_Friends"]#select collection (table) from the db
register = db["Bear_register"]
print("done")
