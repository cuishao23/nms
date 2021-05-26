#!/bin/bash
UWSGI=/opt/mcu/nms_webserver/nms_server_python3/bin/uwsgi

${UWSGI} --ini /opt/mcu/nms_webserver/nms_server/uwsgi.ini
