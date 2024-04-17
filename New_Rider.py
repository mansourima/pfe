from datetime import datetime
import random
from dbconnection import db
import constants
import functions
import operator
from joblib.compressor import _XZ_PREFIX
import pandas as pd
import numpy as np
from dbconnection import db
from sklearn.svm import SVC
from datetime import datetime
import constants
import random
from joblib import load
import pickle
import Make_Trip
from sklearn.preprocessing import RobustScaler,MinMaxScaler,StandardScaler
import pymongo


def gen_new_rider():
        IdCollection = db.ridersndrivers
        latest_document = IdCollection.find_one({}, sort=[("userId", pymongo.DESCENDING)]) 
        userId = latest_document["userId"]+1
        ridersCollection = db.ridersndrivers   

        char = functions.uni_char()

        chattyScore = char[0]
        safetyScore = char[1]
        punctualityScore = char[2]
        friendlinessScore = char[3]
        comfartabilityScore = char[4]


        charDict = {constants.CHATTY_SCORE: chattyScore,
                     constants.SAFETY_SCORE: safetyScore,
                     constants.PUNCTUALITY_SCORE: punctualityScore,
                     constants.FRIENDLINESS_SCORE: friendlinessScore,
                     constants.COMFORTIBILITY_SCORE: comfartabilityScore}

        reg_classifier = max(charDict, key=charDict.get)
        utt = random.randrange(2, 7)
        utt = utt*5

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

        #Document de passager
        riders = {constants.USER_ID: userId,
                    constants.CHAR_DICT: charDict,
                    constants.CHATTY_SCORE: chattyScore,
                    constants.SAFETY_SCORE: safetyScore,
                    constants.PUNCTUALITY_SCORE: punctualityScore,
                    constants.FRIENDLINESS_SCORE: friendlinessScore,
                    constants.COMFORTIBILITY_SCORE: comfartabilityScore,
                    constants.REG_CLASSIFIER: reg_classifier,
                    constants.ALSO_DRIVER: constants.NO,
                    constants.UTT: utt,
                    constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING),
                    constants.ACTIVE_STATE: constants.NO,
                    constants.CURRENT_ZONE: sourceZone,
                    constants.CURRENT_LOCATION: source,
                    constants.BROADCASTING: broadcasting,
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
        print("userId de passager: ", userId)
        rider_ids = ridersCollection.insert_one(riders)


        X= [[utt, chattyScore, safetyScore,punctualityScore, friendlinessScore, comfartabilityScore]]

        filename = "svm_give"
        saved_given_reg = pickle.load(open(filename, 'rb'))
        classifier_super_test = saved_given_reg.predict(X)
        value_classifier_super_test = classifier_super_test[0]
        int_round_classifier_super_test = int(value_classifier_super_test)
        string_give_novariance = convertor1(int_round_classifier_super_test)

        filename = "svm_got"
        saved_given_reg = pickle.load(open(filename, 'rb'))
        classifier_super_test = saved_given_reg.predict(X)
        value_classifier_super_test = classifier_super_test[0]
        int_round_classifier_super_test = int(value_classifier_super_test)
        string_got_novariance = convertor1(int_round_classifier_super_test)

        ridersCollection.find_one_and_update({constants.USER_ID: userId},
                                             {"$set": {
                                                 constants.GIVEN_FEEDBACK_CLASSIFIER: string_give_novariance,
                                                 constants.GOT_FEEDBACK_CLASSIFIER: string_got_novariance,
                                                 constants.FEEDBACK_GIVEN: constants.YES,
                                                 "pred_class_given": string_give_novariance,
                                                 f"trip_given_class.0": string_give_novariance,                                                
                                                 "pred_class_got": string_got_novariance,
                                                 f"trip_got_class.0": string_got_novariance
                                                 
                                             }})

        destination = functions.generate_random_location()

        users, trip_id=Make_Trip.mainResults(userId,utt,source,destination)
        print("les passager de ce trajet sont :" ,users)
        print("Numero de trajet :",trip_id)

def convertor1(int_round_classifier_super_test):
    string_give = ""
    if int_round_classifier_super_test == 1:

        string_give = constants.CHATTY_SCORE
    elif int_round_classifier_super_test == 2:
        string_give = constants.SAFETY_SCORE

    elif int_round_classifier_super_test == 3:
        string_give = constants.PUNCTUALITY_SCORE

    elif int_round_classifier_super_test == 4:
        string_give = constants.FRIENDLINESS_SCORE

    elif int_round_classifier_super_test == 5:
        string_give = constants.COMFORTIBILITY_SCORE

    return string_give
gen_new_rider()