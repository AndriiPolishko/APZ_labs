import uvicorn
import httpx
from typing import Union
from fastapi import FastAPI
import random

async def sendMessageToLoggingService(msg_uuid, text):
    async with httpx.AsyncClient() as client:
        try:
            port = random.randint(8082, 8084)

            print(f'Making a request to the logging service on port {port}')

            # Make a request to the one of logging services
            response = await client.post(f'http://127.0.0.1:{port}/save-msg', json = {
                "msg_uuid": msg_uuid,
                "text": text})

            print(f'Seccess on request to the logging service. Response: {response.json()}')

            return {"status": response.json().get("status")}
        except Exception as error:
            print(f"Error occured while sending request to logging service: {error}")

            return {"status": "error", "error": str(error)}

async def getItemsFromLoggerService():
    async with httpx.AsyncClient() as client:
        try:
            port = random.randint(8082, 8084)

            print(f'Making a request to the logging service on port {port}')

            loggingServiceResponse = await client.get(f'http://localhost:{port}/get-msg')
            
            print(f'Seccess on request to the logging service. Response: {loggingServiceResponse.json()}')

            messagesServiceResponse = await client.get(f"http://localhost:8085")

            result = loggingServiceResponse.json().get("message") + " " + messagesServiceResponse.json().get("message")

            return {"status": "ok", "message": result}
        except Exception as error:
            print(f"Error occured: {error}")

            return {"status": "error", "message": str(error)}
