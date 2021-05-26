import logging, json
from django_redis import get_redis_connection

logger = logging.getLogger('nms.'+__name__)

# 获取服务器阈值
def get_physical_server_limit(parentMoid, start, count):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_physical_server_limit.lua')
    content = fileHandler.read()
    
    try:
        server_limit = connect.eval(content, 0, parentMoid, start, count)
    except Exception as e:
        logger.error(e)
        server_limit = {}
        
    return json.loads(server_limit)

def add_warning_notify_info(domain_moid, email, phone, wechat, code_list, id):
    connect = get_redis_connection()
    user_id = 'warning:notify:' + str(domain_moid)
    user_info = 'warning:notify:' + str(id) + ':info'
    user_codes = 'warning:notify:' + str(id) + ':codes'
    codes = code_list.split(",")
    try:
        connect.sadd(user_id, id)
        connect.hmset(user_info, {'email': email, 'phone': phone, 'wechat': wechat})
        for value in codes:
            if value != '':
                connect.sadd(user_codes, value)
    except Exception as e:
        logger.error(e)

def set_warning_notify_info(domain_moid, email, phone, wechat, code_list, id):
    connect = get_redis_connection()
    user_id = 'warning:notify:' + str(domain_moid)
    user_info = 'warning:notify:' + str(id) + ':info'
    user_codes = 'warning:notify:' + str(id) + ':codes'
    codes = code_list.split(",")
    try:
        connect.hmset(user_info, {'email': email, 'phone': phone, 'wechat': wechat})
        connect.delete(user_codes)
        for value in codes:
            if value != '':
                connect.sadd(user_codes, value)
    except Exception as e:
        logger.error(e)

def del_warning_notify_info(domain_moid, id):
    connect = get_redis_connection()
    user_id = 'warning:notify:' + str(domain_moid)
    user_info = 'warning:notify:' + str(id) + ':info'
    user_codes = 'warning:notify:' + str(id) + ':codes'
    try:
        connect.delete(user_info)
        connect.delete(user_codes)
        connect.srem(user_id, id)
    except Exception as e:
        logger.error(e)

def set_global_server_limit(s_pas,s_callpair,s_nms,s_media_resource):
    connect = get_redis_connection()
    keyLimit = 'warning:limit:global'
    try:
        connect.hmset(keyLimit,{'s_pas':s_pas,'s_callpair':s_callpair,'s_nms':s_nms,'s_media_resource':s_media_resource})
    except Exception as e:
        logger.error(e)

def set_physical_server_limit(devMoid,cpu,disk,memory,port,diskwritespeed,rateofflow):
    connect = get_redis_connection()
    keyLimit = 'warning:limit:'+ devMoid
    try:
        connect.hmset(keyLimit,{'cpu':cpu,'disk':disk,'memory':memory,'port':port,'diskwritespeed':diskwritespeed,'rateofflow':rateofflow})
    except Exception as e:
        logger.error(e)

def add_terminal_type(terminalType):
    connect = get_redis_connection()
    try:
        connect.hset('terminal_type_list',terminalType.replace(' ','~'),terminalType)
    except Exception as e:
        logger.error(e)

def del_terminal_type(terminalType):
    connect = get_redis_connection()
    try:
        connect.hdel('terminal_type_list',terminalType.replace(' ','~'))
    except Exception as e:
        logger.error(e)

def init_warning_stop(moid_list):
    connect = get_redis_connection()
    try:
        connect.delete('warning:stop')
        if moid_list:
            connect.sadd('warning:stop', *moid_list)
    except Exception as e:
        logger.error(e)