import pymongo
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
collection = db["movie"]

f = open('sample_movies.json')
content = json.load(f)
f.close

for data in content:
    model_input = data['plot'] + data['title']
    plot_embeddings = st_model.encode(model_input)
    data['plot_embeddings'] = plot_embeddings.tolist()

    print(data['title'])
    if 'poster' in data:
        img_raw = requests.get(data['poster']).content
        img_file = 'static/poster/'+data['title']+'.jpg'
        with open(img_file, 'wb') as handler:
            handler.write(img_raw)
        image = preprocess(Image.open(img_file)).unsqueeze(0).to(device)
        with torch.no_grad():
            image_features = img_model.encode_image(image)
            # text_features = model.encode_text(text)
            # 对特征进行归一化，请使用归一化后的图文特征用于下游任务
            image_features /= image_features.norm(dim=-1, keepdim=True) 
            # text_features /= text_features.norm(dim=-1, keepdim=True)  
            poster_embeddings = image_features.tolist()[0]
            data['poster_embeddings'] = poster_embeddings

collection.insert_many(content)

