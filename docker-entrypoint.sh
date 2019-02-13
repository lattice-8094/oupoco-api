#!/bin/bash

# Start Gunicorn processes
echo "Starting Gunicorn."
exec gunicorn wsgi:app \
	 --name oupoco \
	 --forwarded-allow-ips "*" \
	 --bind 0.0.0.0:8000 \
	 --proxy-allow-from "*" \
	 "$@"