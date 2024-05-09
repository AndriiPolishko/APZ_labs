import hazelcast

clientOne = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701'],
cluster_name="hello-world") 
    
# Get the distributed map
hazecast_map = clientOne.get_map("my-distributed-map").blocking()

hazecast_map.set("1", "Hello World!")
hazecast_map.set("2", "Hello World!")
hazecast_map.set("3", "Hello World!")
hazecast_map.set("4", "Bye World!")