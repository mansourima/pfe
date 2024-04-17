from datetime import datetime
import random
from dbconnection import db
import constants
import functions

for userId in range(300001, 400001):

        ridersCollection = db.ridersndrivers
        char = functions.uni_char()


        charDict = {constants.CHATTY_SCORE: char[0],
                     constants.SAFETY_SCORE: char[1],
                     constants.PUNCTUALITY_SCORE: char[2],
                     constants.FRIENDLINESS_SCORE: char[3],
                     constants.COMFORTIBILITY_SCORE: char[4]}
        utt = random.randrange(2, 7)
        utt = utt * 5

        reg_classifier = max(charDict, key=charDict.get)

        sourceZone = random.randrange(1, 263)
        source = functions.generate_location(sourceZone)

        """luggageCarrierRandom = random.random()
        if luggageCarrierRandom > 0.5:
                luggageCarrier = constants.YES
        else:
                luggageCarrier = constants.NO"""

        activeUser = ""
        activeUserStatus = random.random()
        if activeUserStatus > 0.7:
            activeUser = constants.NO
        else:
            activeUser = constants.YES

        seatCapacity = random.randrange(3, 5)
        #Driver Document
        riders = {constants.USER_ID: userId,
                    constants.CHAR_DICT: charDict,
                    constants.CHATTY_SCORE: char[0],
                    constants.SAFETY_SCORE: char[1],
                    constants.PUNCTUALITY_SCORE: char[2],
                    constants.FRIENDLINESS_SCORE: char[3],
                    constants.COMFORTIBILITY_SCORE: char[4],
                    constants.REG_CLASSIFIER: reg_classifier,
                    constants.UTT: utt,
                    constants.ALSO_DRIVER: constants.YES,
                    constants.SEAT_CAPACITY: seatCapacity,
                    constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING),
                    constants.ACTIVE_STATE: activeUser,
                    constants.CURRENT_ZONE: sourceZone,
                    constants.CURRENT_LOCATION: source,
                    constants.FEEDBACK_GIVEN: constants.NO,
                    "pred_class_given": constants.NO,
                    "trip_given_class":{},
                    "pred_class_got": constants.NO,
                    "trip_got_class":{},
                    "trip_nbr": 0,
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