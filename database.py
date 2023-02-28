from pymongo import MongoClient
import datetime

idKey = 'tg_user_id'
questionsKey = 'questions'
dateKey = 'date'

#sampleUser = {idKey: 1, questionsKey: 0}

class DataStore:
    def __init__(self, url='localhost', port='27017'):
        self.url = url
        self.port = int(port)
        self.client = MongoClient(self.url, self.port)
        self.db = self.client['my-database-name']

    def addUser(self, user):
        user[dateKey] = datetime.datetime.utcnow()
        user[questionsKey] = 0
        user_id = self.db.users.insert_one(user)
        return user_id
    
    def updateUser(self, user, questions):
        user[dateKey] = datetime.datetime.utcnow()
        user[questionsKey] = questions
        user_id = self.db.users.update_one(user)
        return user[idKey]

    def getUser(self, tg_user_id):
        return self.db.users.find_one({idKey: tg_user_id})

    def removeUser(self, tg_user_id):
        return self.db.users.remove({idKey: tg_user_id})

    def getAllUsers(self):
        users = []
        for user in self.db.users.find():
            users.append(user)
        return users

    def dropAllUsers(self):
        self.db.users.drop()