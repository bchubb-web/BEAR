import face_recognition
import pymongo
import os

client = pymongo.MongoClient()
db = client["Bear"]
collection = db["Bear_Friends"]

link = "D:\CODE\BEAR\BEAR\Faces\\" + input("1. Copy .jpg image into /Faces \n2. Paste image name here: ")
print(link)
if os.path.isfile(link):
    image = face_recognition.load_image_file(link)
    locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image,locations)
    for encoding in encodings:
        encoding = encoding.tolist()
        name = input("Enter your full name: ")
        obj = {
            "name":name,
            "encoding":encoding
        }
        x = collection.insert_one(obj)

print("encoding added to db")