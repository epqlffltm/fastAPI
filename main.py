#main.py
#2026-04-10
#main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static",StaticFiles(directory = "static"), name = "static")

@app.get("/api/hello")
def hello():
    return {"message":"hello!"}

@app.get("/")
def root():
    return{"message":"hello! fastAPI!"}
