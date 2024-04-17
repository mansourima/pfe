import constants
import functions
from datetime import datetime
from dbconnection import db

def UTTMatching(data):
        start_clock = datetime.now()
        riders = data[0]
        tripUTT = int(data[1])
        ridersMatching = int(data[2])
        ridersMatched = int(data[3])
        foundRiders = data[4]
        tripSeatCapacity = int(data[5])
        seatCount = int(data[6])
        userSourceZone = data[7]
        source = data[8]
        destination = data[9]
        userIDQueue = data[10]
        locationlist = data[11]
        user_wait_start_time = data[12]
        userNoQueue = data[13]
        if foundRiders != [] or foundRiders != None:
            if foundRiders == None:
                return None
            else:
                for i in range(0, len(foundRiders)):
                    """end_clock = start_clock = datetime.now()
                    clock_diff_secs, clock_diff_mins = functions.time_diff(start_clock, end_clock)"""
                    
                    if i > 60:
                        print("i passed the rider count",i)
                        break
                        return None
                    else:
                        ridersMatching += 1
                        
                        # print("-------------------------------------------------------------------------")
                        if seatCount <= tripSeatCapacity - 2:
                            newRiderMongoId = foundRiders[i][constants.MONGO_ID]
                            newRiderUserId = foundRiders[i][constants.USER_ID]
                            newRiderUTT = foundRiders[i][constants.UTT]
                            newRiderZone = foundRiders[i][constants.CURRENT_ZONE]

                            if newRiderUTT < tripUTT:
                                tripUTT = newRiderUTT
                               
                            random_new_user_source = ""
                            random_new_user_destination = ""

                            #generer une localisation source pour le rider

                            while random_new_user_source == "":
                                if newRiderZone == userSourceZone:
                                    random_new_user_source = functions.generate_location(newRiderZone)
                                else:
                                    random_new_user_source = functions.generate_random_location()

                            #generer une destination (zone et localisation) pour le rider

                            while random_new_user_destination == "":
                                random_new_user_destination, lastZone = functions.generate_random_location_with_Zone()

                            #calculer le temp entre les source et les destination de rider diffuseur et nw rider
                            source_geocode_source, destination_geocode_source, new_user_distance_source, new_user_time_source = functions.google_Maps_time_distance(
                                source, random_new_user_source)
                            source_geocode_dest, destination_geocode_dest, new_user_distance_dest, new_user_time_dest = functions.google_Maps_time_distance(
                                destination, random_new_user_destination)

                            if new_user_time_source <= tripUTT:
                                if new_user_time_dest <= tripUTT:
                                    user_wait_end_time = datetime.now()
                                    user_wait_time_secs, user_wait_time_mins = functions.time_diff(user_wait_start_time, user_wait_end_time)
                                    #user_wait_start_time = datetime.now()
                                    userIDQueue.append(newRiderMongoId)
                                    userNoQueue.append(newRiderUserId)
                                    seatCount += 1
                                    
                                    print("----------L'utilisateur satisfait les conditions de caractéristiques et de couche UTT---------")
                                    ridersMatched += 1
                                    
                                    rider = {constants.ROLE: constants.RIDER,
                                              constants.USER_ID: foundRiders[i][constants.USER_ID],
                                              constants.ALSO_DRIVER: foundRiders[i][constants.ALSO_DRIVER],
                                              constants.MONGO_ID: foundRiders[i][constants.MONGO_ID],
                                              constants.CHATTY_SCORE: foundRiders[i][constants.CHATTY_SCORE],
                                              constants.SAFETY_SCORE: foundRiders[i][constants.SAFETY_SCORE],
                                              constants.PUNCTUALITY_SCORE: foundRiders[i][constants.PUNCTUALITY_SCORE],
                                              constants.FRIENDLINESS_SCORE: foundRiders[i][constants.FRIENDLINESS_SCORE],
                                              constants.COMFORTIBILITY_SCORE: foundRiders[i][constants.COMFORTIBILITY_SCORE],
                                              constants.UTT: foundRiders[i][constants.UTT],
                                              constants.SOURCE: random_new_user_source,
                                              constants.DESTINATION: random_new_user_destination,
                                              constants.SOURCE_ADDRESS: destination_geocode_source,
                                              constants.DEST_ADDRESS: destination_geocode_dest,
                                              constants.USER_WAIT_TIME_MINS: user_wait_time_mins,
                                              constants.USER_WAIT_TIME_SECS: user_wait_time_secs,
                                              constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}
                                    print("userId de passager accepté: ", foundRiders[i][constants.USER_ID])
                                    #print("Caractéristiques de passager accepté: ", foundRiders[i][constants.CHAR_DICT])

                                    if(tripSeatCapacity-seatCount <= 1):
                                        
                                        print("Le véhicule a atteint sa capacité de places assises, pool terminé.")

                                    riders = riders, rider

                                    userCollection = db.ridersndrivers
                                    userCollection.find_one_and_update({constants.MONGO_ID: newRiderMongoId},
                                                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})
                                    userCollection.find_one_and_update({constants.MONGO_ID: newRiderMongoId},
                                                                       {"$set": {constants.BROADCASTING: constants.NO}})
                                    locationlist.append(random_new_user_source)
                                    locationlist.append(random_new_user_destination)
                                    user_wait_start_time = datetime.now()
                                    datareturn = [riders, tripUTT, userIDQueue, locationlist, ridersMatching, ridersMatched, lastZone, seatCount, user_wait_start_time, userNoQueue]
                                    return datareturn
                        else:
                            return None
                else:
                    return None
        else:
            return None