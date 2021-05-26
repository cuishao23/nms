#!/bin/bash

. /opt/data/luban/shells/kdfunctions
BASE_PATH=/opt/mcu/nms_webserver

mkdir -p /opt/log/nms_webserver
mkdir -p /opt/data/nms_webserver
mkdir -p BASE_PATH

# nms_server_python3
rm -rf ${BASE_PATH}/nms_server_python3
unzip -d ${BASE_PATH}/ python3/nms_server_python3.zip

# nms_server
rm -rf ${BASE_PATH}/nms_server
unzip -d ${BASE_PATH}/ nms_server.zip

# 数据库处理
# 0：mysql 1：highgodb
db_type=$(get_db_type)
# 平台类型
system_type=$(get_system_type)
if [ x"${db_type}" == x"1" ];then
    set_field_value $BASE_PATH/nms_server/conf/nms_server.ini nms db_engine highgodb
fi
if [ x"${system_type}" == x"1" ];then
    mv -f ${BASE_PATH}/nms_server_python3/bin/uwsgi-ft ${BASE_PATH}/nms_server_python3/bin/uwsgi
else
    rm -rf ${BASE_PATH}/nms_server_python3/bin/uwsgi-ft
fi