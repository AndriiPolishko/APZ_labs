import uvicorn
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root_get():
    return {"Hello": "World"}
   

uvicorn.run(app, host="127.0.0.1", port=8004)
