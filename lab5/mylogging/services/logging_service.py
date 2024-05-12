import hazelcast
import socket
import consul
import time

consul_client = consul.Consul(host='127.0.0.1', port=8500)  # Connect to Consul agent
hz_clusster_name = consul_client.kv.get('hazelcast_cluster_name')[1]['Value'].decode('utf-8').split()
hz_map_name = consul_client.kv.get('hazelcast_map_name')[1]['Value'].decode('utf-8')
#time.sleep(1)
print(hz_clusster_name[0], hz_map_name)

hazelcast_client = hazelcast.HazelcastClient(cluster_name="hello-world") 

hazecast_map = hazelcast_client.get_map(hz_map_name).blocking()
logging_service_ports = [8001, 8002, 8003]
service_port = logging_service_ports[0]

def register_service_with_consul():
    print("Registering service with Consul...")
    service_name = "logging"
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

def saveMessage(msg_uuid, text):
    hazecast_map.set(msg_uuid, text)

    print(f"Message {text} saved with id {msg_uuid}")

def getMessagess():
    values = list(hazecast_map.values())

    if values:
        return "".join(values)
    else:
        return ""
