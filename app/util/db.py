from pymongo import MongoClient
import datetime
import config

idKey = 'tg_user_id'
questionsKey = 'questions'
referralsKey = 'referrals'
dateKey = 'date'

#sampleUser = "{tg_user_id: 473104234, questions: 0, referrals: 0, date: 20230306201515}"

class DataStore:
    def __init__(self, connection_string=config.MONGODB_CONNECTION_STRING):
        self.connection_string = connection_string
        self.client = MongoClient(self.connection_string)
        self.db = self.client['ChatGPTBot']

    # called only once
    def createUser(self, telegram_user_id):
        dt = datetime.datetime.now()
        int_dt = int(dt.strftime("%Y%m%d%H%M%S"))
        result = self.db.users.insert_one({"tg_user_id": telegram_user_id, "questions": 0, "referrals": 0, "date": int_dt})
        return result.acknowledged
    
    # for each update call either this
    def updateQuestions(self, telegram_user_id, questions_num):
        dt = datetime.datetime.now()
        int_dt = int(dt.strftime("%Y%m%d%H%M%S"))
        result = self.db.users.update_one({"tg_user_id":telegram_user_id},{"$set":{"questions": questions_num, "date": int_dt}})
        return result.acknowledged
    
    # or this
    def updateReferrals(self, telegram_user_id, referrals_num):
        dt = datetime.datetime.now()
        int_dt = int(dt.strftime("%Y%m%d%H%M%S"))
        result = self.db.users.update_one({"tg_user_id":telegram_user_id},{"$set":{"referrals": referrals_num, "date": int_dt}})
        return result.acknowledged

    def getQuestions(self, telegram_user_id):
        result = self.db.users.find_one({"tg_user_id":telegram_user_id})
        if result is None:
            return -1
        else:
            return result['questions']

    def getReferrals(self, telegram_user_id):
        result = self.db.users.find_one({"tg_user_id":telegram_user_id})
        if result is None:
            return -1
        else:
            return result['referrals']
    
    def checkUserInDB(self, telegram_user_id):
        result = self.db.users.find_one({"tg_user_id":telegram_user_id})
        if result is None:
            return False
        else:
            return True
    
    def checkQuestionsLeft(self, telegram_user_id):
        result = self.db.users.find_one({"tg_user_id":telegram_user_id})
        if result['questions'] == 0:
            return False
        else:
            return True
