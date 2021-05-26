#!/bin/bash

PID_FILE=/opt/data/nms_webserver/nms_webserver.pid
UWSIG=/opt/mcu/nms_webserver/nms_server_python3/bin/uwsgi

if [ -e ${PID_FILE} ];then
    ${UWSIG} --stop ${PID_FILE}
    rm -rf ${PID_FILE}
    sleep 3
fi
uwsgi_pid=$(ps aux|grep "nms_server/uwsgi.ini"|grep -v "grep"|awk '{print $2}')
[ -z "${uwsgi_pid}" ] && echo "nms_webserver stop" || kill -9 ${uwsgi_pid}
