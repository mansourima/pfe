from dbconnection import db
import random
import constants
from datetime import datetime
import functions
# import feedback_sys
import variance
import uttMatching
import fdbck_sys
import pymongo
import warnings

warnings.filterwarnings("ignore")


def mainResults(parameterUTT, forriders):
    driverNo = 0
    ridersMatching = 0
    forRiders = 0
    ridersMatched = 1
    requiredDrivers = 0
    userIDQueue = []
    userNoQueue = []
    driver = {}
    # first_rider = {}
    riders = {}
    locationlist = []
    # data = []
    returnData = []
    # last_zone = 0
    start_time = datetime.now().strftime(constants.TIME_STRING)
    start_time_actual = datetime.now()
    broadcasting_rider_start_time = start_time_actual
    userCollection = db.ridersndrivers
    # userSourceZone, scoreList, zoneStat, parameterUTT
    cursor = functions.cursorRiders(0, 0, constants.JUST_UTT, parameterUTT)
    cursorRandomUser = list(cursor)

    # Finds Only Inactive and Broacasting Rider - A True Broadcasting Rider
    while cursorRandomUser == []:
        cursor = functions.cursorRiders(0, 0, constants.JUST_UTT, parameterUTT)
        cursorRandomUser = list(cursor)

    # print("Broadcasting Rider Found...")
    tripUTT = cursorRandomUser[0][constants.UTT]
    Broadcasting_userId = cursorRandomUser[0][constants.MONGO_ID]
    Broadcasting_userNo = cursorRandomUser[0][constants.USER_ID]
    userIDQueue.append(Broadcasting_userId)
    userNoQueue.append(Broadcasting_userNo)
    userCollection.find_one_and_update({constants.MONGO_ID: Broadcasting_userId},
                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})
    userCollection.find_one_and_update({constants.MONGO_ID: Broadcasting_userId},
                                       {"$set": {constants.BROADCASTING: constants.NO}})
    userSourceZone = cursorRandomUser[0][constants.CURRENT_ZONE]
    userSourceLocation = cursorRandomUser[0][constants.CURRENT_LOCATION]
    tripSeatCapacity = 0
    tripChatty = cursorRandomUser[0][constants.CHATTY_SCORE]
    tripSafety = cursorRandomUser[0][constants.SAFETY_SCORE]
    tripPunctuality = cursorRandomUser[0][constants.PUNCTUALITY_SCORE]
    tripFriendliness = cursorRandomUser[0][constants.FRIENDLINESS_SCORE]
    tripComfortibility = cursorRandomUser[0][constants.COMFORTIBILITY_SCORE]
    charDict = cursorRandomUser[0][constants.CHAR_DICT]
    reg_classifier = cursorRandomUser[0][constants.REG_CLASSIFIER]
    feed_back_status = cursorRandomUser[0][constants.FEEDBACK_GIVEN]

    if feed_back_status == constants.YES:
        # print("L'utilisateur a effectué des trajets auparavant.")
        feedback_given_classifer = cursorRandomUser[0]["giving_feedback_classifier"]
        feedback_got_classifer = cursorRandomUser[0]["got_feedback_classifier"]

    else:
        ""
        # print("C'est le premier trajet pour ce utilisateur")

    source = functions.generate_location(userSourceZone)
    destination = functions.generate_random_location()
    locationlist.append(destination)

    source_geocode, destination_gecode, total_trip_distance, total_time_2_int = functions.google_Maps_time_distance(
        source, destination)

    cursorDrivers = functions.cursorRiders(userSourceZone, 0, constants.FIND_DRIVER, parameterUTT)
    drivers = list(cursorDrivers)
    total_drivers = len(drivers)
    closest_driver_time = 10
    closest_driver_id = ""
    closest_flag = False
    #
    # print("------------------------------------------------------------------------------------------")
    # print("Recherche du covoitureur le plus proche dans la même zone")
    driverMongoId = ""
    for i in range(0, total_drivers):
        # print(drivers[i])

        driver_location = drivers[i][constants.CURRENT_LOCATION]

        source_geocode, destination_gecode, distance, time_2_int = functions.google_Maps_time_distance(source,
                                                                                                       driver_location)

        if time_2_int <= closest_driver_time and closest_flag is False:
            tripSeatCapacity = drivers[i][constants.SEAT_CAPACITY]
            driverMongoId = drivers[i][constants.MONGO_ID]
            driverNo = drivers[i][constants.USER_ID]
            closest_driver_time = time_2_int
            driver = {constants.ROLE: constants.DRIVER,
                      constants.USER_ID: drivers[i][constants.USER_ID],
                      constants.SEAT_CAPACITY: drivers[i][constants.SEAT_CAPACITY],
                      constants.ALSO_DRIVER: drivers[i][constants.ALSO_DRIVER],
                      constants.MONGO_ID: drivers[i][constants.MONGO_ID],
                      constants.CHATTY_SCORE: drivers[i][constants.CHATTY_SCORE],
                      constants.SAFETY_SCORE: drivers[i][constants.SAFETY_SCORE],
                      constants.PUNCTUALITY_SCORE: drivers[i][constants.PUNCTUALITY_SCORE],
                      constants.FRIENDLINESS_SCORE: drivers[i][constants.FRIENDLINESS_SCORE],
                      constants.COMFORTIBILITY_SCORE: drivers[i][constants.COMFORTIBILITY_SCORE],
                      constants.UTT: drivers[i][constants.UTT],
                      constants.CURRENT_ZONE: drivers[i][constants.CURRENT_ZONE],
                      constants.CURRENT_LOCATION: drivers[i][constants.CURRENT_LOCATION],
                      constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)
                      }

            if closest_driver_time == 1:
                trip = {}
                # print("Le covoitureur choisi est :",driver[constants.USER_ID])
                closest_flag = True
                break

    broadcasting_rider_end_time = datetime.now()
    user_wait_start_time = broadcasting_rider_end_time
    broadcasting_time_secs, broadcasting_time_mins = functions.time_diff(broadcasting_rider_start_time,
                                                                         broadcasting_rider_end_time)

    first_rider = {constants.ROLE: constants.RIDER,
                   constants.USER_ID: cursorRandomUser[0][constants.USER_ID],
                   constants.CHAR_DICT: charDict,
                   constants.REG_CLASSIFIER: reg_classifier,
                   # constants.FEEDBACK_CLASSIFIER: feedback_classifier,
                   constants.ALSO_DRIVER: cursorRandomUser[0][constants.ALSO_DRIVER],
                   constants.MONGO_ID: cursorRandomUser[0][constants.MONGO_ID],
                   constants.CHATTY_SCORE: cursorRandomUser[0][constants.CHATTY_SCORE],
                   constants.SAFETY_SCORE: cursorRandomUser[0][constants.SAFETY_SCORE],
                   constants.PUNCTUALITY_SCORE: cursorRandomUser[0][constants.PUNCTUALITY_SCORE],
                   constants.FRIENDLINESS_SCORE: cursorRandomUser[0][constants.FRIENDLINESS_SCORE],
                   constants.COMFORTIBILITY_SCORE: cursorRandomUser[0][constants.COMFORTIBILITY_SCORE],
                   constants.UTT: cursorRandomUser[0][constants.UTT],
                   constants.SOURCE: source,
                   constants.DESTINATION: destination,
                   constants.SOURCE_ADDRESS: source_geocode,
                   constants.DEST_ADDRESS: destination_gecode,
                   constants.USER_WAIT_TIME_SECS: broadcasting_time_secs,
                   constants.USER_WAIT_TIME_MINS: broadcasting_time_mins,
                   constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}

    requiredDrivers = requiredDrivers + 1

    filledSeatCount = 0
    lastZone = random.randrange(2, constants.TOTAL_ZONES)
    seatCount = 1
    # print("Recherche des passagers ...")
    # print("------------------------------------------------------------------------------")
    # print("-----------------Recherche exact dans la meme zone----------------------------")
    userCollection = db.ridersndrivers
    user_wait_start_time = datetime.now()
    # Exact Similar Characteristics
    # print("1- Correspondance exact")
    char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
    cursor_newRiders = functions.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
    foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    print("1")
    if filledSeatCount != 0:
        data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount,
                userSourceZone, source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
        returnData = uttMatching.UTTMatching(data)
    if returnData == None or returnData == []:
        ""
        # print("Aucun passager trouvé.")
    else:
        # print("Passagers trouvés par correspondance exacte des caractéristiques et de l'UTT")
        riders = returnData[0]
        tripUTT = returnData[1]
        userIDQueue = returnData[2]
        locationlist = returnData[3]
        ridersMatching = returnData[4]
        ridersMatched = returnData[5]
        lastZone = returnData[6]
        seatCount = returnData[7]
        user_wait_start_time = returnData[8]
        userNoQueue = returnData[9]
        forRiders += ridersMatching
        # print("Les passagers trouvés :",ridersMatched)

    if feed_back_status == constants.YES:
        # print("")
        # print("---------------------FEEDBACK-GIVEN-CLASSIFIER SEARCH--------------------------------")
        # Feedback-Given-Classifier Search
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.YES
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                             feedback_given_classifer,
                                                                                             constants.SAME_ZONE,
                                                                                             given)
            # print("2- Le meme classificateurs donné")
            filledSeatCount += filledSeatCountFunction
            print("2")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                # print("Aucun passager trouvé")# avec le même classificateur donné")
            else:
                # print("Les passagers trouvés :")# ayant le même classificateur donné")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print("forRiders")
                # print("Les passagers trouvés :",ridersMatched)
        # print("")
        # print("---------------------FEEDBACK-RECEIVED-CLASSIFIER SEARCH--------------------------------")
        # Feedback-Received-Classifier Search
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.NO
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                             feedback_got_classifer,
                                                                                             constants.SAME_ZONE,
                                                                                             given)
            # print("3- Le meme classificateur reçu")
            filledSeatCount += filledSeatCountFunction
            print("3")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""

                # print("Aucun passager trouvé")# avec le même classificateur reçu")
            else:
                # print("Les passagers trouvés :")# ayant le même classificateur reçu")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print(forRiders)
                # print("Les passagers trouvés :",ridersMatched)

    # print("-----------------------------CLOSER SEARCH--------------------------------------")
    # All Broadcasting Riders By Exact Register Classifier In Same Zone
    for no in range(0,4):
        if seatCount <= (tripSeatCapacity - 2):
            # print("4- Le meme classificateurs d'inscreption")
            userCollection = db.ridersndrivers
            cursor_newRiders, filledSeatCountfunction = functions.cursorRidersMachineLearnClassifierEnhanced(
                userSourceZone,
                charDict,
                reg_classifier,
                constants.SAME_ZONE)

            filledSeatCount += filledSeatCountfunction
            print("4")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                # print("Aucun passager trouvé")
            else:
                # print(" Riders Found In Same Zone with Exact Registration Classifier....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print("Les passagers trouvés :",ridersMatched)

        # All Broadcasting Riders With Register Classifier with Max Score 5 In Same Zone
        if seatCount <= (tripSeatCapacity - 2):
            # print("------------------------------------------------------------------------------")
            # print("-----------------Recherche plus proche dans la meme zone----------------------")
            userCollection = db.ridersndrivers
            max_score = 5
            cursor_newRiders, filledSeatCountFunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone,
                                                                                                   charDict,
                                                                                                   reg_classifier,
                                                                                                   max_score,
                                                                                                   constants.SAME_ZONE)
            # print("5- Le classificateurs d'inscreption appartient [4,5]")
            filledSeatCount += filledSeatCountFunction
            print("5")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                # print("Aucun passager trouvé")
            else:
                # print("Riders Found in Same Zone with Registration Classifier Score 5....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print("Les passagers trouvés :",ridersMatched)

        # All Broadcasting Driver With Register Classifier with Max Score 4 In Same Zone
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 4
            cursor_newRiders, filledSeatCountFunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone,
                                                                                                   charDict,
                                                                                                   reg_classifier,
                                                                                                   max_score,
                                                                                                   constants.SAME_ZONE)
            # print("6- Le classificateur d'inscreption appartient [3,4]")
            filledSeatCount += filledSeatCountFunction
            print("6")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                # print("Aucun passager trouvé")
            else:
                # print("Riders Found in Same Zone with Registration Classifier Score 4....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print("Les passagers trouvés :",ridersMatched)

    # All Broadcasting Driver With Register Classifier with Max Score 3 In Same Zone
    """if seatCount <= (tripSeatCapacity - 2):
        userCollection = db.ridersndrivers
        max_score = 3
        cursor_newRiders, filledSeatCountFunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone, charDict,
                                                                                               reg_classifier,
                                                                                               max_score,
                                                                                               constants.SAME_ZONE)
        print("7- Le classificateur d'inscreption appartient ]2,3]")
        filledSeatCount += filledSeatCountFunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            # error here
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
            # print("Riders Found In Same Zone with Registration Classifier Score 3....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching
            print("Les passagers trouvés :",ridersMatched)"""

    if seatCount <= (tripSeatCapacity - 2):
        userCollection = db.ridersndrivers
        # print("7- Tous les passagers diffuseurs")
        cursor_newRiders = functions.cursorRiders(userSourceZone, 0, constants.ALL_BROADCASTING, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        print("7")
        if returnData == None or returnData == []:
            ""
            # print("Aucun passager trouvé")
        else:
            # print("Riders found are from Same Zone All Broadcasting....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching
            # print("Les passagers trouvés :",ridersMatched)

    exact_close_match = seatCount

    if seatCount <= (tripSeatCapacity - 2):
        # print("------------------------------------------------------------------------------")
        # print("-----------------Recherche alternative dans une autre zone--------------------")
        # print("8- Correspondance exact")
        cursor_newRiders = functions.cursorRiders(userSourceZone, char, constants.OTHER_ZONE, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount,
                    userSourceZone, source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        print("8")
        if returnData == None or returnData == []:
            ""
            # print("Aucun passager trouvé")# par correspondance exacte.")
        else:
            # print("Passagers trouvés par correspondance exacte des caractéristiques et de l'UTT")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching
            # print(forRiders)
            # print("Les passagers trouvés :",ridersMatched)

    # Feedback-Given-Classifier Search Other Zones
    if feed_back_status == constants.YES:
        if seatCount <= (tripSeatCapacity - 2):
            # print("9- Le meme classificateurs donné")
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.YES
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                             feedback_given_classifer,
                                                                                             constants.OTHER_ZONE,
                                                                                             given)
            filledSeatCount += filledSeatCountFunction
            print("9")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                # print("Aucun passager trouvé")
            else:
                # print("Riders are Found Having Same Feedback-Given-Classifier Other Zones....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print("Les passagers trouvés :",ridersMatched)

        # Feedback-Received-Classifier Search All zones
        if seatCount <= (tripSeatCapacity - 2):
            # print("10- Le meme classificateur reçu")
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.NO
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                             feedback_got_classifer,
                                                                                             constants.OTHER_ZONE,
                                                                                             given)
            filledSeatCount += filledSeatCountFunction
            print("10")
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                # print("Aucun passager trouvé")
                # print("No Riders Found with Same Feedback-Received-Classifier in Other Zones")
            else:
                # print("Riders are Found Having Same Feedback-Received-Classifier in Other Zones....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
                # print("Les passagers trouvés :",ridersMatched)

    # All Broadcasting Riders By Classifier In Other Zone
    if seatCount <= (tripSeatCapacity - 2):
        # print("11- Le meme classificateurs d'inscreption")

        userCollection = db.ridersndrivers
        cursor_newRiders, filledSeatCountfunction = functions.cursorRidersMachineLearnClassifierEnhanced(
            userSourceZone,
            charDict,
            reg_classifier,
            constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        print("11")
        if returnData == None or returnData == []:
            ""
            # print("Aucun passager trouvé")
        else:
            # print("Riders Found are from Other Zone with Exact Classifier....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    if seatCount <= (tripSeatCapacity - 2):
        userCollection = db.ridersndrivers
        # print("14- Tous les passagers diffuseurs")
        cursor_newRiders = functions.cursorRiders(userSourceZone, 0, constants.ABOZ, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        print("14")
        if returnData == None or returnData == []:
            ""
            # print("Aucun passager trouvé")
        else:
            # print("Riders found are from Same Zone All Broadcasting....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching
            # print("Les passagers trouvés :",ridersMatched)

    # print("Number of Matched by Exact or Closer Characteristics Matching", exact_close_match)

    # Same Zone All Broadcasting
    """if seatCount <= (tripSeatCapacity-2):
        #print("---------------------ALTERNATIVE SEARCH--------------------------------")
        userCollection = db.ridersndrivers
        cursor_newRiders = functions.cursorRiders(userSourceZone, 0, constants.ALL_BROADCASTING, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders found are from Same Zone All Broadcasting....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    #All Zones All Broadcasting
    if seatCount <= (tripSeatCapacity-2):
        while foundRiders == [] or filledSeatCount <= tripSeatCapacity:
            userCollection = db.ridersndrivers
            char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
            cursor_newRiders = functions.cursorRiders(userSourceZone, char, constants.OTHER_ZONE, UTT)
            foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders fund are from All Zones All Broadcasting....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching"""

    # print("For rider matched are", forRiders)
    different_char_match = seatCount - exact_close_match
    # print("Differenct Char Broadcasting Count ", different_char_match)

    # print("Lcation List:", locationlist)
    # print("--------Printing the Final Trip-------")
    # print("Seat Left to be filled (Number of Poolers Not Found): ", (tripSeatCapacity - (seatCount + 1)))
    seats_not_filled = tripSeatCapacity - (seatCount + 1)
    # print(trip)
    # print("Active User IDs: ", userIDQueue)

    """userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})"""
    # Update Driver's Active State
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.NO}})
    # driverNewLocationStatus = random.random() #[0.0, 1.0[

    driverNewCurrentLocation = ""
    # if driverNewLocationStatus <= 0.5:
    lastZone = userSourceZone

    driver_new_location = functions.generate_location(lastZone)
    # Update Driver Zone as Last Zone
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_ZONE: lastZone}})
    # Update Driver Location as Last User's Location
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_LOCATION: driver_new_location}})
    functions.updateNoBroadcast(userIDQueue)
    functions.updateNoActiveState(userIDQueue)

    # totalDistanceTime = commons.multiCoordinatesString(locationlist)
    # print(totalDistanceTime)
    # source_geocode_dest, destination_geocode_dest, new_user_distance_dest, new_user_time_dest = commons.google_Maps_time_distance(
    # source, totalDistanceTime)

    poolCompleted = ""
    if seatCount == tripSeatCapacity - 1:
        poolCompleted = constants.YES
    else:
        poolCompleted = constants.NO

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time_actual = datetime.now()

    time_secs, time_mins = functions.time_diff(start_time_actual, end_time_actual)

    # if exact_close_match > seatCount:
    #     different_char_match = seatCount-1
    # else:
    #     different_char_match = seatCount - exact_close_match
    # print("--------------------------------The Final Trip Document----------------------------------")
    """tripData = {
        "pool_completed": poolCompleted,
        "exact_close_match": exact_close_match,
        "different_match": different_char_match,
        constants.SEAT_CAPACITY: tripSeatCapacity,
        "seats_filled": seatCount,
        "seats_not_filled": seats_not_filled,
        constants.UTT: [UTT, tripUTT],
        # total_trip_time": total_trip_time,
        # "total_trip_distance": total_trip_distance,
        "driverId": driverMongoId,
        "user_MongoQ": userIDQueue,
        "userQ": userNoQueue,
        constants.TOTAL_RIDERS_CHECKED: ridersMatching,
        constants.TOTAL_RIDERS_MATCHED: ridersMatched,
        constants.TOTAL_DRIVERS: requiredDrivers,
        constants.TRIP_START_TIME: start_time,
        constants.TRIP_END_TIME: end_time,
        constants.TRIP_DIFF_SECS: time_secs,
        constants.TRIP_DIFF_MINS: time_mins,
        "trip_characteristics": {
            constants.CHATTY_SCORE: tripChatty,
            constants.SAFETY_SCORE: tripSafety,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility
        }
    }

    trip = {
        "tripData": tripData,
        "tripDriver": driver,
        "broadcasting_rider": first_rider,
        "otherRiders": riders
    }"""

    avg_time, wait_time, usercount = functions.avg_wait_time_for_trip(first_rider, riders)  # (trip)
    avg_time = round(avg_time, 2)

    tripCollectionDocs = db.tripCollection
    latest_document = tripCollectionDocs.find_one({}, sort=[("trip_id", pymongo.DESCENDING)])
    if latest_document:
        trip_id = latest_document["trip_id"] + 1
    else:
        trip_id = 1
    # trip_id = tripCollectionDocs.insert_one(trip)
    # tripcursor = tripCollectionDocs.find().sort(constants.MONGO_ID, -1)
    # listTrip = list(tripcursor)
    # trip_mongoId = listTrip[0][constants.MONGO_ID]
    # tripCollectionDocs.delete_one({constants.MONGO_ID: trip_mongoId})

    tripData = {
        # constants.TRIP_ID: trip_id,
        "average_waiting_time": avg_time,
        "pool_completed": poolCompleted,
        "exact_close_match": exact_close_match,
        "different_match": different_char_match,
        constants.SEAT_CAPACITY: tripSeatCapacity,
        "seats_filled": seatCount,
        "seats_not_filled": seats_not_filled,
        constants.UTT: [parameterUTT, tripUTT],
        # total_trip_time": total_trip_time,
        # "total_trip_distance": total_trip_distance,
        "driverId": driverMongoId,
        "user_MongoQ": userIDQueue,
        "userQ": userNoQueue,
        constants.TOTAL_RIDERS_CHECKED: ridersMatching,
        constants.TOTAL_RIDERS_MATCHED: usercount,
        constants.TOTAL_DRIVERS: requiredDrivers,
        constants.TRIP_START_TIME: start_time,
        constants.TRIP_END_TIME: end_time,
        constants.TRIP_DIFF_SECS: time_secs,
        constants.TRIP_DIFF_MINS: time_mins,
        "trip_characteristics": {
            constants.CHATTY_SCORE: tripChatty,
            constants.SAFETY_SCORE: tripSafety,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility
        }
    }

    trip = {
        constants.TRIP_ID: trip_id,
        "tripData": tripData,
        "tripDriver": driver,
        "broadcasting_rider": first_rider,
        "otherRiders": riders
    }
    trip_no = tripCollectionDocs.insert_one(trip)
    # print(trip)

    # userIDQueue.append(driverMongoId)
    # userMongoQ, driverMongoQ, userIdQ, driverId, tripId

    if riders == {} or riders == None or riders == constants.EMPTY_STRING:
        ""
    else:
        fdbck_sys.feedback(userIDQueue, driverMongoId, userNoQueue, driverNo, trip_id)
        variance.variance_given_classifier(userNoQueue)
        variance.variance_got_classifier(userNoQueue)
    # variance.variance_got_classifier(userNoQueue)
    # fdbck_aggr.feedback_aggr(userNoQueue)

    return ridersMatching, usercount, requiredDrivers, exact_close_match, different_char_match, trip_id, wait_time, usercount