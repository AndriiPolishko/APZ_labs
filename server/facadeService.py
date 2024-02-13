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
            response = await client.post("http://localhost:8001/save-msg", json = {
                "msg_uuid": msg_uuid,
                "text": request.text})
            return response.json()
        except httpx.RequestError as e:
            # Handle connection error
            raise HTTPException(status_code=400, detail=f"Request to the other server failed: {str(e)}")

@app.get("/get-msg")
async def read_item(msg_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://localhost:8001/get-msg", params={"msg_id": msg_id})
            
            print(response.json().get("message"))
            
            return response.json()
        except httpx.RequestError as e:
            # Handle connection error
            raise HTTPException(status_code=400, detail=f"Request to the other server failed: {str(e)}")

uvicorn.run(app, host="127.0.0.1", port=8003)
# uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)