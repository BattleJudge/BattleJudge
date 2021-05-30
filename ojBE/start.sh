#!/bin/sh
 
UWSGI_COUNT=`netstat -an | grep ":9600" | awk '$1 == "tcp" && $NF == "LISTEN" {print $0}' | wc -l`

if [ $UWSGI_COUNT -eq 0 ];then
    uwsgi --ini uwsgi.ini &
    daphne -b 127.0.0.1 -p 9621 oj.routing:application --access-log ./log/daphne.log &
    celery multi start w1 -A oj -l info --beat --logfile=./log/celery.log --pidfile=./log/celery.pid
    echo "start"
else
    echo "nothing todo"
fi
