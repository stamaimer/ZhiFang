#!/usr/bin/env bash
# start.sh

source venv/bin/activate

gunicorn -w 9 -k gevent run:app -p app.pid -b 0.0.0.0:7070 --log-level=DEBUG --access-logfile log/access_log --error-logfile log/error_log --preload
