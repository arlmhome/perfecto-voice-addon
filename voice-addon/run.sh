#!/bin/sh
set -eu
export OPENAI_API_KEY="$(python3 -c 'import json; print(json.load(open("/data/options.json")).get("openai_api_key",""))')"
exec python3 /app/server.py
