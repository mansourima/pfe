import random
import constants
from dbconnection import db
import requests
import json
import time
import sys
from datetime import datetime
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getTimeStamp():
    return datetime.now().strftime(constants.TIME_STRING)



def uni_char():
        char = []
        comfartabilityScore = round(random.uniform(1, 5.1),1)
        friendlinessScore = round(random.uniform(1, 5.1),1)
        punctualityScore = round(random.uniform(1, 5.1),1)
        safetyScore = round(random.uniform(1, 5.1),1)
        chattyScore = round(random.uniform(1, 5.1),1)

        chatty_safety_relation = 0.05
        chatty_punctuality_relation = 0.15
        chatty_friendliness_relation = 0.25
        chatty_comfortibility_relation = 0.05
       
        safety_punctuality_relation = 0.15
        safety_friendliness_relation = 0.05
        safety_comfortibility_relation = 0.25
        
        punctuality_friendliness_relation = 0.1
        punctuality_comfortibility_relation = 0.1

        friendliness_comfortibility_relation = 0.1

        # Calculate the scores
        chattyscore=chattyScore*0.5+safetyScore*chatty_safety_relation+chatty_punctuality_relation*punctualityScore+chatty_friendliness_relation*friendlinessScore+ chatty_comfortibility_relation*comfartabilityScore

        safetyscore=(safetyScore*0.5+chatty_safety_relation*chattyScore)+(safety_punctuality_relation*punctualityScore)+(safety_friendliness_relation*friendlinessScore)+(safety_comfortibility_relation*comfartabilityScore)

        friendlinessscore=friendlinessScore*0.5+chatty_friendliness_relation*chattyScore+safety_friendliness_relation*safetyScore+ punctuality_friendliness_relation*punctualityScore+ friendliness_comfortibility_relation*comfartabilityScore

        punctualityscore=punctualityScore*0.5+chatty_punctuality_relation*chattyScore+safety_punctuality_relation*safetyScore+punctuality_friendliness_relation*friendlinessScore+punctuality_comfortibility_relation*comfartabilityScore

        comfartabilityscore=comfartabilityScore*0.5+chatty_comfortibility_relation*chattyScore+safety_comfortibility_relation*safetyScore+friendliness_comfortibility_relation*friendlinessScore+ punctuality_comfortibility_relation*punctualityScore
       

       # Pour arrondir les scores à deux chiffres après la virgule
        chattyscore = round(chattyscore, 1)
        char.append(chattyscore)
        safetyscore = round(safetyscore, 1)
        char.append(safetyscore)
        punctualityscore = round(punctualityscore, 1)
        char.append(punctualityscore)
        friendlinessscore = round(friendlinessscore, 1)
        char.append(friendlinessscore)
        comfartabilityscore = round(comfartabilityscore, 1)
        char.append(comfartabilityscore)
        return char

def uni_char_fdbck():
        char = []
        comfartabilityScore = round(random.uniform(0, 5.1),1)
        friendlinessScore = round(random.uniform(0, 5.1),1)
        punctualityScore = round(random.uniform(0, 5.1),1)
        safetyScore = round(random.uniform(0, 5.1),1)
        chattyScore = round(random.uniform(0, 5.1),1)

        chatty_safety_relation = 0.05
        chatty_punctuality_relation = 0.15
        chatty_friendliness_relation = 0.25
        chatty_comfortibility_relation = 0.05
       
        safety_punctuality_relation = 0.15
        safety_friendliness_relation = 0.05
        safety_comfortibility_relation = 0.25
        
        punctuality_friendliness_relation = 0.1
        punctuality_comfortibility_relation = 0.1

        friendliness_comfortibility_relation = 0.1

        # Calculate the scores
        chattyscore=chattyScore*0.5+safetyScore*chatty_safety_relation+chatty_punctuality_relation*punctualityScore+chatty_friendliness_relation*friendlinessScore+ chatty_comfortibility_relation*comfartabilityScore

        safetyscore=(safetyScore*0.5+chatty_safety_relation*chattyScore)+(safety_punctuality_relation*punctualityScore)+(safety_friendliness_relation*friendlinessScore)+(safety_comfortibility_relation*comfartabilityScore)

        friendlinessscore=friendlinessScore*0.5+chatty_friendliness_relation*chattyScore+safety_friendliness_relation*safetyScore+ punctuality_friendliness_relation*punctualityScore+ friendliness_comfortibility_relation*comfartabilityScore

        punctualityscore=punctualityScore*0.5+chatty_punctuality_relation*chattyScore+safety_punctuality_relation*safetyScore+punctuality_friendliness_relation*friendlinessScore+punctuality_comfortibility_relation*comfartabilityScore

        comfartabilityscore=comfartabilityScore*0.5+chatty_comfortibility_relation*chattyScore+safety_comfortibility_relation*safetyScore+friendliness_comfortibility_relation*friendlinessScore+ punctuality_comfortibility_relation*punctualityScore
       
       # Pour arrondir les scores à deux chiffres après la virgule
        chattyscore = round(chattyscore, 1)
        char.append(chattyscore)
        safetyscore = round(safetyscore, 1)
        char.append(safetyscore)
        punctualityscore = round(punctualityscore, 1)
        char.append(punctualityscore)
        friendlinessscore = round(friendlinessscore, 1)
        char.append(friendlinessscore)
        comfartabilityscore = round(comfartabilityscore, 1)
        char.append(comfartabilityscore)
        return char






#Geneate a Specified Location
def generate_location(sourceZone):
    locations = db.zonenlocations
    s_cursor = locations.find({constants.ZONE_ID: sourceZone})
    s_list = list(s_cursor)
    while s_list == []:
        sourceZone = random.randrange(1, constants.TOTAL_ZONES)
        s_cursor = locations.find({constants.ZONE_ID: sourceZone})
        s_list = list(s_cursor)
    s_count = s_list[0][constants.LOCATION_COUNT]
    random_source_location_index = random.randrange(2, s_count - 2)
    cursor2 = locations.find({constants.ZONE_ID: sourceZone},
                             {constants.COORDINATES: {"$slice": [random_source_location_index, 1]}})
    s_coordinates = list(cursor2)
    s_coordinates_l = s_coordinates[0][constants.COORDINATES]
    s_coordinates_str = str(s_coordinates_l)
    #print(s_coordinates)
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates

#Generate a Random Location from Random Zone
def generate_random_location():
    sourceZone = random.randrange(1, 263)
    locations = db.zonenlocations
    s_cursor = locations.find({constants.ZONE_ID: sourceZone})
    s_list = list(s_cursor)
    while s_list == []:
        sourceZone = random.randrange(1, constants.TOTAL_ZONES)
        s_cursor = locations.find({constants.ZONE_ID: sourceZone})
        s_list = list(s_cursor)
    s_count = s_list[0][constants.LOCATION_COUNT]
    random_source_location_index = random.randrange(2, s_count - 2)
    cursor2 = locations.find({constants.ZONE_ID: sourceZone},
                             {constants.COORDINATES: {"$slice": [random_source_location_index, 1]}})
    s_coordinates = list(cursor2)
    s_coordinates_l = s_coordinates[0][constants.COORDINATES]
    s_coordinates_str = str(s_coordinates_l)
    # print(s_coordinates_str)
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates

def generate_random_location_with_Zone():
    sourceZone = random.randrange(1, 263)
    locations = db.zonenlocations
    s_cursor = locations.find({constants.ZONE_ID: sourceZone})
    s_list = list(s_cursor)
    while s_list == []:
        sourceZone = random.randrange(1, constants.TOTAL_ZONES)
        s_cursor = locations.find({constants.ZONE_ID: sourceZone})
        s_list = list(s_cursor)
    s_count = s_list[0][constants.LOCATION_COUNT]
    random_source_location_index = random.randrange(2, s_count - 2)
    cursor2 = locations.find({constants.ZONE_ID: sourceZone},
                             {constants.COORDINATES: {"$slice": [random_source_location_index, 1]}})
    s_coordinates = list(cursor2)
    s_coordinates_l = s_coordinates[0][constants.COORDINATES]
    s_coordinates_str = str(s_coordinates_l)
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates, sourceZone


def google_Maps_time_distance(source, destination):
    source_geocode = ""
    destination_geocode = ""
    total_trip_distance = ""
    total_time_2_int = 0
    key_collection=db.keyCollection
    cursorKey=key_collection.find_one()
    #cursorKey = list(cursor)
    #key = cursorKey[0]["key"]
    key=cursorKey["key"]

    if key==None:
      #print("La collection des clé est vide!")
      raise ValueError("La collection des clé est vide!")

    URL = "https://api.distancematrix.ai/maps/api/distancematrix/json?origins=" + source + "&destinations=" + destination + "&key=" + key

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    r = requests.get(URL, headers=headers)
    rdata = json.loads(r.text)
    #print(rdata)
    if "rows" in rdata and len(rdata["rows"]) > 0:
        row = rdata["rows"][0]
        if "elements" in row and len(row["elements"]) > 0:
            element = row["elements"][0]
            status = element.get("status")
            if status == constants.ZERO_RESULTS:
                source_geocode = "Cannot Geocode Source"
                destination_geocode = "Cannot Geocode Destination"
                total_trip_distance = "1000 mi"
                total_time_2_int = 10000 #pour indiquer un voyage de durée inconnue ou un voyage impossible.
            elif status == 'OK':
                destination_geocode = rdata.get("destination_addresses", [""])[0]
                source_geocode = rdata.get("origin_addresses", [""])[0]
                distance_info = element.get("distance", {})
                total_trip_distance = distance_info.get("text", "N/A")
                duration_info = element.get("duration", {})
                total_trip_time = duration_info.get("text", "0 mins")
                total_trip_time_parts = total_trip_time.split(" ")
                total_trip_time_num = int(total_trip_time_parts[0])
                if total_trip_time_parts[1] == "min" or total_trip_time_parts[1] == "mins":
                    total_time_2_int = total_trip_time_num
                else:
                    total_time_2_int = total_trip_time_num * 60
            
                
        return source_geocode, destination_geocode, total_trip_distance, total_time_2_int

    else:
        print(rdata)
        print("clé invalide... renouvelemnt de la clé ...")
        result = key_collection.delete_one({})
        print("Document supprimé :", result.deleted_count == 1)
        return google_Maps_time_distance(source, destination)

def updateNoBroadcast(userQ):
    userCollection = db.ridersndrivers
    for i in range(0, len(userQ)):
        userCollection.find_one_and_update({constants.MONGO_ID: userQ[i]},
                                           {"$set": {constants.BROADCASTING: constants.NO}})

def updateNoActiveState(userQ):
    userCollection = db.ridersndrivers
    for j in range(0, len(userQ)):
        userCollection.find_one_and_update({constants.MONGO_ID: userQ[j]},
                                           {"$set": {constants.ACTIVE_STATE: constants.NO}})



def time_diff(start, end):
    distance = (end - start).total_seconds()
    mins = distance / 60
    str_mins = str(mins)
    str_mins = round(mins, 2)
    return distance, str_mins

def cursorRiders(userSourceZone, scoreList, zoneStat, parameterUTT):
    ridersCollection = db.ridersndrivers
    foundRiders = []

    if scoreList == 0:
        ""
    else:

        tripChatty = scoreList[0]
        tripSafety = scoreList[1]
        tripPunctuality = scoreList[2]
        tripFriendliness = scoreList[3]
        tripComfortibility = scoreList[4]

    #Broadcasting Rider
    if zoneStat == constants.JUST_UTT:
        randomUserID = random.randrange(1, constants.TOTAL_USERS)
        cursor = ridersCollection.find({
            constants.USER_ID: randomUserID,
            constants.ACTIVE_STATE: constants.NO,
            constants.ALSO_DRIVER: constants.NO,
            constants.BROADCASTING: constants.YES,
            constants.UTT: parameterUTT})
    #Driver
    elif zoneStat == constants.FIND_DRIVER:
        cursor = ridersCollection.find({
            constants.ACTIVE_STATE: constants.NO,
            constants.ALSO_DRIVER: constants.YES,
            constants.CURRENT_ZONE: userSourceZone})
    #Same zone exact cara
    elif zoneStat == constants.SZEC:
        cursor = ridersCollection.find(
            {
            constants.CURRENT_ZONE: userSourceZone,
            constants.ACTIVE_STATE: constants.NO,
            constants.BROADCASTING: constants.YES,
            constants.ALSO_DRIVER: constants.NO,
            constants.CHATTY_SCORE: tripChatty,
            constants.SAFETY_SCORE: tripSafety,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility})
    elif zoneStat == constants.ALL_BROADCASTING:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
            })
    elif zoneStat == constants.OTHER_ZONE:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SAFETY_SCORE: tripSafety,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility})
    
    elif zoneStat == constants.ABOZ:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,})

    return cursor

def getChar_Extended():
    charNo = []
    for i in range(1, 6):
        randomNp = random.random()
        if randomNp > 0.7:
            no = random.randrange(1, 6)
        else:
            no = 0
        charNo.append(no)
    return charNo

def avg_wait_time_for_trip(first_rider,riders):#(trip):
    wait_time = first_rider[constants.USER_WAIT_TIME_MINS]
    tripRiderCount = len(riders)
    for i in range(1, tripRiderCount):
        time_m = riders[i][constants.USER_WAIT_TIME_MINS]
        wait_time += time_m
    usercount = tripRiderCount + 1
    avg_time = wait_time / usercount
    return avg_time, wait_time, usercount


def vectorDistanceEnhanced(data):

    vec = DictVectorizer()
    matrix = vec.fit_transform(data)
    similarity_scores = cosine_similarity(matrix)
    rider_index = []
    for i in range(1, len(similarity_scores)):
        if similarity_scores[0, i] > 0.85:
            rider_index.append(i)
    return rider_index



#Classifier [4,5] [3,4]
def cursorRidersMachineLearnEnhanced(userSourceZone, char_dict, reg_classifier, max_score, same_or_other):
    ridersCollection = db.ridersndrivers
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                reg_classifier: {"$lte": max_score, "$gte": max_score - 1}
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                reg_classifier: {"$lte": max_score, "$gte": max_score - 1}
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])
    data = [eval(d) if isinstance(d, str) else d for d in data]

    riders_index = vectorDistanceEnhanced(data)    
   
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index) - 1):
            riders.append(foundRiders[riders_index[i]])
    return riders, filledSeatCount




#Exact Classifier
def cursorRidersMachineLearnClassifierEnhanced(userSourceZone, char_dict, reg_classifier, same_or_other):
    ridersCollection = db.ridersndrivers
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.REG_CLASSIFIER: reg_classifier
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.REG_CLASSIFIER: reg_classifier
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])

     # Convertir les chaînes de caractères en dictionnaires
    data = [eval(d) if isinstance(d, str) else d for d in data]
    riders_index = vectorDistanceEnhanced(data)
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index)-1):
            riders.append(foundRiders[riders_index[i]])

    return riders, filledSeatCount

def update_feedback_status(userIdQ):
    for i in range(0, len(userIdQ)):
        #print(userIdQ[i])
        userCollection = db.ridersndrivers
        userCollection.find_one_and_update({constants.USER_ID: userIdQ[i]},
                                           {"$set": {constants.FEEDBACK_GIVEN: constants.YES}})
    return None


def givenClassifierBasedSearch(userSourceZone, char_dict, classifier_string, same_or_other, given):
    ridersCollection = db.ridersndrivers
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE and given == constants.YES:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GIVEN_FEEDBACK_CLASSIFIER: classifier_string

            })
    elif same_or_other == constants.SAME_ZONE and given == constants.NO:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GOT_FEEDBACK_CLASSIFIER: classifier_string

            })
    elif same_or_other == constants.OTHER_ZONE and given == constants.YES :
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GIVEN_FEEDBACK_CLASSIFIER: classifier_string
            })
    elif same_or_other == constants.OTHER_ZONE and given == constants.NO :
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GOT_FEEDBACK_CLASSIFIER: classifier_string
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])
    riders_index = vectorDistanceEnhanced(data)
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index) - 1):
            riders.append(foundRiders[riders_index[i]])
    return riders, filledSeatCount