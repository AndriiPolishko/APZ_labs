import time
import hazelcast

def incrementKeyWithOutLocking(map, key):
    while True:
        current_value = map.get(key)
        new_value = current_value + 1
        
        succeeded = map.replace_if_same(key, current_value, new_value)
        
        if succeeded:
            # If the update succeeded, break out of the loop
            break
        else:
            # If the update failed (meaning the value was changed by another operation), retry
            # In a high-contention scenario, consider adding a brief sleep to reduce load
            time.sleep(0.01)

clientThree = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5703'],
cluster_name="hello-world")
    
# Get the distributed map
myMapFromThirdClient = clientThree.get_map("my-distributed-map").blocking()

key = "1000"

for _ in range(10000):
    incrementKeyWithOutLocking(myMapFromThirdClient, key)
