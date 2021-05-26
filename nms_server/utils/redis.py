from django_redis import get_redis_connection
from django.conf import settings
from os import path
import json


def exec_redis_lua(file_name, *args):
    file_name = path.join(settings.SCRIPT_PATH, file_name)
    with get_redis_connection() as client:
        with open(file_name, encoding='utf-8') as f:
            script = f.read()
            r = client.eval(script, 0, *args)
            if r:
                try:
                    return json.loads(r, encoding='utf-8')
                except:
                    pass
            return r


def distributed_lock(lock_name):
    with get_redis_connection() as client:
        return bool(client.set(lock_name, 'lock', ex=5, nx=True))


def distributed_unlock(lock_name):
    with get_redis_connection() as client:
        client.delete(lock_name)