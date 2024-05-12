import consul
import hazelcast

consul_client = consul.Consul(host='127.0.0.1', port=8500)  # Connect to Consul agent
hz_clusster_name = consul_client.kv.get('hazelcast_cluster_name')[1]['Value'].decode('utf-8')
hz_map_name = consul_client.kv.get('hazelcast_map_name')[1]['Value'].decode('utf-8')
# hazelcast_client = hazelcast.HazelcastClient(cluster_name=hz_clusster_name) 
# hazecast_map = hazelcast_client.get_map(hz_map_name).blocking()
global_dict = {}
logging_service_ports = [8001, 8002, 8003]
service_port = logging_service_ports[0]

print(hz_map_name)