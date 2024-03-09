import hazelcast

def incrementKeyWithOutLocking(map, key):
    map.lock(key)
    try:
        value = map.get(key)
        value += 1
        map.put(key, value)
    finally:
        map.unlock(key)

clientOne = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701'],
cluster_name="hello-world") 
    
# Get the distributed map
myMapFromFirstClient = clientOne.get_map("my-distributed-map").blocking()

key = "1000"

for _ in range(10000):
    incrementKeyWithOutLocking(myMapFromFirstClient, key)
