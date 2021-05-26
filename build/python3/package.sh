#!/bin/bash

PYTHON_PATH=/opt/midware/python3
export LC_ALL="en_US.UTF-8"

pythonpath=$1/nms_server_python3

mkdir -p ${pythonpath}/lib/python3.5/site-packages
export PYTHONPATH=${pythonpath}/lib/python3.5/site-packages
INSTALL="--prefix=${pythonpath}"

package_list=`${PYTHON_PATH}/bin/pip3 list`
if [[ ${package_list} =~ "certifi" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/certifi-2019.11.28-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "chardet" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/chardet-3.0.4-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "pytz" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/pytz-2019.1-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "sqlparse" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/sqlparse-0.3.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "redis" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/redis-3.3.7-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "setuptools" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/setuptools-42.0.2-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "SQLAlchemy" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/SQLAlchemy-1.3.8.tar.gz ${INSTALL}
fi

if [[ ${package_list} =~ "Django" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/Django-2.1.4-py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "django-cors-headers" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/django_cors_headers-3.0.2-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "django-conn-pool" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/django_conn_pool-2.0.3-py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "django-redis" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/django_redis-4.10.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "djangorestframework" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/djangorestframework-3.9.4-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "hiredis" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/hiredis-1.0.0-cp35-cp35m-manylinux1_x86_64.whl ${INSTALL}
fi

if [[ ${package_list} =~ "idna" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/idna-2.8-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "lupa" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/lupa-1.8-cp35-cp35m-manylinux1_x86_64.whl ${INSTALL}
fi

if [[ ${package_list} =~ "pbr" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/pbr-5.4.3-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "PyMySQL" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/PyMySQL-0.9.3-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "six" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/six-1.12.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "python-dateutil" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/python_dateutil-2.8.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "stevedore" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/stevedore-1.31.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "urllib3" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/urllib3-1.25.7-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "requests" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/requests-2.22.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "virtualenv" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/virtualenv-16.7.7-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "virtualenvwrapper" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/virtualenvwrapper-4.8.4.tar.gz ${INSTALL}
fi

if [[ ${package_list} =~ "virtualenv-clone" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/virtualenv_clone-0.5.3-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "pika" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/pika-1.1.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "xlwt" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/xlwt-1.3.0-py2.py3-none-any.whl ${INSTALL}
fi

if [[ ${package_list} =~ "uWSGI" ]];then
    :
else
    cd package
    tar -zxf uwsgi-2.0.18.tar.gz
    cd uwsgi-2.0.18
    sed -i 's/^xml.*$/xml = false/g' buildconf/base.ini
    ${PYTHON_PATH}/bin/python3 setup.py install ${INSTALL}
    cd ..
    rm -rf uwsgi-2.0.18
    cd ..
fi

if [[ ${package_list} =~ "dwebsocket" ]];then
    :
else
    ${PYTHON_PATH}/bin/pip3 install package/dwebsocket-0.5.12.tar.gz ${INSTALL}
fi

# 国产化飞腾依赖库
\cp -a package/ft/psycopg2 ${pythonpath}/lib/python3.5/site-packages/
\cp -a package/ft/uwsgi-ft ${pythonpath}/bin/