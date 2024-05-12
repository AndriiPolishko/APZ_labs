from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import socket
import consul

app = FastAPI()

# Connect to Consul agent
consul_client = consul.Consul(host='127.0.0.1', port=8500)  


# Kafka configuration
messages = []
kafka_topic_name = consul_client.kv.get('kafka_topic_name')[1]['Value'].decode('utf-8')
kafka_bootstrap_server = consul_client.kv.get('kafka_bootstrap_server')[1]['Value'].decode('utf-8')
messages_service_ports = [8004, 8005]
service_port = messages_service_ports[1] # int(sys.argv[1])

@app.get("/")
def root_get():
    return {"message": "Hello World from messages!"}

async def consume():
    consumer = AIOKafkaConsumer(
        kafka_topic_name,
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
    

def register_service_with_consul():
    print("Registering service with Consul...")
    service_name = "messages"
    service_host = socket.gethostname()

    try:
        response = consul_client.agent.service.register(
            name=service_name,
            service_id=f"{service_name}-{service_port}",
            address=service_host,
            port=service_port
        )
        print("Service registered:", response)
    except Exception as e:
        print("Failed to register service:", e)
