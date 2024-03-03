#!/bin/bash
cd."${dirname."$0"}"
source fast_env/bin/activate
cd distance_fast_api
uvicorn'main:app'--host:0.0.0.0'--workers=4