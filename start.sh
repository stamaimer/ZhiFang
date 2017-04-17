#!/usr/bin/env bash
# start.sh

source venv/bin/activate

gunicorn -w 9 -k gevent manage:app -p app.pid -b 127.0.0.1:7071 --log-level=DEBUG --access-logfile log/access_log --error-logfile log/error_log --preload
