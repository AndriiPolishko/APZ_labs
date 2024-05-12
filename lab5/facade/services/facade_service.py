import httpx
import random
from kafka import KafkaProducer
import json
import socket
import consul

# Kafka stuff
producer = KafkaProducer(bootstrap_servers='localhost:9092')
partitions = [0, 1]
# Consul stuff
service_port = 8000
consul_client = consul.Consul(host='127.0.0.1', port=8500)  

def register_service_with_consul():
    print("Registering service with Consul...")
    service_name = "facade"
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

def getServiceAddressUsingConsul(service_name):
    _, services = consul_client.catalog.service(service_name)
    service_address_ports = []
    
    for service in services:
        full_address = f'{service["Address"]}:{service["ServicePort"]}'
        service_address_ports.append(full_address)
            
    return service_address_ports

async def sendMessageToLoggingService(msg_uuid, text):
    async with httpx.AsyncClient() as client:
        try:
            # Get random address of the logging service from Consul
            address = random.choice(getServiceAddressUsingConsul('logging'))

            print(f'Making a request to the logging service to address {address}')

            # Make a request to the one of logging services
            response = await client.post(f'http://{address}/save-msg', json = {
                "msg_uuid": msg_uuid,
                "text": text})

            print(f'Seccess on request to the logging service. Response: {response.json()}')
            
            jsoned_data = json.dumps({'msg_uuid': msg_uuid, 'text': text}).encode('utf-8')
            
            for partition in partitions:
                producer.send('apz-messages', jsoned_data, partition=partition)

            return {"status": response.json().get("status")}

        except Exception as error:
            print(f"Error occured while sending request to logging service: {error}")

            return {"status": "error", "error": str(error)}

async def getItemsFromLoggerService():
    async with httpx.AsyncClient() as client:
        try:
            # Get random address of the logging service from Consul
            logging_address = random.choice(getServiceAddressUsingConsul('logging'))
            
            print(f'Making a request to the logging service to address {logging_address}')

            loggingServiceResponse = await client.get(f'http://{logging_address}/get-msg')
            
            print(f'Seccess on request to the logging service. Response: {loggingServiceResponse.json()}')

            messages_address = random.choice(getServiceAddressUsingConsul('messages'))

            messagesServiceResponse = await client.get(f"http://{messages_address}")

            result = loggingServiceResponse.json().get("message") + " " + messagesServiceResponse.json().get("message")

            return {"status": "ok", "message": result}
        except Exception as error:
            print(f"Error occured: {error}")

            return {"status": "error", "message": str(error)}
