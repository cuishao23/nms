#!/bin/bash

version=6.1.0.4.0
myDate="${version}-`date '+%Y%m%d%H%M'`"

mkdir -p .files_temp/
ls build
\cp -a build .files_temp/
mkdir -p .files_temp/build/nms_server
ls | grep -v ".files_temp" | grep -v "build" | xargs -i \cp -a {} .files_temp/build/nms_server

#依赖库拷贝
\cp -a ../nms_python/certifi-2019.11.28-py2.py3-none-any.whl         .files_temp/build/python3/package/
\cp -a ../nms_python/chardet-3.0.4-py2.py3-none-any.whl              .files_temp/build/python3/package/
\cp -a ../nms_python/setuptools-42.0.2-py2.py3-none-any.whl          .files_temp/build/python3/package/
\cp -a ../nms_python/SQLAlchemy-1.3.8.tar.gz                         .files_temp/build/python3/package/
\cp -a ../nms_python/Django-2.1.4-py3-none-any.whl                   .files_temp/build/python3/package/
\cp -a ../nms_python/django_conn_pool-2.0.3-py3-none-any.whl         .files_temp/build/python3/package/
\cp -a ../nms_python/django_cors_headers-3.0.2-py2.py3-none-any.whl  .files_temp/build/python3/package/
\cp -a ../nms_python/django_redis-4.10.0-py2.py3-none-any.whl        .files_temp/build/python3/package/
\cp -a ../nms_python/djangorestframework-3.9.4-py2.py3-none-any.whl  .files_temp/build/python3/package/
\cp -a ../nms_python/hiredis-1.0.0-cp35-cp35m-manylinux1_x86_64.whl  .files_temp/build/python3/package/
\cp -a ../nms_python/idna-2.8-py2.py3-none-any.whl                   .files_temp/build/python3/package/
\cp -a ../nms_python/lupa-1.8-cp35-cp35m-manylinux1_x86_64.whl       .files_temp/build/python3/package/
\cp -a ../nms_python/pbr-5.4.3-py2.py3-none-any.whl                  .files_temp/build/python3/package/
\cp -a ../nms_python/PyMySQL-0.9.3-py2.py3-none-any.whl              .files_temp/build/python3/package/
\cp -a ../nms_python/python_dateutil-2.8.0-py2.py3-none-any.whl      .files_temp/build/python3/package/
\cp -a ../nms_python/pytz-2019.1-py2.py3-none-any.whl                .files_temp/build/python3/package/
\cp -a ../nms_python/redis-3.3.7-py2.py3-none-any.whl                .files_temp/build/python3/package/
\cp -a ../nms_python/requests-2.22.0-py2.py3-none-any.whl            .files_temp/build/python3/package/
\cp -a ../nms_python/six-1.12.0-py2.py3-none-any.whl                 .files_temp/build/python3/package/
\cp -a ../nms_python/sqlparse-0.3.0-py2.py3-none-any.whl             .files_temp/build/python3/package/
\cp -a ../nms_python/stevedore-1.31.0-py2.py3-none-any.whl           .files_temp/build/python3/package/
\cp -a ../nms_python/urllib3-1.25.7-py2.py3-none-any.whl             .files_temp/build/python3/package/
\cp -a ../nms_python/uwsgi-2.0.18.tar.gz                             .files_temp/build/python3/package/
\cp -a ../nms_python/virtualenv-16.7.7-py2.py3-none-any.whl          .files_temp/build/python3/package/
\cp -a ../nms_python/virtualenv_clone-0.5.3-py2.py3-none-any.whl     .files_temp/build/python3/package/
\cp -a ../nms_python/virtualenvwrapper-4.8.4.tar.gz                  .files_temp/build/python3/package/
\cp -a ../nms_python/pika-1.1.0-py2.py3-none-any.whl                 .files_temp/build/python3/package/
\cp -a ../nms_python/xlwt-1.3.0-py2.py3-none-any.whl                 .files_temp/build/python3/package/
\cp -a ../nms_python/dwebsocket-0.5.12.tar.gz                        .files_temp/build/python3/package/
\cp -a ../nms_python/ft                                              .files_temp/build/python3/package/

# python3 模块打包
cd .files_temp/build/python3/
PACKAGE_PATH=$(pwd)
./package.sh ${PACKAGE_PATH}
rm -rf package
zip -r nms_server_python3.zip nms_server_python3/
rm -rf nms_server_python3
cd -

# 前端打包
cd .files_temp/build
dist_path=$(pwd)/nms_server/nms-web
./nms-web/package.sh ${dist_path}
cd -

# 后端打包
cd .files_temp/build/
echo ${myDate} > nms_server/version
sed -i "s/#version#/$myDate/g" nms_server/conf/nms_server.ini
zip -r nms_server.zip nms_server/
rm -rf nms_server
cd - 

# 国产化数据库处理
cd .files_temp/build/
\cp -a ../../../nms-sql/ft/nms.sql ./
cd -

#make nms_server.bin
cd .files_temp
chmod +x build/install.sh
makeself.sh build/  nms_webserver.bin  "Installing nms_webserver..." ./install.sh
cd - 

\cp -a .files_temp/nms_webserver.bin ../../../10-common/version/release/linux/nms/nms_webserver.bin
rm -rf .files_temp