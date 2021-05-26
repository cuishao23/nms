import logging
import json
from django_redis import get_redis_connection

logger = logging.getLogger('nms.'+__name__)

'''
会议质量
'''
def get_realtime_meeting_quality(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_meeting_quality.lua')
    content = fileHandler.read()

    try:

        meeting_quality = connect.eval(content, 0, parentMoid)
        logger.info('meeting quality:%s' % meeting_quality)

    except Exception as e:
        logger.error(e)
        meeting_quality = []
    return json.loads(meeting_quality)

'''
会议资源
'''
def get_meeting_resource(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_meeting_resource.lua')
    content = fileHandler.read()

    try:
        meeting_resource = connect.eval(content, 0, parentMoid)
        logger.info('meeting resource:%s' % meeting_resource)

    except Exception as e:
        logger.error(e)
        meeting_resource = {}

    return json.loads(meeting_resource)


'''
预约会议列表
'''
def get_appoint_meeting_list(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_appoint_meeting.lua')
    content = fileHandler.read()

    try:
        meeting_list = connect.eval(content, 0,parentMoid)
        logger.info('meeting_list:%s' % meeting_list)

    except Exception as e:
        logger.error(e)
        meeting_list = []

    return json.loads(meeting_list)

'''
返回所有服务器的磁盘寿命信息
'''
def get_disk_age(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_disk_age.lua')
    content = fileHandler.read()

    try:
        server_list = connect.eval(content, 0,parentMoid)
        logger.info('server_list:%s' % server_list)

    except Exception as e:
        logger.error(e)
        server_list = []

    return json.loads(server_list)

'''
返回所有磁盘的使用率信息
'''
def get_disk_usage(parentMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_disk_usage.lua')
    content = fileHandler.read()

    try:
        server_list = connect.eval(content, 0,parentMoid)
        logger.info('server_list:%s' % server_list)

    except Exception as e:
        logger.error(e)
        server_list = []

    return json.loads(server_list)