import cv2
import numpy as np
import face_recognition
import json, os
import pymongo, config
from pymongo.server_api import ServerApi
from db import save_face_encodings, get_face_encodings_from_file
from PIL import Image

client = pymongo.MongoClient(config.MDB_URL, server_api=ServerApi('1'))
db = client[config.MDB_DB]
collection = db["faces"]

IMG_FOLDER = 'static/movie_star/'
known_face_list = []

# print(known_face_list)
for filename in os.listdir(IMG_FOLDER):
    print(filename)
    img = cv2.imread(IMG_FOLDER + filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = {}
    data['name'] = filename.split(".")[0]
    data['filename'] = filename
    data['embeddings'] = face_recognition.face_encodings(img)[0].tolist()
    known_face_list.append(data)

collection.insert_many(known_face_list)
