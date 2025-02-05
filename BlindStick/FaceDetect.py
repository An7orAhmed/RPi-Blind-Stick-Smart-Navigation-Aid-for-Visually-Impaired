import os
import numpy as np
import face_recognition
import cv2

face = []
encode = []
known_faces = []
names = []
fCount = 0

def loadFace(PATH, filename):
    global fCount
    face.append(face_recognition.load_image_file(os.path.join(PATH, filename)))
    encode.append(face_recognition.face_encodings(face[fCount])[0])
    known_faces.append(encode[fCount])
    names.append(filename.replace(".jpg",""))
    print(filename)
    fCount = fCount + 1
        
def importFaces():
    PATH = "Faces/"
    print(">> loading known faces...")
    for filename in os.listdir(PATH):
        if filename.endswith(".jpg"):
            loadFace(PATH, filename)
    print(">> All {} faces loaded.".format(fCount))

def scan(frame):
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    locations = face_recognition.face_locations(rgbFrame)
    encodings = face_recognition.face_encodings(rgbFrame, locations)
    
    name = "unknown"
    for encoding in encodings:
        matches = face_recognition.compare_faces(known_faces, encoding)
            
        face_distances = face_recognition.face_distance(known_faces, encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = names[best_match_index]
        print("Face detected: " + name)
        
    for (top, right, bottom, left) in locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)
    
    return [frame, name]