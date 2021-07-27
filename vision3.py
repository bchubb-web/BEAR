import face_recognition
import cv2
import numpy as np
import os
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Bear"]
collection = db["Bear_Friends"]

encodings = {}

for document in collection.find():
    encodings[document["name"]] = document["encoding"]

print(encodings)