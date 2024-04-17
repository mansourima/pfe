from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd


client = MongoClient(
    "mongodb+srv://zkhelouia02:20rachid0131@cluster0.jxl3vd3.mongodb.net/?retryWrites=true&w=majority")
db = client.ridesharing_2

"""key_collection = db.keyCollection
cle = {"key":"6n8wKSEu2bau8FQREOQehzSKgpQcl"}
ki = key_collection.insert_one(cle)"""
#"mongodb+srv://smia:Passwrd2023@cluster1.jo2bgen.mongodb.net/?retryWrites=true&w=majority")

"""source_db = client['ridesharing_2']
source_collection = source_db['zonenlocations']

# Sélectionner la base de données cible et la collection cible
target_db = client['ridesharing_final']
target_collection = target_db['zonenlocations']

# Copier les documents de la collection source vers la collection cible
for document in source_collection.find():
    target_collection.insert_one(document)"""


"""df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ridesharing/zohra_ridersndrivers.csv')
json_data = df.to_dict('records')
db.ridersndrivers.insert_many(json_data)"""

"""df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ridesharing/Give_Fdbck_Train_636.csv')
json_data = df.to_dict('records')
db.Give_Fdbck_Train.insert_many(json_data)

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ridesharing/feedbackCollection_1614.csv')
json_data = df.to_dict('records')
db.feedbackCollection.insert_many(json_data)

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ridesharing/tripCollection_186.csv')
json_data = df.to_dict('records')
db.tripCollection.insert_many(json_data)

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ridesharing/ridersndrivers_170927.csv')
json_data = df.to_dict('records')
db.ridersndrivers.insert_many(json_data)"""

"""give_train = db.Give_Fdbck_Train
cursor = give_train.find()
df = pd.DataFrame(list(cursor))
df.to_csv('Give_Fdbck_Train_float.csv', index=False)

got_train = db.Got_Fdbck_Train
cursor = got_train.find()
df = pd.DataFrame(list(cursor))
df.to_csv('Got_Fdbck_Train_float.csv', index=False)

rider = db.ridersndrivers
cursor = rider.find()
df = pd.DataFrame(list(cursor))
df.to_csv('ridersndrivers_new_float.csv', index=False)

feedback = db.feedbackCollection
cursor = feedback.find()
df = pd.DataFrame(list(cursor))
df.to_csv('feedbackCollection_float.csv', index=False)

trip = db.tripCollection
cursor = trip.find()
df = pd.DataFrame(list(cursor))
df.to_csv('tripCollection_float.csv', index=False)"""


#ridersCollection = db.Give_Fdbck_Train
#count = ridersCollection.count_documents({})
#db.Got_v1.insert_many(db.Test_v3.find())
#print('Found ', count, 'records')
#db.zonenlocations.updateMany({},{"$addFields": {"coordinates": " "}})
#db.zonenlocations.update_many({},{"$set": {"coordinates": 55}})"""
"""resultCollectionFile = db.Got
cursor = resultCollectionFile.find()
df = pd.DataFrame(list(cursor))
df.to_csv('Got_eq.csv', index=False)
db.Got_All.update(
   { $rename: { "oldColumnName": "newColumnName" } },
   { multi: true }
)"""