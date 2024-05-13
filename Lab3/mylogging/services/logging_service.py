from typing import Union
from fastapi import FastAPI
import hazelcast

hazelcast_client = hazelcast.HazelcastClient(
cluster_name="hello-world") 

hazecast_map = hazelcast_client.get_map("messages").blocking()

global_dict = {}

def saveMessage(msg_uuid, text):
    hazecast_map.set(msg_uuid, text)

    print(f"Message {text} saved with id {msg_uuid}")

def getMessagess():
    #values = list(global_dict.values())
    values = list(hazecast_map.values())

    if values:
        return "".join(values)
    else:
        return ""

