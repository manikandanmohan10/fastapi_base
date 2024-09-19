from pymongo import MongoClient

client = MongoClient("mongodb://root:123@192.168.32.2:27017/?retryWrites=true&w=majority")
db = client['sample_mflix']


# collection = db['users']
# collection.create_index("email", unique=True)
# collection.create_index("phone_number", unique=True)