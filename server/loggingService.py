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

@app.get("/get-msg")
def msg_get(msg_id: str):
    if msg_id in global_dict:
        return {"message": global_dict[msg_id]}
    else:
        return {"message": "Not found"}
uvicorn.run(app, port=8001)