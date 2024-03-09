import uvicorn
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    msg_uuid: str
    text: str

global_dict = {}

@app.post("/save-msg")
def msg_saver(request : MessageRequest):
    global_dict[request.msg_uuid] = request.text
    print(f"Message {request.text} saved with id {request.msg_uuid}")

    return {"status": "ok"}

@app.get("/get-msg")
def msg_get():
    print(global_dict.values())
    values = list(global_dict.values())
    if values:
        return {"message": " ".join(values)}
    else:
        return {"message": "Dictionary is empty"}
uvicorn.run(app, port=8002)