from pymongo import MongoClient

connect = MongoClient("mongodb://localhost:27017/")
db = connect["todolist-database"]
collection = db["tasks"]