from dbconnection import db
import constants
locations = db.zone_latlon
cursor2 = locations.find({})
results2 = list(cursor2)
startflag = 0
complete = 0
latitude = []
longitude = []

zonenlocations = db.zonenlocations

for i in range(0, 263):

        latlongArray = []
        latStr = constants.EMPTY_STRING
        longStr = constants.EMPTY_STRING
        results3 = []
        location_id = constants.EMPTY_STRING
        borough = constants.EMPTY_STRING
        zone_name = constants.EMPTY_STRING
        location_id = results2[0][constants.FEATURES][i][constants.PROPERTIES]["location_id"]
        zone_name = results2[0][constants.FEATURES][i][constants.PROPERTIES]["zone"]
        borough = results2[0][constants.FEATURES][i][constants.PROPERTIES]["borough"]
        results3 = results2[0][constants.FEATURES][i]["geometry"]['coordinates']
        results3Str = str(results3)
        results3Str = results3Str.replace('[[[', '')
        results3Str = results3Str.replace(']]]', '')
        for x in results3Str:
               if startflag == 0:
                   latStr = latStr + x
                   latStr = latStr.replace("[", "")
                   if x == "," or x == "]":
                       startflag = 1
                       latitude = latStr.replace(",", "")
                       latStr = ""
               if startflag == 1:
                    longStr = longStr + x
                    if x == "[":
                       longStr = longStr.replace("]", "")
                       startflag = 0
                       longitude = longStr.replace(", [", "")
                       longStr = ""
                       complete = 1
               if complete == 1:
                   actual_location = latitude + longitude
                   latlongArray.append(actual_location)
                   complete = 0

        latlonglen = len(latlongArray)
        record = {constants.ZONE_ID: int(location_id),
                  constants.ZONE_NAME: zone_name,
                  constants.BOROUGH: borough,
                  constants.LOCATION_COUNT: latlonglen,
                  constants.COORDINATES: latlongArray
                  }
        location_ids = zonenlocations.insert_one(record)
