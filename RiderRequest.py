from dbconnection import db
import random
import constants
from datetime import datetime
import functions
import Make_Trip
import pymongo


userId = 30001#random.randrange(30001,60001)
userCollection = db.ridersndrivers
cursorRandomUser = []
cursor = userCollection.find({
             constants.USER_ID: userId})
cursorRandomUser = list(cursor)
UTT = cursorRandomUser[0][constants.UTT]
userSourceZone = cursorRandomUser[0][constants.CURRENT_ZONE]

source = functions.generate_location(userSourceZone)
destination = functions.generate_random_location()

print("------------------------------------------------------------------------------------------")
print("L'utilisateur ayant les informations suivantes a soumis une demande de covoiturage :")
print("userId :",userId)
print("UTT :",UTT)
print("Source :",source)
print("Destination :",destination)

users, trip_id=Make_Trip.mainResults(userId,UTT,source,destination)
print("les passager de ce trajet sont :" ,users)
print("Numero de trajet :",trip_id)