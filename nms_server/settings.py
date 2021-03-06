"""
Django settings for nms_server project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import sys
from common.globalfun import get_conf, SecpspApi

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'nms_server'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ajaja*5+z#v1i$v(ysn3fdp4tct+!st^q)(wd!r_hw3d($o70b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DEBUG_COOKIE = ""

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'dwebsocket',
    'device',
    'diagnosis',
    'domain',
    'meeting',
    'opr_log',
    'sus',
    'system_set',
    'warning',
    'misc',
    'api',
    'inner_api',
    'nms_inspect',
    'ws',
    'statistic',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'middleware.authenticate.authenticateMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.logStash.logStashMiddleware',
]

ROOT_URLCONF = 'nms_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nms_server.wsgi.application'

SESSION_COOKIE_NAME = 'nms_sessionid'

# 配置文件路径
CONFIG_PATH = os.path.join(BASE_DIR, 'conf/nms_server.ini')
LIB_PATH = '/opt/mcu/sodir64'
LIB_KDV_SECPSP = os.path.join(LIB_PATH, 'libkdvsecpsp.so')
BOARD_ID = get_conf('EqpInfo', 'BoardId', CONFIG_PATH)
sec = SecpspApi(LIB_KDV_SECPSP, BOARD_ID)
############## 连接配置 ##############
rmq_password = sec.decrypt_data(get_conf('rabbitmq', 'password', CONFIG_PATH))
mysql_password = sec.decrypt_data(get_conf('mysql', 'password', CONFIG_PATH))
redis_password = sec.decrypt_data(get_conf('redis', 'password', CONFIG_PATH))
# mysql连接池配置
SQLALCHEMY_QUEUEPOOL = {
    'pool_size': 10,
    'max_overflow': 10,
    'timeout': 5,
    'recycle': 100,
}
DB_ENGINE = 'django_conn_pool.mysql' if get_conf("nms", "db_engine", CONFIG_PATH)=='mysql' else 'django.db.backends.postgresql_psycopg2'
DATABASES = {
    # 网管数据库配置
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': 'nms_db',
        'USER': get_conf("mysql", "user", CONFIG_PATH),
        'PASSWORD': mysql_password,
        'HOST': get_conf("mysql", "host", CONFIG_PATH),
        'PORT': int(get_conf("mysql", "port", CONFIG_PATH)),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# redis配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s/0' % (get_conf('redis', 'host', CONFIG_PATH), get_conf('redis', 'port', CONFIG_PATH)),
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 10},
            'PASSWORD': redis_password,
            'CONNECTION_POOL_KWARGS': {'decode_responses': True}
        }
    }
}

# graphite配置
GRAPHITE = {
    'HOST': get_conf('graphite', 'host', CONFIG_PATH),
    'PORT': get_conf('graphite', 'port', CONFIG_PATH)
}

# kdfs配置
KDFS = {
    'HOST': get_conf('kdfs', 'host', CONFIG_PATH),
    'PORT': get_conf('kdfs', 'port', CONFIG_PATH)
}

# sus版本文件目录
SUS_DIR = '/opt/data/sus/'

# nms_server临时文件目录
TEMP_DIR = '/opt/data/nms_server/'

# 脚本文件路径
SCRIPT_PATH = os.path.join(BASE_DIR, 'nms_server/script')

# sso配置
SSO_HOST = get_conf('api', 'api_core_ip', CONFIG_PATH)
SSO_PORT = get_conf('api', 'api_core_port', CONFIG_PATH)

# 品牌0-摩云， 1-视讯，2-电信，3-dx6000
BRAND = get_conf('nms', 'brand', CONFIG_PATH)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/nmsweb/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'nms-web', 'dist'), )
INFO_URL = STATIC_URL + 'index.html#/nms/baseinfo/home'

LOGIN_URL = STATIC_URL + 'index.html#/login'
SSO_LOGIN_URL = '/portalCore/login'

CORS_ORIGIN_ALLOW_ALL = True


CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie


CORS_EXPOSE_HEADERS = ["Content-Disposition"]

# SILENCED_SYSTEM_CHECKS = ['mysql.E001']

# rest framework
# 异常处理
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'nms_server.utils.exception.exception_handler'
}
######################################################## 新增的配置项########################################################


# 导入标志, 如果数据更新导致升级需要更重新导入, 更新此标志版本号
VERSION = get_conf('nms', 'version', CONFIG_PATH)

# "api_level"是一个1开始的自增值，当平台修改了API接口后，此值需要自增，如果某个版本API没有变化，则API Level可以无需增加。
API_LEVEL = get_conf('nms', 'api_level', CONFIG_PATH)

############## 连接配置 ##############
# rmq
AMQP_URL = 'amqp://{user}:{password}@{host}:{port}/'.format(
    user=get_conf('rabbitmq', 'user', CONFIG_PATH),
    password=rmq_password,
    host=get_conf('rabbitmq', 'host', CONFIG_PATH),
    port=int(get_conf('rabbitmq', 'port', CONFIG_PATH))
)

# 日志目录
LOG_PATH = "/opt/log/nms_webserver/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(lineno)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
    },
    'handlers': {
        'file': {
            'level': "DEBUG",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, "nms_server.log"),
            # 'maxBytes': 50 * 1024 * 1024,
            # 'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': "DEBUG",
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'nms': {
            'handlers': ['file'],
            'level': "DEBUG",
            'propagate': False
        }
    }
}

WEBSOCKET_FACTORY_CLASS = 'dwebsocket.backends.uwsgi.factory.uWsgiWebSocketFactory'

# 每页数据数量
PER_PAGE = 10

# requests 请求超时时间
REQUESTS_TIMEOUT = 3