from dbconnection import db
import random
import constants
from datetime import datetime
import functions
#import feedback_sys
import variance
import uttMatching
import fdbck_sys
import pymongo
import warnings
warnings.filterwarnings("ignore")


def mainResults(userId, UTT,source,destination):

    driverNo = 0 #list des driver
    ridersMatching = 0
    forRiders = 0
    ridersMatched = 1
    requiredDrivers = 0 #nombre de driver
    userIDQueue = [] #_id mongodb
    userNoQueue = [] #userId
    driver = {}

    riders = {}
    locationlist = []
    returnData = [] 
    start_time = datetime.now().strftime(constants.TIME_STRING)
    start_time_actual = datetime.now()
    broadcasting_rider_start_time = start_time_actual
    userCollection = db.ridersndrivers


    cursorRandomUser = []

    cursor = userCollection.find({
            constants.USER_ID: userId})
    cursorRandomUser = list(cursor)
    tripUTT = UTT
    Broadcasting_userId = cursorRandomUser[0][constants.MONGO_ID]
    Broadcasting_userNo = cursorRandomUser[0][constants.USER_ID]
    userIDQueue.append(Broadcasting_userId)
    userNoQueue.append(Broadcasting_userNo)
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
    feedback_classifier = constants.NO
    trip_nbr = cursorRandomUser[0]["trip_nbr"]

    locationlist.append(destination)

    source_geocode, destination_gecode, total_trip_distance, total_time_2_int = functions.google_Maps_time_distance(
        source, destination)

    if feed_back_status == constants.YES:
        print("L'utilisateur a les deux classificateurs.")
        feedback_given_classifer = cursorRandomUser[0]["giving_feedback_classifier"]
        feedback_got_classifer = cursorRandomUser[0]["got_feedback_classifier"]

    else:
        print("C'est le premier trajet pour ce utilisateur")

    cursorDrivers = functions.cursorRiders(userSourceZone, 0, constants.FIND_DRIVER, UTT)
    drivers = list(cursorDrivers)
    total_drivers = len(drivers)
    closest_driver_time = 10
    closest_driver_id = ""
    closest_flag = False
    #
    print("------------------------------------------------------------------------------------------")
    print("Recherche du covoitureur le plus proche dans la même zone")
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
                print("Le covoitureur choisi est :",driver[constants.USER_ID])
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
                   constants.FEEDBACK_CLASSIFIER: feedback_classifier,
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
    print("Recherche des passagers ...")
    print("------------------------------------------------------------------------------")
    print("-----------------Recherche exact dans la meme zone----------------------------")
    userCollection = db.ridersndrivers
    user_wait_start_time = datetime.now()

    print("1- Correspondance exact")
    char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
    cursor_newRiders = functions.cursorRiders(userSourceZone, char, constants.SZEC, UTT)
    foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    if filledSeatCount != 0:
        data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone, source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
        returnData = uttMatching.UTTMatching(data)
    if returnData == None or returnData == []:
        print("Aucun passager trouvé.")
    else:
        #print("Passagers trouvés par correspondance exacte des caractéristiques et de l'UTT")
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
        #print("Les passagers trouvés :",ridersMatched)


    if feed_back_status == constants.YES:
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.YES
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                                 feedback_given_classifer,
                                                                                                 constants.SAME_ZONE,
                                                                                                 given)
            print("2- Le meme classificateurs donné")
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                print("Aucun passager trouvé")# avec le même classificateur donné")
            else:
                #print("Les passagers trouvés :")# ayant le même classificateur donné")
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
            max_score = 0
            given = constants.NO
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                           feedback_got_classifer,
                                                                                           constants.SAME_ZONE,
                                                                                           given)
            print("3- Le meme classificateur reçu")
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                print("Aucun passager trouvé")# avec le même classificateur reçu")
            else:
                #print("Les passagers trouvés :")# ayant le même classificateur reçu")
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
        print("4- Le meme classificateurs d'inscreption")
        userCollection = db.ridersndrivers
        cursor_newRiders, filledSeatCountfunction = functions.cursorRidersMachineLearnClassifierEnhanced(userSourceZone,
                                                                                                         charDict,
                                                                                                         reg_classifier,
                                                                                                         constants.SAME_ZONE)
        
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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
        print("------------------------------------------------------------------------------")
        print("-----------------Recherche plus proche dans la meme zone----------------------")
        userCollection = db.ridersndrivers
        max_score = 5
        cursor_newRiders, filledSeatCountFunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone, charDict,
                                                                                               reg_classifier,
                                                                                               max_score,
                                                                                               constants.SAME_ZONE)
        print("5- Le classificateurs d'inscreption appartient [4,5]")
        filledSeatCount += filledSeatCountFunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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
        max_score = 4
        cursor_newRiders, filledSeatCountFunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone, charDict,
                                                                                               reg_classifier,
                                                                                               max_score,
                                                                                               constants.SAME_ZONE)
        print("6- Le classificateur d'inscreption appartient [3,4]")
        filledSeatCount += filledSeatCountFunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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


    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        print("7- Tous les passagers diffuseurs")
        cursor_newRiders = functions.cursorRiders(userSourceZone, 0, constants.ALL_BROADCASTING, UTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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
            #print("Les passagers trouvés :",ridersMatched)


    exact_close_match = seatCount

    if seatCount <= (tripSeatCapacity - 2):
          print("------------------------------------------------------------------------------")
          print("-----------------Recherche alternative dans une autre zone--------------------")
          print("8- Correspondance exact")
          cursor_newRiders = functions.cursorRiders(userSourceZone, char,constants.OTHER_ZONE, UTT)
          foundRiders = list(cursor_newRiders)
          filledSeatCount += len(foundRiders)
          if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone, source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
          if returnData == None or returnData == []:
                print("Aucun passager trouvé")# par correspondance exacte.")
          else:
                #print("Passagers trouvés par correspondance exacte des caractéristiques et de l'UTT")
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

    if feed_back_status == constants.YES:
        if seatCount <= (tripSeatCapacity - 2):
            print("9- Le meme classificateurs donné")
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.YES
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                             feedback_given_classifer,
                                                                                             constants.OTHER_ZONE,
                                                                                             given)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                print("Aucun passager trouvé")
            else:
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
                #print("Les passagers trouvés :",ridersMatched)

        if seatCount <= (tripSeatCapacity - 2):
            print("10- Le meme classificateur reçu")
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.NO
            cursor_newRiders, filledSeatCountFunction = functions.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                             feedback_got_classifer,
                                                                                             constants.OTHER_ZONE,
                                                                                             given)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                print("Aucun passager trouvé")
            else:
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
                
    if seatCount <= (tripSeatCapacity-2):
        print("11- Le meme classificateurs d'inscreption")

        userCollection = db.ridersndrivers
        cursor_newRiders, filledSeatCountfunction = functions.cursorRidersMachineLearnClassifierEnhanced(userSourceZone, charDict, reg_classifier,
                                                                      constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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

    if seatCount <= (tripSeatCapacity-2):
        print("12- Le classificateurs d'inscreption appartient [4,5]")
        userCollection = db.ridersndrivers
        max_score = 5
        cursor_newRiders, filledSeatCountFunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score,
                                                            constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountFunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
            
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
            

    if seatCount <= (tripSeatCapacity-2):
        print("13- Le classificateur d'inscreption appartient [3,4]")
        userCollection = db.ridersndrivers
        max_score = 4
        cursor_newRiders, filledSeatCountfunction = functions.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score, constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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


    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        print("14- Tous les passagers diffuseurs")
        cursor_newRiders = functions.cursorRiders(userSourceZone, 0, constants.ABOZ, UTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            print("Aucun passager trouvé")
        else:
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


    different_char_match = seatCount - exact_close_match

    seats_not_filled = tripSeatCapacity - (seatCount + 1)

    """userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})"""
    # Update Driver's Active State
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.NO}})

    #update la zone de drive
    driverNewCurrentLocation = ""
    lastZone = userSourceZone
    driver_new_location = functions.generate_location(lastZone)
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_ZONE: lastZone}})
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_LOCATION: driver_new_location}})
    functions.updateNoBroadcast(userIDQueue)
    functions.updateNoActiveState(userIDQueue)

    poolCompleted = ""
    if seatCount == tripSeatCapacity - 1:
        poolCompleted = constants.YES
    else:
        poolCompleted = constants.NO

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time_actual = datetime.now()

    time_secs, time_mins = functions.time_diff(start_time_actual, end_time_actual)

    avg_time, wait_time, usercount = functions.avg_wait_time_for_trip(first_rider,riders)#(trip)
    avg_time = round(avg_time, 2)

    tripCollectionDocs = db.tripCollection
    latest_document = tripCollectionDocs.find_one({}, sort=[("trip_id", pymongo.DESCENDING)]) 
    if latest_document:
        trip_id = latest_document["trip_id"]+1
    else:
        trip_id =1

    tripData = {
        "average_waiting_time": avg_time,
        "pool_completed": poolCompleted,
        "exact_close_match": exact_close_match,
        "different_match": different_char_match,
        constants.SEAT_CAPACITY: tripSeatCapacity,
        "seats_filled": seatCount,
        "seats_not_filled": seats_not_filled,
        constants.UTT: [UTT, tripUTT],
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

    if riders == {} or riders == None or riders == constants.EMPTY_STRING:
        ""
    else:
        fdbck_sys.feedback(userIDQueue, driverMongoId, userNoQueue, driverNo, trip_id)
        variance.variance_given_classifier(userNoQueue)
        variance.variance_got_classifier(userNoQueue)


    return userNoQueue, trip_id #ridersMatching, usercount, requiredDrivers, exact_close_match, different_char_match, trip_id, wait_time, usercount
