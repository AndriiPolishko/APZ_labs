from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from facade.services.facade_service import *

class PrivitiveRequest(BaseModel):
    text: str

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    register_service_with_consul()

@app.get("/")
def root_get():
    return {"message": "Hello World from facade!"}

@app.post("/save-msg")
async def root_post(request: PrivitiveRequest):
    msg_uuid = str(uuid.uuid4())
    text = request.text

    result = await sendMessageToLoggingService(msg_uuid, text)

    return result

@app.get("/get-msgs")
async def get_messages():
    result = await getItemsFromLoggerService()

    return result
