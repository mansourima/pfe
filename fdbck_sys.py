import constants
from dbconnection import db
import functions
import random
def feedback(userMongoQ, driverMongoQ, userIdQ, driverId, tripId):
    feedback = {}
    functions.update_feedback_status(userIdQ)
    userIdQ.append(driverId)
    userMongoQ.append(driverMongoQ)
    #print(userIdQ)
    user_count = len(userIdQ)
    feed_back_type = ""
    reg_user = []
    for i in range(user_count):

        riderCollection = db.ridersndrivers
        cursor = riderCollection.find({constants.MONGO_ID: userMongoQ[i]})
        reg_user = list(cursor)
        reg_chat = reg_user[0][constants.CHATTY_SCORE]
        reg_safe = reg_user[0][constants.SAFETY_SCORE]
        reg_punctual = reg_user[0][constants.PUNCTUALITY_SCORE]
        reg_friend = reg_user[0][constants.FRIENDLINESS_SCORE]
        reg_comfort = reg_user[0][constants.COMFORTIBILITY_SCORE]
        reg_user_UTT = reg_user[0][constants.UTT]

        for j in range(user_count):
            if i != j:
                ratingList = functions.uni_char_fdbck()
                chat = ratingList[0]
                safe = ratingList[1]
                punctual = ratingList[2]
                friend = ratingList[3]
                comfort = ratingList[4]

                #feedback_given_classifier, classifier_to_int = functions.get_classifier(chat, safe, punctual, friend, comfort)

                avg_rating = (chat + safe + punctual + friend + comfort) / 5

                if j == user_count-1:
                    feed_back_type = "rider_to_driver"
                elif i == user_count-1:
                    feed_back_type = "driver_to_rider"
                else:
                    feed_back_type = "rider_to_rider"

                if feed_back_type == "rider_to_driver":
                    driving_rating = random.randrange(2, 5)
                    document = {
                        "feedback_type": feed_back_type,
                        "user_who_is_rating_Mongoid": userMongoQ[i],
                        "user_who_is_rating_id": userIdQ[i],
                        "user_getting_rated_Mongoid": userMongoQ[j],
                        "user_getting_rated_id": userIdQ[j],
                        constants.CHATTY_SCORE: reg_chat,
                        constants.SAFETY_SCORE: reg_safe,
                        constants.PUNCTUALITY_SCORE: reg_punctual,
                        constants.FRIENDLINESS_SCORE: reg_friend,
                        constants.COMFORTIBILITY_SCORE: reg_comfort,
                        constants.UTT: reg_user_UTT,
                        "driver_rating": driving_rating,
                        constants.TRIP_ID: tripId,
                        constants.CHAT_RATE: chat,
                        constants.SAFE_RATE: safe,
                        constants.PUNCTUAL_RATE: punctual,
                        constants.FRIENDLINESS_RATE: friend,
                        constants.COMFORT_RATE: comfort,
                        "average_rating": avg_rating,
                        constants.TIME_STAMP: functions.getTimeStamp()
                    }
                else:

                    document = {
                        "feedback_type": feed_back_type,
                        "user_who_is_rating_Mongoid": userMongoQ[i],
                        "user_who_is_rating_id": userIdQ[i],
                        "user_getting_rated_Mongoid": userMongoQ[j],
                        "user_getting_rated_id": userIdQ[j],
                         constants.CHATTY_SCORE: reg_chat,
                         constants.SAFETY_SCORE: reg_safe,
                         constants.PUNCTUALITY_SCORE: reg_punctual,
                         constants.FRIENDLINESS_SCORE: reg_friend,
                         constants.COMFORTIBILITY_SCORE: reg_comfort,
                        constants.UTT: reg_user_UTT,
                        constants.TRIP_ID: tripId,
                        constants.CHAT_RATE: chat,
                        constants.SAFE_RATE: safe,
                        constants.PUNCTUAL_RATE: punctual,
                        constants.FRIENDLINESS_RATE: friend,
                        constants.COMFORT_RATE: comfort,
                        "average_rating": avg_rating,
                        constants.TIME_STAMP: functions.getTimeStamp()
                    }
                #print("Document de Feedback:")
                print("Evaluation donné par user", userIdQ[i], "a user", userIdQ[j], ":")
                print("Chatty Rating:", chat)
                print("Safety Rating:", safe)
                print("Punctuality Rating:", punctual)
                print("Friendliness Rating:", friend)
                print("Comfortability Rating:", comfort)
                print("")
                feedbackCollection = db.feedbackCollection
                feed_back_id = feedbackCollection.insert_one(document)