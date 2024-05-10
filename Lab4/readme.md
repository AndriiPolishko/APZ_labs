# Lab#4

## Description
First we create Kafka topic with two partitions for each of our message service:

`bin/kafka-topics.sh --create --topic apz-messages --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2`

## How to run
To run facade service:
-  `python3 -m uvicorn facade.api.facade_controller:app --port 8000 --reload`

To run logging service:
- `python3 -m uvicorn mylogging.api.logging_controller:app --port 8001 --reload`
For logging service I am using ports from 8001 to 8003

To run message service:
- `python3 -m uvicorn messages.api.messages_controller:app --port 8004 --reload`
For message service I am using ports from 8004, 8005

As a client I've used Post
