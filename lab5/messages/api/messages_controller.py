from fastapi import FastAPI
import asyncio
from messages.services.messages_service import *

app = FastAPI()

@app.get("/")
def root_get():
    return {"message": "Hello World from messages!"}

@app.on_event("startup")
async def startup_event():
    register_service_with_consul()
    
    asyncio.create_task(consume())
    # Wait for consumer to initialize
    await asyncio.sleep(1) 

@app.get("/messages")
async def get_messages():
    return {"messages": messages}
