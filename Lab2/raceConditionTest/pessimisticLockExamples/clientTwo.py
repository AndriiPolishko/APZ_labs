import hazelcast

def incrementKeyWithOutLocking(map, key):
    map.lock(key)
    try:
        value = map.get(key)
        value += 1
        map.put(key, value)
    finally:
        map.unlock(key)

clientTwo = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5702'],
cluster_name="hello-world")

# Get the distributed map
myMapFromSecondClient = clientTwo.get_map("my-distributed-map").blocking()

key = "1000"

for _ in range(10000):
    incrementKeyWithOutLocking(myMapFromSecondClient, key)
