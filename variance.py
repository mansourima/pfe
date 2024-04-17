import statistics
import constants
from datetime import datetime
from dbconnection import db


#Giving Classifier
def variance_given_classifier(userid):
    #ridercollection = db.ridersndrivers
    for j in range(len(userid)):
        chat = []
        safe = []
        punctual = []
        comfort = []
        friend = []
        feedbackCollection = db.feedbackCollection
        cursor = feedbackCollection.find({"user_who_is_rating_id": userid[j]})
        riderFdBack = list(cursor)
        #print(len(riderFdBack))
        for i in range(len(riderFdBack)):
            chat.append(riderFdBack[i][constants.CHAT_RATE])
            safe.append(riderFdBack[i][constants.SAFE_RATE])
            punctual.append(riderFdBack[i][constants.PUNCTUAL_RATE])
            friend.append(riderFdBack[i][constants.FRIENDLINESS_RATE])
            comfort.append(riderFdBack[i][constants.COMFORT_RATE])

        chat_var = statistics.pvariance(chat)
        safe_var = statistics.pvariance(safe)
        punctual_var = statistics.pvariance(punctual)
        friend_var = statistics.pvariance(friend)
        comfort_var = statistics.pvariance(comfort)

        chat_variance = round(chat_var, 1)
        safe_variance = round(safe_var, 1)
        punctual_variance = round(punctual_var, 1)
        friend_variance = round(friend_var, 1)
        comfort_variance = round(comfort_var, 1)


        datalist = {
             constants.CHATTY_SCORE: chat_variance,
             constants.SAFETY_SCORE: safe_variance,
             constants.PUNCTUALITY_SCORE: punctual_variance,
             constants.FRIENDLINESS_SCORE: friend_variance,
             constants.COMFORTIBILITY_SCORE: comfort_variance
             }
        max_score = round(max(datalist.values()), 2)
        max_key = max(datalist, key=datalist.get)

        ridersndrivers = db.ridersndrivers
        cursor = ridersndrivers.find({
            constants.USER_ID: userid[j]})
        cursorRandomUser = list(cursor)
        trip_nbr = cursorRandomUser[0]["trip_nbr"] +1
        ridersndrivers.find_one_and_update({constants.USER_ID: userid[j]},
                                           {"$inc": {
                                                 "trip_nbr": 1,  # Incrémente le champ trip_nbr de 1
                                             },
                                           "$set":{constants.GIVEN_RATING_CHAT: chat,
                                                    constants.GIVEN_RATING_SAFE: safe,
                                                    constants.GIVEN_RATING_PUNCTUAL: punctual,
                                                    constants.GIVEN_RATING_FRIEND: friend,
                                                    constants.GIVEN_RATING_COMFORT: comfort,
                                                    constants.VARIANCE_DICT: datalist,
                                                    constants.GIVEN_FEEDBACK_CLASSIFIER: max_key,
                                                    f"trip_given_class.{trip_nbr}": max_key,
                                                     
                                                     }
                                             })
        cursor = ridersndrivers.find({constants.USER_ID: userid[j]})
        list_data = list(cursor)
        given_fdbk_classifier_int = 0
        if max_key == constants.CHATTY_SCORE:
            given_fdbk_classifier_int = 1
        elif max_key == constants.SAFETY_SCORE:
            given_fdbk_classifier_int = 2
        elif max_key == constants.PUNCTUALITY_SCORE:
            given_fdbk_classifier_int = 3
        elif max_key == constants.FRIENDLINESS_SCORE:
            given_fdbk_classifier_int = 4
        elif max_key == constants.COMFORTIBILITY_SCORE:
            given_fdbk_classifier_int = 5

        give_fdbck_data = db.Give_Fdbck_Train

        cursor_check = give_fdbck_data.find({constants.USER_ID:userid[j]})
        check_list = list(cursor_check)
        #print(check_list)
        if check_list == [] or check_list == constants.EMPTY_STRING or check_list == None:
            train_fdbck_givendocument = {
                constants.USER_ID: list_data[0][constants.USER_ID],
                constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                constants.VARIANCE_DICT: datalist,
                constants.UTT: list_data[0][constants.UTT],
                "max_variance": max_score,
                constants.GIVEN_FEEDBACK_CLASSIFIER: max_key,
                constants.GIVEN_FEEDBACK_CLASSIFIER_INT: given_fdbk_classifier_int,
                "trip_nbr": 1,
                "trip_given_class":{str(trip_nbr):max_key},
                constants.TIME_STAMP: datetime.now()
                
            }

            give_fdbck_id = give_fdbck_data.insert_one(train_fdbck_givendocument)
        else:
            give_fdbck_data.find_one_and_update({constants.USER_ID: userid[j]},
                                            {"$inc": {
                                                 "trip_nbr": 1,  # Incrémente le champ trip_nbr de 1
                                             },
                                              "$set":    {constants.USER_ID: list_data[0][constants.USER_ID],
                                                         constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                                                         constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                                                         constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                                                         constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                                                         constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                                                         constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                                                         constants.VARIANCE_DICT: datalist,
                                                         constants.UTT: list_data[0][constants.UTT],
                                                         "max_variance": max_score,
                                                         constants.GIVEN_FEEDBACK_CLASSIFIER: max_key,
                                                         constants.GIVEN_FEEDBACK_CLASSIFIER_INT: given_fdbk_classifier_int,
                                                         f"trip_given_class.{trip_nbr}":max_key,
                                                         constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)
                                                      }})

    return constants.EMPTY_STRING


#Got Classifier
def variance_got_classifier(userid):
    for j in range(len(userid)):
        rated_chat = 0
        rated_safe = 0
        rated_punctual = 0
        rated_friend = 0
        rated_comfort = 0
        feedbackCollection = db.feedbackCollection
        cursor = feedbackCollection.find({"user_getting_rated_id": userid[j]})
        dataList = list(cursor)
        for i in range(0, len(dataList)):
            if dataList[i] == {} or dataList[i] == None:
                ""
            else:
                user_rating_the_rider = dataList[i]["user_who_is_rating_id"]
                if user_rating_the_rider == "" or user_rating_the_rider == None:
                    ""
                else:
                    riders = db.ridersndrivers
                    rider_cursor = riders.find({constants.USER_ID: user_rating_the_rider})
                    rider_data_list = list(rider_cursor)
                    variance_dict = rider_data_list[0][constants.VARIANCE_DICT]

                    rated_chat += dataList[i][constants.CHAT_RATE] * variance_dict[constants.CHATTY_SCORE]
                    rated_safe += dataList[i][constants.SAFE_RATE] * variance_dict[constants.SAFETY_SCORE]
                    rated_punctual += dataList[i][constants.PUNCTUAL_RATE] * variance_dict[constants.PUNCTUALITY_SCORE]
                    rated_friend += dataList[i][constants.FRIENDLINESS_RATE] * variance_dict[constants.FRIENDLINESS_SCORE]
                    rated_comfort += dataList[i][constants.COMFORT_RATE] * variance_dict[constants.COMFORTIBILITY_SCORE]

        class_dict = {constants.CHATTY_SCORE: rated_chat, constants.SAFETY_SCORE: rated_safe, constants.PUNCTUALITY_SCORE: rated_punctual,
                      constants.FRIENDLINESS_SCORE: rated_friend, constants.COMFORTIBILITY_SCORE: rated_comfort}
        max_score = max(class_dict.values())
        max_key = max(class_dict, key=class_dict.get)

        ridersndrivers = db.ridersndrivers
        cursor = ridersndrivers.find({
            constants.USER_ID: userid[j]})
        cursorRandomUser = list(cursor)
        trip_nbr = cursorRandomUser[0]["trip_nbr"]
        ridersndrivers.find_one_and_update({constants.USER_ID: userid[j]},
                                            {"$set": {constants.FEEDBACK_GOT_CHAT: rated_chat,
                                                     constants.FEEDBACK_GOT_SAFE: rated_safe,
                                                     constants.FEEDBACK_GOT_PUNCTUAL: rated_punctual,
                                                     constants.FEEDBACK_GOT_FRIEND: rated_friend,
                                                     constants.FEEDBACK_GOT_COMFORT: rated_comfort,
                                                     constants.RATINGS_GOT_DICT: class_dict,
                                                     constants.GOT_FEEDBACK_CLASSIFIER: max_key,
                                                     f"trip_got_class.{trip_nbr}": max_key,
                                                     }})
        cursor = ridersndrivers.find({constants.USER_ID: userid[j]})
        list_data = list(cursor)
        got_fdbk_classifier_int = 0
        if max_key == constants.CHATTY_SCORE:
            got_fdbk_classifier_int = 1
        elif max_key == constants.SAFETY_SCORE:
            got_fdbk_classifier_int = 2
        elif max_key == constants.PUNCTUALITY_SCORE:
            got_fdbk_classifier_int = 3
        elif max_key == constants.FRIENDLINESS_SCORE:
            got_fdbk_classifier_int = 4
        elif max_key == constants.COMFORTIBILITY_SCORE:
            got_fdbk_classifier_int = 5

        got_fdbck_data = db.Got_Fdbck_Train

        cursor_check = got_fdbck_data.find({constants.USER_ID: userid[j]})
        check_list = list(cursor_check)
        #print(check_list)
        if check_list == [] or check_list == constants.EMPTY_STRING or check_list == None:
            train_fdbck_gotdocument = {
                constants.USER_ID: list_data[0][constants.USER_ID],
                constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                constants.RATINGS_GOT_DICT: class_dict,
                constants.UTT: list_data[0][constants.UTT],
                "max_rating_with_variance": max_score,
                constants.GOT_FEEDBACK_CLASSIFIER: max_key,
                constants.GOT_FEEDBACK_CLASSIFIER_INT: got_fdbk_classifier_int,
                "trip_nbr": 1,
                "trip_got_class":{str(trip_nbr):max_key},
                constants.TIME_STAMP: datetime.now()
            }

            got_fdbck_id = got_fdbck_data.insert_one(train_fdbck_gotdocument)
        else:
            got_fdbck_data.find_one_and_update({constants.USER_ID: userid[j]},
                                                {"$inc": {
                                                 "trip_nbr": 1,  # Incrémente le champ trip_nbr de 1
                                                         },
                                                  "$set": {
                                                    constants.USER_ID: list_data[0][constants.USER_ID],
                                                    constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                                                    constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                                                    constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                                                    constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                                                    constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                                                    constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                                                    constants.RATINGS_GOT_DICT: class_dict,
                                                    constants.UTT: list_data[0][constants.UTT],
                                                    "max_rating_with_variance": max_score,
                                                    constants.GOT_FEEDBACK_CLASSIFIER: max_key,
                                                    constants.GOT_FEEDBACK_CLASSIFIER_INT: got_fdbk_classifier_int,
                                                    f"trip_got_class.{trip_nbr}": max_key,
                                                    constants.TIME_STAMP: datetime.now()
                                                }})

    return constants.EMPTY_STRING
