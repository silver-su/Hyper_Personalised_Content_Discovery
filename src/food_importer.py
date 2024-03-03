import pymongo, os
from pymongo.server_api import ServerApi
import json, config, requests
import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
import torch 
from PIL import Image

from sentence_transformers import SentenceTransformer
# sentences = ["This is an example sentence", "Each sentence is converted"]

device = "cuda" if torch.cuda.is_available() else "cpu"
img_model, preprocess = load_from_name("ViT-B-16", device=device, download_root='./models')
img_model.eval()

st_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

client = pymongo.MongoClient(config.MDB_URL, server_api=ServerApi('1'))
db = client[config.MDB_DB]
collection = db["food"]

IMG_FOLDER = 'static/food/'
known_face_list = []

for filename in os.listdir(IMG_FOLDER):
    image = preprocess(Image.open(IMG_FOLDER + filename)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = img_model.encode_image(image)
        # text_features = model.encode_text(text)
        # 对特征进行归一化，请使用归一化后的图文特征用于下游任务
        image_features /= image_features.norm(dim=-1, keepdim=True) 
        # text_features /= text_features.norm(dim=-1, keepdim=True)  
        embeddings = image_features.tolist()[0]
        data = {}
        data['embeddings'] = embeddings
        data['title'] = filename.split(".")[0]
        data['filename'] = filename
        known_face_list.append(data)

collection.insert_many(known_face_list)

