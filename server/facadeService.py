import uvicorn
import httpx
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

class PrivitiveRequest(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def root_get():
    return {"Hello": "World"}

@app.post("/save-msg")
async def root_post(request: PrivitiveRequest):
    msg_uuid = str(uuid.uuid4())
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8002/save-msg", json = {
                "msg_uuid": msg_uuid,
                "text": request.text})
            return {"status": response.json().get("status")}
        except httpx.RequestError as e:
            # Handle connection error
            raise HTTPException(status_code=400, detail=f"Request to the other server failed: {str(e)}")

@app.get("/get-msg")
async def read_item():
    async with httpx.AsyncClient() as client:
        try:
            loggingServiceResponse = await client.get(f"http://localhost:8002/get-msg")
            messagesServiceResponse = await client.get(f"http://localhost:8003/dummy")
            
            result =loggingServiceResponse.json().get("message") + " " + messagesServiceResponse.json().get("greating")
            
            return {"status": "ok", "result": result}
        except httpx.RequestError as e:
            # Handle connection error
            raise HTTPException(status_code=400, detail=f"Request to the other server failed: {str(e)}")

uvicorn.run(app, host="127.0.0.1", port=8001)
# uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)