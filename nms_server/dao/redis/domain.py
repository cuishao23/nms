from django_redis import get_redis_connection
import json

# 读服务域树型结构
def get_service_domain_tree(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_service_domain_tree.lua')
    content = fileHandler.read()
    service_domain_tree = conn.eval(content, 0, parentMoid)
    return json.loads(service_domain_tree)

# 读用户域树型结构
def get_user_domain_tree(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_user_domain_tree.lua')
    content = fileHandler.read()
    user_domain_tree = conn.eval(content, 0, parentMoid)
    return json.loads(user_domain_tree)

# 读平台设备域树
def get_platform_domain_tree(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_platform_domain_tree.lua')
    content = fileHandler.read()
    platform_domain_tree = conn.eval(content, 0, parentMoid)
    return json.loads(platform_domain_tree)

# 读取指定域下子moid列表
def get_child_moid_list(parentMoid):
    conn = get_redis_connection()
    child_moid_list = conn.smembers("domain:%s:sub" % (parentMoid))
    child_moid_list = list(child_moid_list)
    return child_moid_list

def get_machine_room_moid_list(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_machine_room_moid_list.lua')
    content = fileHandler.read()
    machine_room_moid_list = conn.eval(content, 0, parentMoid)
    return json.loads(machine_room_moid_list)

def get_user_domain_moid_list(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_user_domain_moid_list.lua')
    content = fileHandler.read()
    user_domain_moid_list = conn.eval(content, 0, parentMoid)
    return json.loads(user_domain_moid_list)

# 获取指定域和其所有子域的moid信息
# parentMoid为用户域或机房时，仅返回该域的moid信息
def get_domain_moid_list(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_domain_moid_list.lua')
    content = fileHandler.read()
    user_domain_moid_list = conn.eval(content, 0, parentMoid)
    return json.loads(user_domain_moid_list)

'''
@description: 获取指定域下域列表
@param {str}  parentMoid
@return: 
    example:
    [
        {
            "parent_moid": "-1",
            "type": "kernel",
            "moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
            "name": "kedacom"
        },
        {
            "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
            "type": "service",
            "moid": "512e22e7-225d-4612-9dcf-50e585045b87",
            "name": "测试服务域"
        }
    ]
'''
# 
def get_domain_list(parentMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_domain_list.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, parentMoid)
    return json.loads(ret_data_str)

def get_domain_info(domainMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_domain_info.lua')
    content = fileHandler.read()
    domain_info = conn.eval(content, 0, domainMoid)
    return json.loads(domain_info)



'''
@description: 通过用户域或机房域moid，获取该节点和祖先节点，最高到服务域
@param {str}  domain_moid  用户域moid或机房moid
@return: 
    example:
    [
        {
            "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
            "type": "service",
            "moid": "512e22e7-225d-4612-9dcf-50e585045b87",
            "name": "测试服务域"
        },
        {
            "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
            "type": "user",
            "moid": "512e22e7-225d-4612-9dcf-50e585045b87",
            "name": "测试服务域"
        }
    ]
'''
def get_domain_list_by_Leaf(parentMoid,RootMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_domain_list_by_Leaf.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, parentMoid, RootMoid)
    return json.loads(ret_data_str)

'''
@description: 获取指定域置顶key的值
@param {str} domainMoid
@param {str} KeyValue
@return: 
'''
def get_domain_info_field(domainMoid,KeyValue):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_domain_info_field.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, domainMoid,KeyValue)
    return ret_data_str

'''
@description: 获取指定机房指定key的值
@param {str} machineRoomMoid
@param {str} KeyValue
@return: 
'''
def get_machine_room_info_field(machineMoid,KeyValue):
    conn = get_redis_connection()
    return conn.hget('machine_room:'+machineMoid+':info', KeyValue)