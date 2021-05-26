from nms_server.utils.redis import exec_redis_lua
import json


def get_license(domain_moid_list):
    import time
    now = time.strftime("%Y-%m-%d")
    r = exec_redis_lua('inspect_license.lua', json.dumps(domain_moid_list))
    for info in r:
        info['auth_status'] = 'normal' if info['auth_dead_time'] >= now else 'expired'
    return r


def get_resource_info(parent_domain_moid):
    return exec_redis_lua('get_meeting_resource.lua', parent_domain_moid)


def get_server(machine_room_moid_list):
    return exec_redis_lua('inspect_server.lua', json.dumps(machine_room_moid_list))


def get_server_hw_result(machine_room_moid_list):
    return exec_redis_lua('inspect_server_hw_result.lua', json.dumps(machine_room_moid_list))


def get_terminal(domain_moid_list):
    return exec_redis_lua('inspect_terminal.lua', json.dumps(domain_moid_list))
