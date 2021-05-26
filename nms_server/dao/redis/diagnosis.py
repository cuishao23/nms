from django_redis import get_redis_connection
import json

def get_machineroom_list(DomainMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_machineroom_list.lua')
    content = fileHandler.read()
    machine_room_list = conn.eval(content, 0, DomainMoid)
    return machine_room_list

def get_server_resource_info(deviceMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/diagnosis_server_hw_result.lua')
    content = fileHandler.read()
    server_resource_info = conn.eval(content, 0, deviceMoid)
    return json.loads(server_resource_info)