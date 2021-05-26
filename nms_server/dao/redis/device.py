import logging
import json
from django_redis import get_redis_connection

logger = logging.getLogger('nms.'+__name__)

'''
物理服务器
'''
# 所有服务器设备类型列表
def get_server_type_list():
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_server_type_list.lua')
    content = fileHandler.read()

    try:
        server_type_list = connect.eval(content, 0)
        logger.info('server_type_list:%s' % server_type_list)

    except Exception as e:
        logger.error(e)
        server_type_list = []

    return json.loads(server_type_list)

# 物理服务器设备类型列表
def get_physical_type_list():
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_physical_type_list.lua')
    content = fileHandler.read()

    try:
        physical_type_list = connect.eval(content, 0)
        logger.info('physical_type_list:%s' % physical_type_list)

    except Exception as e:
        logger.error(e)
        physical_type_list = []

    logger.info('physical_type_list:%s' % physical_type_list)
    return json.loads(physical_type_list)

# 机框设备类型列表
def get_frame_type_list():
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_frame_type_list.lua')
    content = fileHandler.read()

    try:
        frame_type_list = connect.eval(content, 0)
        logger.info('frame_type_list:%s' % frame_type_list)

    except Exception as e:
        logger.error(e)
        frame_type_list = []

    logger.info('frame_type_list:%s' % frame_type_list)
    return json.loads(frame_type_list)

# 非机框设备类型列表
def get_noframe_type_list():
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_noframe_type_list.lua')
    content = fileHandler.read()

    try:
        noframe_type_list = connect.eval(content, 0)
        logger.info('noframe_type_list:%s' % noframe_type_list)

    except Exception as e:
        logger.error(e)
        noframe_type_list = []

    logger.info('noframe_type_list:%s' % noframe_type_list)
    return json.loads(noframe_type_list)

# 物理服务器信息
def get_physical_server_list(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/domain_physical_server_list.lua')
    content = fileHandler.read()
    physical_server_list = connect.eval(content, 0, parentMoid)
    return json.loads(physical_server_list)

# 单个物理服务器的详细信息
def get_physical_server_info(deviceMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_physical_server_info.lua')
    content = fileHandler.read()
    physical_server_info = connect.eval(content, 0, deviceMoid)
    return json.loads(physical_server_info)

# dev_moid: 对应collector所在的服务器的moid
def get_collector_info(deviceMoid,deviceType,isTerminal):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_collector_info.lua')
    content = fileHandler.read()
    collector_info = connect.eval(content, 0, deviceMoid,deviceType,isTerminal)
    return json.loads(collector_info)

# 物理服务器磁盘信息
def get_physical_disk_info(deviceMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_physical_server_disk_info.lua')
    content = fileHandler.read()
    physical_disk_info = connect.eval(content, 0, deviceMoid)
    return json.loads(physical_disk_info)

# 在线服务器名称、类型、网卡信息（作为抓包参数显示使用）
def get_online_server_list(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_online_server_list.lua')
    content = fileHandler.read()
    server_list = connect.eval(content, 0, parentMoid)
    logger.info('server_list:%s' % server_list)
    return json.loads(server_list)   

def get_logical_server_list(pServerMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_logical_server_list.lua')
    content = fileHandler.read()
    server_list = connect.eval(content, 0, pServerMoid)
    logger.info('server_list:%s' % server_list)
    return json.loads(server_list)   

"""
终端设备
"""

# 终端设备类型列表
def get_terminal_type_list():
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminal_type_list.lua')
    content = fileHandler.read()
    terminal_type_list = connect.eval(content, 0)
    return json.loads(terminal_type_list)


# 终端设备列表
def get_terminal_list(parentMoid,deviceName,start,count):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/domain_terminal_list.lua')
    content = fileHandler.read()
    terminal_list = connect.eval(content, 0, parentMoid,deviceName,start,count)
    logger.info('terminal_list:%s' % terminal_list)
    return json.loads(terminal_list)

# 终端详情信息
def get_terminal_detail_info(deviceMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminal_detail.lua')
    content = fileHandler.read()
    terminal_detail_info = connect.eval(content, 0, deviceMoid)
    return json.loads(terminal_detail_info)

# 终端性能信息
def get_terminal_performance_info(deviceMoid, devType):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminal_performance.lua')
    content = fileHandler.read()
    terminal_performance_info = connect.eval(content, 0, deviceMoid, devType)
    return json.loads(terminal_performance_info)

# 终端详情外设信息
def get_terminal_peripherals_list(deviceMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminal_peripherals.lua')
    content = fileHandler.read()
    peripherals_list = connect.eval(content, 0, deviceMoid)
    return json.loads(peripherals_list)

# 在线终端名称、类型、网卡信息（作为抓包参数显示使用）
def get_online_terminal_list(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_online_terminal_list.lua')
    content = fileHandler.read()
    terminal_list = connect.eval(content, 0, parentMoid)
    logger.info('terminal_list:%s' % terminal_list)
    return json.loads(terminal_list)

def set_device_user_moid(devMoid,devType,userMoid):
    connect = get_redis_connection()
    keyLimit = 'device:'+ devMoid + ':user_moid'
    try:
        connect.hset(keyLimit,devType.replace(' ','~'),userMoid)
    except Exception as e:
        logger.error(e)

def del_device_user_moid(devMoid,devType):
    connect = get_redis_connection()
    keyLimit = 'device:'+ devMoid + ':user_moid'
    try:
        connect.hdel(keyLimit,devType.replace(' ','~'))
    except Exception as e:
        logger.error(e)

def get_device_user_moid(devMoid,devType):
    connect = get_redis_connection()
    keyLimit = 'device:'+ devMoid + ':user_moid'
    try:
        return connect.hget(keyLimit, devType.replace(' ','~'))
    except Exception as e:
        logger.error(e)
        return ''