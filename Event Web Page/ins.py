from pymongo import MongoClient
client =MongoClient("mongodb://admin:KpwapmRB65diQlCt@SG-H2KSP-52430.servers.mongodirector.com:27017/admin")

db = client['events']
users = db['users']
posts = db['posts']

users.insert_one({"username": "foodadmin",  "password": "c235548cfe84fc87678ff04c9134e060cdcd7512d09ed726192151a995541ed8db9fda5204e72e7ac268214c322c17787c70530513c59faede52b7dd9ce64331",  "clubname": "food"})

for i in users.find():
    print(i)