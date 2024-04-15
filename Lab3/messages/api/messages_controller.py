import uvicorn
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root_get():
    return {"message": "Hello World from messages!"}

