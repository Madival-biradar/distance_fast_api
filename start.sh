#!/bin/bash


# Change directory to the directory of the script
cd "$(dirname "$0")"

# Activate the virtual environment (assuming it exists in fast_env/bin/activate)
source fast_env/bin/activate

# Change to the directory where your app is located (adjust if necessary)
cd distance_fast_api

# Run uvicorn with correct syntax
uvicorn main:app --host 0.0.0.0 --workers 4
