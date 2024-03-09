import hazelcast
import threading

client = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701'],
cluster_name="hello-world") 

queue = client.get_queue("queue") 
print(queue.size().result())

def produce():
    for i in range(100):
        queue.offer("value-" + str(i))


producer_thread = threading.Thread(target=produce)

producer_thread.start()

producer_thread.join()

print(queue.size().result())

client.shutdown()

print("Producer: Done producing to the queue.")
