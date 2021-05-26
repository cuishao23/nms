# coding:utf-8
import logging
import json
logger = logging.getLogger("nms." + __name__)
from nms_server.utils.date_conversion import time_difference
from django_redis import get_redis_connection
from nms_server.utils.error_code import *

'''
@description:  meidia资源
@param {str} domain_moid 
@return: 
    example:
    {
        "port_meeting": {
            "other": 0,
            "used": 0,
            "remainder": 224,
            "tra_used": 0,
            "total": 224
        },
        "vmr": {
            "total_8_720": 0,
            "used_large": 3,
            "env_type": 1,
            "used_32_1080": 0,
            "total_small": 640,
            "total_8_1080": 0,
            "total_large": 640,
            "used_192_720": 0,
            "total_192_720": 0,
            "used_32_720": 0,
            "used_192_1080": 0,
            "used_64_720": 0,
            "total_32_1080": 0,
            "total_64_720": 0,
            "total_192_1080": 0,
            "used_small": 0,
            "used_8_720": 0,
            "total_32_720": 0,
            "used_64_1080": 0,
            "used_8_1080": 0,
            "total_64_1080": 0
        },
        "env_type": 1,
        "access": {
            "g_ap_total": 0,
            "ap_total": 1000,
            "g_ap_used": 0,
            "ap_used": 0
        },
        "media": {
            "total_h264": 1000,
            "used_h265": 4,
            "total_g_h265": 0,
            "used_g_h264": 0,
            "total_vmp": 18,
            "used_mixer": 1,
            "total_h265": 1000,
            "used_h264": 7,
            "used_g_h265": 0,
            "total_g_h264": 0,
            "used_vmp": 1,
            "total_mixer": 32
        },
        "tra_meeting": {
            "port_used": 0,
            "other": 0,
            "used": 0,
            "remainder": 42,
            "total": 42
        },
        "vrs": {
            "recroomtotal": 0,
            "lcasttotal": 0,
            "recroomocp": 0,
            "lcastocp": 0,
            "html5lcasttotal": 0,
            "html5lcastocp": 0
        },
        "dcs": {
            "max_mt_num": 0,
            "mt_num": 0,
            "conf_num": 0,
            "max_conf_num": 0
        }
    }
'''
def get_media_vmr_api(domain_moid):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_media_vmr_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, domain_moid)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0, 'error_code':REDIS_ERROR}

# 
'''
@description: 物理服务器列表(内部api)
@param {str} domain_moid    核心域、服务域、平台域、机房moid
@return: {json}
    example:
    {
        "success": 1,
        "physicals": [
            {
                "online": "offline",
                "name": "ceu-e",
                "domain_moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
                "moid": "0500ab86-1fc2-11ea-967d-001e67e6a111",
                "machine_room_moid": "dd886c47-28db-4d1e-b624-a04b259f6756",
                "type": "ceu-e"
            },
            {
                "online": "offline",
                "name": "192.168.88.1",
                "domain_moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
                "moid": "5ef9df50-255c-11ea-a893-001e67e6a111",
                "machine_room_moid": "dd886c47-28db-4d1e-b624-a04b259f6756",
                "type": "das4000"
            }
    }
'''
def get_physical_server_list(domain_moid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_physicals_api.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, domain_moid)
    return json.loads(ret_data_str)

'''
@description: 单个物理服务器的详细信息
@param {type} 
@return: 
'''
def get_physical_server_detail(deviceMoid):
    connect = get_redis_connection()
    fileHandler = open('./nms_server/script/get_physical_server_detail.lua')
    content = fileHandler.read()
    physical_server_info = connect.eval(content, 0, deviceMoid)
    return json.loads(physical_server_info)


'''
@description: 
@param {type} domain_moid   核心域、服务域或平台域、用户域、机房moid
@return: 
{
    [   
        {
            "p_server_moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
            "type": "dss-worker",
            "ip": "172.16.185.181",
            "backup_state": "",
            "warning_level": "critical",
            "domain_moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
            "online": "online",
            "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
            "guid": "9d6d75ce-62ad-11ea-8dad-a4bf01519af2",
            "name": "dss-worker_172.16.185.181",
            "moid": "9d6d75ce-62ad-11ea-8dad-a4bf01519af2"
        },
        {
            "p_server_moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
            "type": "prsworker",
            "ip": "172.16.185.181",
            "backup_state": "",
            "warning_level": "",
            "domain_moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
            "online": "offline",
            "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
            "guid": "9d6f4aca-62ad-11ea-8dad-a4bf01519af2",
            "name": "prsworker_172.16.185.181",
            "moid": "9d6f4aca-62ad-11ea-8dad-a4bf01519af2"
        }
    ],
    "success": 1
}
'''
def get_logic_server_list(domain_moid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_logicals_api.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, domain_moid)
    return json.loads(ret_data_str) 

'''
@description: 获取置顶物理服务器下的逻辑服务器列表
@param {str} p_server_moid  
@return: 
{
    "success": 1,
    "logicals": [
        {
            "warning_level": "",
            "p_server_moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
            "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
            "moid": "9ce58d44-62ad-11ea-8dad-a4bf01519af2",
            "ip": "172.16.185.181",
            "domain_moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
            "type": "ntp",
            "backup_state": "",
            "guid": "9ce58d44-62ad-11ea-8dad-a4bf01519af2",
            "online": "offline",
            "name": "ntp_172.16.185.181"
        },
        {
            "warning_level": "",
            "p_server_moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
            "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
            "moid": "9ce85ed4-62ad-11ea-8dad-a4bf01519af2",
            "ip": "172.16.185.181",
            "domain_moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
            "type": "keepalived",
            "backup_state": "",
            "guid": "9ce85ed4-62ad-11ea-8dad-a4bf01519af2",
            "online": "offline",
            "name": "keepalived_172.16.185.181"
        }
    ]
}
'''
def get_physical_logic_server(p_server_moid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_logicals_by_physical.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, p_server_moid)
    return json.loads(ret_data_str)  

'''
@description: 获取指定域下的终端列表
@param {str} domain_moid    核心域、服务域或平台域、用户域
@param {int} start          终端的起点位置。从0开始
@param {int} count          查询的终端数量，从start开始算起
@return: 
{
    "success": 1,
    "terminals": [
        {
            "name": "0512000000000",
            "domain_moid": "ied7jq5ixs20b27dcef901ki",
            "ip": "",
            "moid": "216ec6c0-5b93-49ce-aa23-170a023ceea1",
            "online": "offline",
            "e164": "0512000000000"
        },
        {
            "name": "0512000000001",
            "domain_moid": "ied7jq5ixs20b27dcef901ki",
            "ip": "",
            "moid": "56a3a3fa-ff52-4623-87fc-d0f74e13f07b",
            "online": "offline",
            "e164": "0512000000001"
        }
    ],
    "total_count": 30
}
'''
def get_terminal_list(domain_moid, start, count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminals_api.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, domain_moid,start,count)
    return json.loads(ret_data_str)    

'''
@description: 获取服务器的硬件资源信息
@param {str} moid_list :物理服务器moid列表，逗号分隔，uri编码，最多5个 
@return: 
    example:
    {
        "physicals": [
            {
                "name": "jds6000",
                "machine_room_name": "默认机房",
                "moid": "8fe98794-62ad-11ea-8dad-a4bf01519af2",
                "ip": "",
                "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
                "type": "jds6000"
            },
            {
                "memused": 18662968,
                "name": "172.16.185.181",
                "machine_room_name": "默认机房",
                "moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
                "memtotal": 32660852,
                "cpu": 2,
                "ip": "",
                "memory": 57,
                "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
                "type": "umm"
            }
        ],
        "success": 1
    }
'''
def get_physicals_res_api(moid_list):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_physicals_res_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, moid_list)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0, 'error_code':REDIS_ERROR}

'''
@description: 
@param {str} domain_moid    核心域、服务域、平台域或用户域moid
@param {int} count
@return: 
    example:
    {
        "success": 1,
        "physicals": [
            {
                "moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
                "machine_room_name": "默认机房",
                "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
                "ip": "",
                "type": "umm",
                "name": "172.16.185.181",
                "cpu": 2
            },
            {
                "moid": "8fe98794-62ad-11ea-8dad-a4bf01519af2",
                "machine_room_name": "默认机房",
                "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
                "ip": "",
                "type": "jds6000",
                "name": "jds6000",
                "cpu": 0
            }
        ]
    }
'''

def get_topn_physicals_by_cpu_api(domain_moid, count):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_topn_physicals_by_cpu_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, domain_moid,count)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0, 'error_code':REDIS_ERROR}

'''
@description: 
@param {str} domain_moid    核心域、服务域、平台域或用户域moid
@param {int} count
@return: 
    example:
    {
        "physicals": [
            {
                "moid": "992ce364-62ad-11ea-8dad-a4bf01519af2",
                "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
                "type": "umm",
                "machine_room_name": "默认机房",
                "memory": 57,
                "name": "172.16.185.181",
                "ip": "",
                "memtotal": 32660852,
                "memused": 18662968
            },
            {
                "moid": "8fe98794-62ad-11ea-8dad-a4bf01519af2",
                "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
                "type": "jds6000",
                "machine_room_name": "默认机房",
                "memory": 0,
                "name": "jds6000",
                "ip": "",
                "memtotal": 0,
                "memused": 0
            }
        ],
        "success": 1
    }
'''
def get_topn_physicals_by_mem_api(domain_moid, count):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_topn_physicals_by_mem_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, domain_moid,count)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0, 'error_code':REDIS_ERROR}

'''
@description: 获取指定moid的物理服务器的信息
@param {str} p_server_moid 
@return: 
    example:
    {
        "moid": "8fe98794-62ad-11ea-8dad-a4bf01519af2",
        "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
        "machine_room_name": "默认机房",
        "type": "jds6000",
        "name": "jds6000",
        "ip": "",    
        "cpu":0,
        "memory": 0,    
        "memtotal": 0,
        "memused": 0,
        "frame_moid":"aaa",
        "frame_name":"kdv8000a_92",
        "frame_type":"kdv8000a"
    }
'''
def get_physical_server_info_api(p_server_moid):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_physical_info_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, p_server_moid)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}

        

'''
@description: 获取直播列表
@param {str} parentMoid
@return: 

'''
def get_live_list_api(parentMoid):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_live_list_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, parentMoid)
        ret_data = json.loads(ret_data_str)
        
        for live in ret_data['live']:
            # start_time时间格式转化 1900-03-01 00:00:00 -> 1900/03/01 00:00:00
            live['start_time'] = live['start_time'].replace('-','/')
            #获取直播时长，单位：s
            live['elapse'] = time_difference(live['start_time'] )
        return ret_data
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}

'''
@description: 获取预约直播列表
@param {str} parentMoid
@return: 

'''
def get_aplive_list_api(parentMoid):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_aplive_list_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, parentMoid)
        ret_data = json.loads(ret_data_str)
        
        for live in ret_data['aplive']:
            # start_time时间格式转化 1900-03-01 00:00:00 -> 1900/03/01 00:00:00
            live['start_time'] = live['start_time'].replace('-','/')
        return ret_data
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}

'''
@description: 获取预约会议列表
@param {str} parentMoid
@return: 

'''
def get_appointment_list_api(parentMoid):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_appointment_list_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, parentMoid)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR} 

'''
@description: 获取预约会议统计信息
@param {str} parentMoid
@param {str} start_time     "2020/02/17 06:00:00"
@param {str} end_time       "2020/02/17 06:00:00"
@return: 
{
    "success": 1,
    "statistic": {
        "time": [
            "2020/02/17 06:00:00",
            "2020/02/17 07:00:00",
            "2020/02/17 08:00:00",
            "2020/02/17 09:00:00"
        ],
        "min": 0,
        "values": [
            0,
            0,
            0,
            0
        ],
        "max": 0,
        "average": 0
    }
}
'''
def get_appointment_future_api(parentMoid, start_time, end_time):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_appointment_future_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, parentMoid, start_time, end_time)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}

'''
@description: 实时会议列表
@param {str} parentMoid
@param {str} conf_type  multi-多点会议、p2p-点对点会议，entity-实体会议
@param {int} count
@return: 
    {
    "success": 1,
    "meetings（tran、port、sfu、mix）": [
        {
        "name": "test1",
        "start_time": "2018/06/02 09:18:03",
        "end_time": "2018/06/02 10:18:03",
        "confe164": "05551234567",
        "organizer": "赵六",
        "multi": 8,
        "format": "H.264",
        "resolution": "720P",
        "encryption": "aes"
        }
    ],
    "meetings（entity）": [
        {
        "name": "test1",
        "start_time": "2018/06/02 09:18:03",
        "end_time": "2018/06/02 10:18:03",
        "organizer": "张三",
        "mobile": "1555555553",
        "telephone": "0551234567",
        "rooms": [
            {
            "id": 111,
            "name": "苏州会议室1"
            },
            {
            "id": 112,
            "name": "上海会议室2"
            }
        ]
        }
    ],
    "meetings（p2p）": [
        {
        "caller_name": "12346788",
        "callee_name": "12346579",
        "caller_e164": "12346788",
        "callee_e164": "12346579",
        "start_time": "2018/06/02 09:18:03"
        }
    ]
    }
'''
def get_domain_meetings_api(parentMoid, conf_type, count):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_domain_meetings_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, parentMoid, conf_type, count)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}

'''
@description: 获取实时会议列表（外部api）
@param {str} parentMoid     用户域moid
@return: 
'''
def get_meeting_info_list(parentMoid):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_meeting_info_list.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, parentMoid)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}


'''
@description: 获取会议终端详情
@param {str} conf_e164
@return: 
'''
def get_meeting_terminal_detail(conf_e164):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_meeting_terminal_detail_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, conf_e164)
        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}      
        


'''
@description: 获取终端诊断信息
@param {str} terminal_moid
@param {str} terminal_type
@return: 
'''
def get_terminal_hardwarestate_api(terminal_moid,terminal_type):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_terminal_hardware_state_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, terminal_moid,terminal_type)

        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}


'''
@description: 获取指定终端的入会信息
@param {str} param_type     'e164' or 'ip_sip'
@param {str} param_value     '0512000000000' or '172.16.80.236'
@return: 
    {
    "success": 1,
    "detail": {
        "primary_video": [
        {
            "chan_id": 1,
            "up_or_down": 1,
            "video_format": "H264",
            "video_framerate": 0,
            "video_up_bitrate": 0,
            "video_down_bitrate": 0,
            "video_pkts_lose": 0,
            "audio_format": "Opus",
            "audio_up_bitrate": 0,
            "audio_pkts_lose": 0,
            "audio_pkts_loserate": 0,
            "res": "1920*1080"
        },
        {
            "chan_id": 1,
            "up_or_down": 0,
            "video_format": "H264",
            "video_framerate": 0,
            "video_down_bitrate": 0,
            "video_pkts_lose": 0,
            "video_pkts_loserate": 0,
            "audio_format": "Opus",
            "audio_down_bitrate": 0,
            "audio_pkts_lose": 0,
            "audio_pkts_loserate": 0,
            "res": "1920*1080"
        }
        ],
        "dual_video": [
        {
            "chan_id": 1,
            "up_or_down": 1,
            "video_format": "H264",
            "video_framerate": 0,
            "video_up_bitrate": 0,
            "video_pkts_lose": 0,
            "video_pkts_loserate": 0,
            "res": "1920*1080"
        },
        {
            "chan_id": 1,
            "up_or_down": 0,
            "video_format": "H264",
            "video_framerate": 0,
            "video_down_bitrate": 0,
            "video_pkts_lose": 0,
            "video_pkts_loserate": 0,
            "res": "1920*1080"
        }
        ]
    }
    }
'''
def get_terminal_meeting_detail_api(param_type, param_value):
    try:
        conn = get_redis_connection()
        fileHandler = open('./nms_server/script/get_terminal_meeting_detail_api.lua')
        content = fileHandler.read()
        ret_data_str = conn.eval(content, 0, param_type, param_value)

        return json.loads(ret_data_str)
    except Exception as e:
        logger.error(e)
        return {'success':0,'error_code':REDIS_ERROR}


'''
@description: 获取指定域下的会议能力
@param {str} domain_moid    核心域、服务域、平台域、机房、用户域的moid
@return: 
'''
def get_domain_media_resource_api(domain_moid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_domain_media_resource_api.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, domain_moid)

    return json.loads(ret_data_str)


'''
@description: 获取指定媒体服务器的会议能力
@param {str} l_server_moid  媒体服务器moid
@return: 
'''
def get_server_media_resource_api(l_server_moid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_server_media_resource_api.lua')
    content = fileHandler.read()
    ret_data_str = conn.eval(content, 0, l_server_moid)

    return json.loads(ret_data_str)
