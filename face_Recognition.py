import cv2
import face_recognition
import os
import numpy as np

# Create an empty list to store face encodings and associated names
face_encodings_and_names = []

# Use os.walk to go through all image files in the directory and its subdirectories
for dirpath, dirnames, filenames in os.walk('faces'):
    for filename in filenames:
        if filename.endswith('.png') or filename.endswith('.jpg'):  # add more conditions if there are other image types
            # Get the name of the person from the name of the subdirectory
            name = os.path.basename(dirpath)
            # Load the image
            image = cv2.imread(os.path.join(dirpath, filename))
            # Detect the locations of faces in the image
            face_locs = face_recognition.face_locations(image)
            # Encode the detected faces and add the encodings to the list with associated name
            for face_loc in face_locs:
                encoding = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]
                face_encodings_and_names.append({"encoding": encoding, "name": name})

# Video Capture 
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if ret == False: break
    frame = cv2.flip(frame, 1)
    
    # Detect the locations of faces in the frame
    face_locs = face_recognition.face_locations(frame)
    # Encode the detected faces
    face_encs = face_recognition.face_encodings(frame, face_locs)
    # Loop over each detected face and its location
    for (top, right, bottom, left), face_enc in zip(face_locs, face_encs):
        # Compare the face with the stored encodings
        matches = [face_recognition.compare_faces([d["encoding"]], face_enc)[0] for d in face_encodings_and_names]
        # name = "Desconocido" ESTE
        
    
        # If there is a match, get the name associated with the encoding
        if True in matches:
            match_index = matches.index(True)
            color = (125, 220, 0)
            name = face_encodings_and_names[match_index]["name"] 
        else:
            name = "Desconocido"
            color = (50, 50, 255)

        # Display the name on the frame
        cv2.rectangle(frame, (left, top), (right, top + 30), color, -1)
        cv2.rectangle(frame, (left, top), (right, top), color, 2)
        cv2.putText(frame, name, (left, top + 20), 2, 0.7, (255, 255, 255), 1) 

    cv2.imshow('Frame: ', frame)
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()