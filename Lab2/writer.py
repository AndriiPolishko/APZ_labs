import hazelcast

client = hazelcast.HazelcastClient(
cluster_name="hello-world"
) 
    
# Get the distributed map
my_map = client.get_map("my-distributed-map").blocking()

values = ['BMW', 'Mercedes', 'Audi', 'Toyota', 'Honda', 'Ford', 'Nissan', 'Tesla', 'Hyundai', 'Kia']

for i in range(1000):
  my_map.set(str(i), values[i % len(values)])

my_map.set("1000", 0)


print("Writer: Done writing to the map.")