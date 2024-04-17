from datetime import datetime
import random
from dbconnection import db
import constants
import functions
import operator
from pymongo import MongoClient, database
from pymongo.server_api import ServerApi

for userId in range(237117,300001):
        
        ridersCollection = db.ridersndrivers
        char = functions.uni_char()


        charDict = {constants.CHATTY_SCORE: char[0],
                     constants.SAFETY_SCORE: char[1],
                     constants.PUNCTUALITY_SCORE: char[2],
                     constants.FRIENDLINESS_SCORE: char[3],
                     constants.COMFORTIBILITY_SCORE: char[4]}
                     
        reg_classifier = max(charDict, key=charDict.get)
        utt = random.randrange(2, 7)
        utt = utt * 5
        

        activeUser = ""
        activeUserStatus = random.random()
        if activeUserStatus > 0.7:
            activeUser = constants.NO
        else:
            activeUser = constants.YES
        

        broadcasting = ""
        broadcastingStatus = random.random()
        if broadcastingStatus > 0.7:
            broadcasting = constants.YES
        else:
            broadcasting = constants.NO
        
        sourceZone = random.randrange(1, 263)
        source = functions.generate_location(sourceZone)
        

        #Rider Document
        riders = {constants.USER_ID: userId,
                    constants.CHAR_DICT: charDict,
                    constants.CHATTY_SCORE: char[0],
                    constants.SAFETY_SCORE: char[1],
                    constants.PUNCTUALITY_SCORE: char[2],
                    constants.FRIENDLINESS_SCORE: char[3],
                    constants.COMFORTIBILITY_SCORE: char[4],
                    constants.REG_CLASSIFIER: reg_classifier,
                    constants.ALSO_DRIVER: constants.NO,
                    constants.UTT: utt,
                    constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING),
                    constants.ACTIVE_STATE: constants.NO,
                    constants.CURRENT_ZONE: sourceZone,
                    constants.CURRENT_LOCATION: source,
                    constants.BROADCASTING: broadcasting,
                    "pred_class_given": constants.NO,
                    "trip_given_class":{},
                    "pred_class_got": constants.NO,
                    "trip_got_class":{},
                    "trip_nbr": 0,
                    constants.FEEDBACK_GIVEN: constants.NO,
                    constants.FEEDBACK_GOT_CHAT: 0,
                    constants.FEEDBACK_GOT_SAFE: 0,
                    constants.FEEDBACK_GOT_PUNCTUAL: 0,
                    constants.FEEDBACK_GOT_FRIEND: 0,
                    constants.FEEDBACK_GOT_COMFORT: 0,
                    constants.RATINGS_GOT_DICT: {},
                    constants.GOT_FEEDBACK_CLASSIFIER: constants.EMPTY_STRING,
                    constants.GIVEN_RATING_CHAT: 0,
                    constants.GIVEN_RATING_SAFE: 0,
                    constants.GIVEN_RATING_PUNCTUAL: 0,
                    constants.GIVEN_RATING_FRIEND: 0,
                    constants.GIVEN_RATING_COMFORT: 0,
                    constants.VARIANCE_DICT: {},
                    constants.GIVEN_FEEDBACK_CLASSIFIER: constants.EMPTY_STRING,

                  }
        rider_ids = ridersCollection.insert_one(riders)
        

count = ridersCollection.count_documents({})

print('Found ', count, 'records')