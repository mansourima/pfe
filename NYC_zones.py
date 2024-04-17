from dbconnection import db
import json

zone_latlong = db.zone_latlon
with open('NYC_zones.geojson') as zone:
    file_data = json.load(zone)
db.zone_latlon.insert_one(file_data)