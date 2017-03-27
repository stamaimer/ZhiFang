#!/usr/bin/env bash
# analysis.sh

/usr/bin/goaccess -f log/access_log > app/static/analysis.html
