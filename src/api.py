from fastapi import FastAPI, File, UploadFile
from db import save_face_encodings, get_face_encodings_from_file
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import pymongo
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer
import openai
from pydantic import BaseModel
import torch
import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
import config

class BaseSearch(BaseModel):
    query: str

class Search(BaseModel):
    question: str
    type: str
    lang: str
    enable_gpt: bool

class MovieSearch(BaseModel):
    question: str
    
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
# app.mount("/images", StaticFiles(directory="./images"), name="images")

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = load_from_name("ViT-B-16", device=device, download_root="./models")
clip_model.eval()

client = pymongo.MongoClient(config.MDB_URL, server_api=ServerApi('1'))
db = client[config.MDB_DB]

# open ai
openai.api_key = config.API_KEY

@app.get("/", response_class=HTMLResponse)
async def index():
    return open("static/index.html", "r").read()

@app.get("/faq", response_class=HTMLResponse)
async def faq():
    return open("static/faq.html", "r").read()

@app.get("/movie", response_class=HTMLResponse)
async def movie():
    return open("static/movie.html", "r").read()

@app.get("/pokemon", response_class=HTMLResponse)
async def pokemon():
    return open("static/pokemon.html", "r").read()

@app.get("/food", response_class=HTMLResponse)
async def food():
    return open("static/food.html", "r").read()

# Upload endpoint
@app.post("/upload")
async def upload_image(file: UploadFile):
    collection = db["faces"]
    print(file.filename)
    # Save face encodings to database
    face_encodings = get_face_encodings_from_file(file.file)
    # print(face_encodings)
    # save_face_encodings(face_encodings)
    
    result = [embedding.tolist() for embedding in face_encodings]
    for embedding in face_encodings:
        vector_query = embedding.tolist() 
    print(vector_query)
    # Return face encodings
    # print(face_encodings.tolist())
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": "faces",
                "path": "embeddings",
                "queryVector": vector_query,
                "numCandidates": 150, 
                "limit": 10
            }
        },
        {
            "$project": {
                "embeddings": 0,
                "_id": 0,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    ]
    search_result = list(collection.aggregate(pipeline))
    print(search_result)
    return search_result

@app.post("/faq/search")
async def faq_search(search: Search):
    
    collection = db["faq"]
    
    type = search.type
    lang = search.lang
    enable_gpt = search.enable_gpt
    # print(search)
    query_embeddings = model.encode(search.question)
    query_embeddings_list = query_embeddings.tolist()
    # print(query_embeddings_list)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "faq",
                "path": "embeddings",
                "queryVector": query_embeddings_list,
                "numCandidates": 150, 
                "limit": 10
            }
        },
        {
            "$project": {
                "embeddings": 0,
                "_id": 0,
                "score": {
                    "$meta": "searchScore"
                }
            }
        }
    ] 
    search_result = list(collection.aggregate(pipeline))
    answers = []
    for doc in search_result:
        # print(doc)
        # first_answer = first_answer + " " + doc["answer"]
        answers.append(doc["answer"])
        # break
    answer_all = "|".join(answers)
    # print(answer_all)
    # print(first_answer)
    # build chatgpt prompt
    if enable_gpt:
        prompt = build_prompt(search.question, answer_all, type, lang)
        print(prompt)
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=1024,
        #     temperature=0,
        # )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0,
        )

        # print(response)
        # gpt_response = response["choices"][0]["text"].strip()
        gpt_response = response["choices"][0]["message"].content.strip()
        # print(response)
        # gpt_response = "gpt response"
        return {"original_answer": answers[0], "gpt_response": gpt_response}
    else:
        return {"original_answer": answers[0]}

def build_prompt(question: str, answer: str, answer_type: str="summarize", lang: str="tradition chinese"):
    # prompt = f"""
    #         only use the following context to "{answer_type}" in "{lang}","
    #         context: "{answer}"
    #         """.strip()
    # prompt = f"""
    #         只能用以下提供的內容找出答案，並將答案翻譯成 "{lang}"。
    #         問題: "{question}"\n
    #         內容: "{answer}"
    # """.strip()

    # prompt = f"""
    #         If the question cannot be answered, please response me [抱歉，我不知道答案。].
    #         Only use the following context to answer this question "{question}" to "{answer_type}" and answer in language:"{lang}".
            
    #         Context: "{answer}"
    # """.strip()
    prompt = f"""
            If the question cannot be answered, please response me [抱歉，我不知道答案。].
            Only use the following context to answer this question "{question}" to "{answer_type}" and answer in language:"{lang}".
            Context: "{answer}"
    """.strip()
    # prompt = f"""
    #         Only use the following context to answer this question "{question}" in "{lang}".
    #         If cannot be anaswered, please response [抱歉，我不知道答案。]
    #         Context: "{answer}"
    # """.strip()
    return prompt

@app.post("/movie/search")
async def movie_search(search: MovieSearch):
    
    collection = db["movie"]
    
    # type = search.type
    # lang = search.lang
    # enable_gpt = search.enable_gpt
    # print(search)
    query_embeddings = model.encode(search.question)
    query_embeddings_list = query_embeddings.tolist()
    print(query_embeddings)
    print(query_embeddings_list)
    # print(query_embeddings_list)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "movie_idx",
                "path": "plot_embeddings",
                "queryVector": query_embeddings_list,
                "numCandidates": 150, 
                "limit": 10
            }
        },
        {
            "$project": {
                "plot_embeddings": 0,
                "_id": 0,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    ] 
    search_result = list(collection.aggregate(pipeline))
    print(search_result)
    result = []
    for doc in search_result:
        if doc["score"] > 0.05:
            result.append(doc)
    print(search_result)
    return result

@app.post("/pokemon/search")
async def pokemon_search(search: BaseSearch):
    
    collection = db["pokemon"]
    text = clip.tokenize([search.query]).to(device)
    text_features = clip_model.encode_text(text)
    
    text_features /= text_features.norm(dim=-1, keepdim=True)    
    query_embeddings = text_features.tolist()[0]

    # print(query_embeddings_list)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "pokemon",
                "path": "embeddings",
                "queryVector": query_embeddings,
                "numCandidates": 150, 
                "limit": 10
            }
        },
        {
            "$project": {
                "poster_embeddings": 0,
                "_id": 0,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    ] 
    search_result = list(collection.aggregate(pipeline))
    print(search_result)
    return search_result


@app.post("/food/search")
async def pokemon_search(search: BaseSearch):
    
    collection = db["food"]
    text = clip.tokenize([search.query]).to(device)
    text_features = clip_model.encode_text(text)
    
    text_features /= text_features.norm(dim=-1, keepdim=True)    
    query_embeddings = text_features.tolist()[0]

    # print(query_embeddings_list)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "food_idx",
                "path": "embeddings",
                "queryVector": query_embeddings,
                "numCandidates": 150, 
                "limit": 10
            }
        },
        {
            "$project": {
                "embeddings": 0,
                "_id": 0,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    ] 
    search_result = list(collection.aggregate(pipeline))
    print(search_result)
    return search_result