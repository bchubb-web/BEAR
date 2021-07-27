import requests
import cv2
import os
cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
#path to face data
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
#start video capture

def getStatus():
    status = requests.get('http://192.168.1.129:3000/data')
    return str(status)

def send_face(x,y,w,h):
    url = "http://localhost:3000/face/"
    #node post request location
    payload='x={0}&y={1}&w={2}&h={3}'.format(x,y,w,h)
    #input the co ordinated into form data
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.request("POST", url, headers=headers, data=payload)
    #POST REQUEST

def findBiggest(list):#finds the biggest face in the frame
    biggest = [0,0,0,0]
    #INIT blank x,y,w,h co ords
    for i in range(0,len(list)):
        if list[i][2]>biggest[2]:
            #if bigger than the previous biggest
            biggest = list[i]
            #update biggest with new
    return biggest

while True:
    ret,frames = video_capture.read()
    #get data from video feed
    grey = cv2.cvtColor(frames,cv2.COLOR_BGR2GRAY)
    #set to greyscale
    faces = faceCascade.detectMultiScale(
        grey,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(15,15),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    #setting required for face recognotion

    biggest=[]
    #init empty array
    for (x,y,w,h) in faces:
        biggest.append([x,y,w,h])
        #add each set of co ords to the array
    if len(faces) > 0:
        #if there is a recognised face
        face = findBiggest(biggest)
        #get the biggest face
        x,y,w,h = face[0],face[1],face[2],face[3] 
        #separate each of the co ords from the list
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,255,0),2)
        #generate a rectangle around the face
        centerX,centerY =   x+round(w/2),y+round(h/2) 
        #find center of the face area
        cv2.circle(frames, (centerX,centerY), 1, (0,255,0), 2)
        #draw dot on the center
        send_face(x,y,w,h)
        #send co ords to the NODEJS server

    cv2.line(frames,(320,0),(320,480),(0,0,255),1)
    #draw a vertical line splitting the viewport into two halves

    #cv2.putText(frames,getStatus(),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)

    cv2.imshow('Video', frames)
    #return updated frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #if q is pressed
        break
video_capture.release()
#end video feed
cv2.destroyAllWindows()
#close windows