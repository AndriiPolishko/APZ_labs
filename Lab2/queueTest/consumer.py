import sys
import hazelcast
import threading

clientNode = ""

if len(sys.argv) > 1:
   clientNode = sys.argv[1]
else:
    exit("Please provide the client node name as an argument")

client = hazelcast.HazelcastClient(cluster_members=[clientNode],
cluster_name="hello-world") 

queue = client.get_queue("queue") 


def consume():
    consumed_count = 0
    while consumed_count < 100: 
        head = queue.take().result()
        print("Consuming {}".format(head))
        consumed_count += 1


consumer_thread = threading.Thread(target=consume)

consumer_thread.start()

consumer_thread.join()

client.shutdown()