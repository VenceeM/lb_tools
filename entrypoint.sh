#!/bin/sh
set -e

echo "Starting server..."
exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app


