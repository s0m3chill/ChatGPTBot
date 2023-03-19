from pymongo import MongoClient
import datetime
import config

idKey = 'tg_user_id'
questionsKey = 'questions'
referralsKey = 'referrals'
dateKey = 'date'

class DataStore:
    # check if Init is needed here
    # def __init__(self, connection_string=config.MONGODB_CONNECTION_STRING):
    #     self.connection_string = connection_string
    #     self.client = MongoClient(self.connection_string)
    #     self.db = self.client['CheatQuestionBot']

    async def connect(self, connection_string=config.MONGODB_CONNECTION_STRING):
        self.connection_string = connection_string
        self.client = MongoClient(self.connection_string)
        self.db = self.client['CheatQuestionBot']
        # self.db.connect()    check if 'connect is needed'

    async def disconnect(self):
        self.db.disconnect()

    # called only once
    def createUser(self, telegram_user_id):
        dt = datetime.datetime.now()
        int_dt = int(dt.strftime("%Y%m%d%H%M%S"))
        result = self.db.users.insert_one({idKey: telegram_user_id, questionsKey: 0, referralsKey: 0, dateKey: int_dt})
        return result.acknowledged
    
    # for each update call either this
    def updateQuestions(self, telegram_user_id, questions_num):
        dt = datetime.datetime.now()
        int_dt = int(dt.strftime("%Y%m%d%H%M%S"))
        result = self.db.users.update_one({idKey:telegram_user_id},{"$set":{questionsKey: questions_num, dateKey: int_dt}})
        return result.acknowledged
    
    # or this
    def updateReferrals(self, telegram_user_id, referrals_num):
        dt = datetime.datetime.now()
        int_dt = int(dt.strftime("%Y%m%d%H%M%S"))
        result = self.db.users.update_one({idKey:telegram_user_id},{"$set":{referralsKey: referrals_num, dateKey: int_dt}})
        return result.acknowledged

    def getQuestions(self, telegram_user_id):
        result = self.db.users.find_one({idKey:telegram_user_id})
        if result is None:
            return -1
        else:
            return result[questionsKey]

    def getReferrals(self, telegram_user_id):
        result = self.db.users.find_one({idKey:telegram_user_id})
        if result is None:
            return -1
        else:
            return result[referralsKey]
    
    def checkUserInDB(self, telegram_user_id):
        result = self.db.users.find_one({idKey:telegram_user_id})
        if result is None:
            return False
        else:
            return True
    
    def checkQuestionsLeft(self, telegram_user_id):
        result = self.db.users.find_one({idKey:telegram_user_id})
        if result[questionsKey] == 0:
            return False
        else:
            return True