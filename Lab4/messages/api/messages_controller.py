import uvicorn
import json
from typing import Union
from fastapi import FastAPI
import asyncio
from aiokafka import AIOKafkaConsumer

from kafka import KafkaConsumer, TopicPartition

app = FastAPI()

def json_deserializer(serialized):
    if serialized is None:
        return None
    json.loads(serialized)

messages = []
# Kafka configuration
bootstrap_server = 'localhost:9092'  # Adjust if different
topicName = 'apz-messages'

@app.get("/")
def root_get():
    return {"message": "Hello World from messages!"}

async def consume():
    consumer = AIOKafkaConsumer(
        topicName,
        bootstrap_servers=bootstrap_server,
        auto_offset_reset='earliest',
        group_id="my-group"
    )

    await consumer.start()
    
    try:
        # Consume messages
        async for message in consumer:
            messages.append(message.value)
    finally:
        # Cleanup
        await consumer.stop()
    
    # await consumer.stop()


@app.on_event("startup")
async def startup_event():
    task = asyncio.create_task(consume())
    # Wait for consumer to initialize
    await asyncio.sleep(1) 

@app.get("/messages")
async def get_messages():
    return {"messages": messages}
