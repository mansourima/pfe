from dbconnection import db
import constants

trip = db.tripCollection
cursorTrip = []
cursor = trip.find({
            "tripData.pool_completed": "Yes"})
cursorTrip = list(cursor)
total_trips = len(cursorTrip)
print("total numbre of trip completed :",total_trips)

trip = db.tripCollection
cursor = trip.find({})  # Récupère tous les documents de la collection

total_exact_close_match_sum = 0  # Initialiser la somme à zéro
total_different_match_sum = 0

for document in cursor:
    if "tripData" in document and "exact_close_match" in document["tripData"]:
        exact_close_match = document["tripData"]["exact_close_match"]
        total_exact_close_match_sum += exact_close_match

print("Somme totale des exact_close_match:", total_exact_close_match_sum)


trip = db.tripCollection
cursor = trip.find({})

for document in cursor:
    if "tripData" in document and "different_match" in document["tripData"]:
        different_match = document["tripData"]["different_match"]
        total_different_match_sum += different_match

print("Somme totale des different_match:", total_different_match_sum)