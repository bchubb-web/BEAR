from face_recognition.api import face_distance, face_encodings
import pymongo
import face_recognition
import cv2
import numpy as np

face_locations = []
face_encodings = []
face_names = []
everyOtherFrame = True

face_found = False
stream = cv2.VideoCapture(0)

while True:
    ret, frame = stream.read()

    resized_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)

    bgr_resized_frame = resized_frame[:, :, ::-1]

    if everyOtherFrame:

        face_locations = face_recognition.face_locations(bgr_resized_frame)
        face_encodings = face_recognition.face_encodings(bgr_resized_frame,face_locations)
        face_names = []
        
    everyOtherFrame = not everyOtherFrame

    for(top, right, bottom, left) in face_locations:

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Friend?..", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if not face_found:
            print(face_encodings[0].tolist())
            face_found = True
    cv2.imshow("init new face", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
stream.release()
cv2.destroyAllWindows()