#!/bin/bash

# Start facade service
python3 -m uvicorn facade.api.facade_controller:app --port 8000 &

# Start logging services
python3 -m uvicorn mylogging.api.logging_controller:app --port 8001 &
python3 -m uvicorn mylogging.api.logging_controller:app --port 8002 &
python3 -m uvicorn mylogging.api.logging_controller:app --port 8003 &

# Start message service
python3 -m uvicorn messages.api.messages_controller:app --port 8004 &

# Wait for all background jobs to finish
wait
