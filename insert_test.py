import pymongo
def insert_encoding(encoding:list,friends,register,encodings):
    name = input("enter the students firstname and lastname in the form 'first last':\n")
    yob = input("enter the students birth year in the form '20xx':\n")
    position = ""
    while position not in ["1", "0"]:
        position = input(f"is {name} a 'student' or 'staff:\n").lower()
        if position == "staff":
            position = "1"
        elif position == "student":
            position = "0"
    name_split = name.split() 
    #pid = "0"+name_split[0][0]+name_split[0][-1]+name_split[1][0]+name_split[1][-1]+"0"+yob[-2:]
    pid = f"{position}{name_split[0][0]}{name_split[0][-1]}{name_split[1][0]}{name_split[1][-1]}0{yob[-2:]}"
    friend_obj = {
        "name":name,
        "PID": pid,
        "position":position,
        "YOB": yob
    }
    reg_obj = {
        "name": name,
        "PID": pid,
        "attending": "NULL",
        "last": "NULL"
    }
    encoding_obj = {
        "PID": pid,
        "encoding": encoding
    }
    query = {"PID":pid}
    if not friends.find(query):
        print("student added to database")
        x = friends.insert_one(friend_obj)
        y = register.insert_one(reg_obj)
    z = encodings.insert_one(encoding_obj)
    print("student encodings refined")
    

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")#connect to the mongodb
db = client["Bear"]#select database
friends = db["Bear_Friends"]#select collection (table) from the db
register = db["Bear_register"]# select the register collection from the db
encodings = db["Bear_Encodings"]
settings = db["Bear_Settings"]

insert_encoding([],friends=friends, register=register,encodings=encodings)