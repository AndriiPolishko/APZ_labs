from fastapi import FastAPI
from pydantic import BaseModel
from mylogging.services.logging_service import *

class MessageRequest(BaseModel):
    msg_uuid: str
    text: str

app = FastAPI()
logging_service_ports = [8001, 8002, 8003]
service_port = logging_service_ports[0]

@app.on_event("startup")
def startup_event():
    register_service_with_consul()

@app.get("/")
def read_root():
    return {"message": "Hello World from logging!"}

@app.post("/save-msg")
def saveMsg(request : MessageRequest):
    print("TEMP engtered save msg contaroller")
    msg_uuid, text = request.msg_uuid, request.text

    res = saveMessage(msg_uuid, text, )

    return {"status": "ok"}

@app.get("/get-msg")
def getMsg():
    values = getMessagess()
    if values != "":
        return {"status": "success", "message": values}
    else:
        return {"status": "fail", "message": "Dictionary is empty"}
