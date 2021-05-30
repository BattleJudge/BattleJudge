#!/bin/bash

UWSGI_PID_FILE="./log/uwsgi.pid"
DAPHNE_PID=$(ps -ef|grep daphne|grep -v grep|awk '{print $2}')
CELERY_PID=`head -n +1 ./log/celery.pid`

if [ -f "$UWSGI_PID_FILE" ]; then 
	uwsgi --stop $UWSGI_PID_FILE
	kill -9 ${DAPHNE_PID}
	celery multi stop w1 -A oj -l info --beat --logfile=./log/celery.log --pidfile=./log/celery.pid
	echo "finished"
else
	echo "nothing todo"
fi
