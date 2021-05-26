from django_redis import get_redis_connection
import logging, json

logger = logging.getLogger('nms.'+__name__)

'''
@description: 获取点对点会议列表
@param 无
@return: {json}
example：
{
    "total_count":2    # 点对点会议总数
    "meeting":[
        {
            "meeting_moid": "fsdgdfhfhfghhfhrger",
            "caller_e164": "051211118889",
            "caller_name": "李四",
            "callee_e164": "051211118890",
            "callee_name": "张三"
            "bandwidth": "512",
            "start_time": "2020-03-26 11:10:03"
        },
        {
            "meeting_moid": "sdgdhfdhsererwerw",
            "caller_e164": "051211118833",
            "caller_name": "kimmi",
            "callee_e164": "051211118824",
            "callee_name": "lucy"
            "bandwidth": "1024",
            "start_time": "2020-03-26 11:20:10"
        }]
}
'''
def get_p2p_meeting(parentMoid,meetingName,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_p2p_meeting_list.lua')
    content = fileHandler.read()
    meeting_list = conn.eval(content, 0, parentMoid,meetingName,start,count)
    return json.loads(meeting_list)

'''
@description: 获取会议终端详情
@param 无
@return: {json}
example：
{
    "moid": "fsdgdfhfhfghhfhrger",
    "tamper": "no",
    "e164": "051211118890",
    "name": "张三"
    "operate": "中国电信",
    "mt_type": "Truelink"
    "conf_bitrate": "512",
    "softversion": "2.3.1.0",
    "encryption": "sm4",
    "mute": "1",
    "dumbness": "0"
    "mt_ip": "172.16.185.181",
    "nat_ip": "172.16.185.183"
}
'''
def get_meeting_terminal_detail(terminalE164):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_meeting_terminal_detail.lua')
    content = fileHandler.read()
    terminal_info = conn.eval(content, 0, terminalE164)
    return json.loads(terminal_info)

'''
@description: 获取终端主视频信息
@param 无
@return: {json}
example：
[
    {
        "channel_id":"1",
        "send_video_format":"",    --发送视屏格式
        "send_video_res":"",       --发送视频分辨率
        "send_video_framerate":"", --发送视屏频率
        "send_video_up_bitrate":"",--发送视屏码率
        "send_video_pkts_lose":"", --发送视屏丢包总数
        "send_video_pkts_loserate":"", --发送视屏丢包率
        "send_video_resource_exist":"", --有无视屏源
        "recv_video_format":"",    --接收视屏格式
        "recv_video_res":"",       --接收视频分辨率
        "recv_video_framerate":"", --接收视屏频率
        "recv_video_down_bitrate":"", --接收视屏码率
        "recv_video_pkts_loserate":"", --接收视屏丢包率
        "recv_video_pkts_lose":"", --接收视屏丢包总数
        "send_audio_format":"",    --发送音频格式
        "send_audio_pkts_lose":"", --发送音频丢包总数
        "send_audio_pkts_loserate":"", --发送音频丢包率
        "send_audio_up_bitrate":"", --发送音频码率
        "recv_audio_format":"",     --接收音频格式
        "recv_audio_pkts_lose":"", --接收音频丢包总数
        "recv_audio_pkts_loserate":"", --接收音频丢包率
        "recv_audio_down_bitrate":"" --接收音频码率
    },
]
'''
def get_privideo_info(terminalE164):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_privideo_info.lua')
    content = fileHandler.read()
    privideo_info = conn.eval(content, 0, terminalE164)
    return json.loads(privideo_info)

# 获取终端辅视频信息
def get_assvideo_info(terminalE164):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_assvideo_info.lua')
    content = fileHandler.read()
    assvideo_info = conn.eval(content, 0, terminalE164)
    return json.loads(assvideo_info)

# 获取多点会议列表
def get_multi_meeting_list(parentMoid,meetingName,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_muti_meeting_list.lua')
    content = fileHandler.read()
    meeting_list = conn.eval(content, 0, parentMoid,meetingName,start,count)
    return json.loads(meeting_list)

# 获取多点会议详情
def get_multi_meeting_detail(meetingE164,meetingType):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_muti_meeting_detail_info.lua')
    content = fileHandler.read()
    meeting_info = conn.eval(content, 0, meetingE164,meetingType)
    return json.loads(meeting_info)

# 软硬终端列表
def get_softhard_terminal(meetingE164, terminalName,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_softhard_terminal.lua')
    content = fileHandler.read()
    terminal_list = conn.eval(content, 0, meetingE164, terminalName,start,count)
    return json.loads(terminal_list)

# 电话终端列表
def get_phone_terminal(meetingE164, terminalName,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_phone_terminal.lua')
    content = fileHandler.read()
    phone_list = conn.eval(content, 0, meetingE164, terminalName,start,count)
    return json.loads(phone_list)

def get_cascade_meeting(meetingE164,meetingName,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_cascade_meeting.lua')
    content = fileHandler.read()
    meeting_list = conn.eval(content, 0, meetingE164, meetingName,start,count)
    return json.loads(meeting_list)

def get_ip_terminal(meetingE164,terminalName,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_ip_terminal.lua')
    content = fileHandler.read()
    ip_terminal_list = conn.eval(content, 0, meetingE164, terminalName,start,count)
    return json.loads(ip_terminal_list)

'''
@description: 直播信息
@param 无
@return: {json}
example：
{
    "liveinfo":
    {
        "live_name":"例会直播",
        "start_time":"2020-03-26 11:00:00",
        "encmode":"1",
        "authmode":"2",
        "max_user_time":"2020-03-26 11:20:00",
        "max_user_count":"30",
        "current_user_count":"25"
    },
    "total_count":2
    "user":[
        {
            "moid": "qwerrtyhhjyrmfnf"
            "e164": "051211118889",
            "name": "张三",
            "enter_time": "2020-03-26 11:10:03"
        },
        {
            "moid": "wwertthgfhjhhkiyku"
            "e164": "051211118810",
            "name": "李四",
            "enter_time": "2020-03-26 11:20:10"
        }]
}
'''
def get_live_info(meetingE164,start,count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_live_info.lua')
    content = fileHandler.read()
    live_info = conn.eval(content, 0, meetingE164,start,count)
    return json.loads(live_info)

'''
@description: 数据会议信息
@param 无
@return: {json}
example：
{   
    "dcsinfo":
    {
        "start_time":"2020-03-26 11:10:03",       # 数据会议开始时间
        "dcs_mode": "0",                          # DCS模式, 0-自由模式/1-管理方模式
        "mode_start_time": "2020-03-26 11:20:03"  # DCS模式开始时间
    }
    "total_count":2    # 参与数据协作的用户总数
    "user":[
        {
            "e164": "051211118889",
            "name": "张三",
            "coop_state": "1",  # 协作状态0-未参与协作， 1-参与协作
            "begin_time": "2020-03-26 11:10:03",
            "end_time": "2020-03-26 11:10:10"
        },
        {
            "e164": "051211118810",
            "name": "李四",
            "coop_state": "1",  # 协作状态0-未参与协作， 1-参与协作
            "begin_time": "2020-03-26 11:20:10",
            "end_time": "2020-03-26 11:20:15"
        }]
}
'''
def get_dcs_info(meetingE164, coopState, start, count):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_dcs_info.lua')
    content = fileHandler.read()
    dcs_info = conn.eval(content, 0, meetingE164, coopState, start, count)
    return json.loads(dcs_info)

def get_terminal_leave_reason(meetingE164, terminalMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminal_leave_reason.lua')
    content = fileHandler.read()
    leave_info_list = conn.eval(content, 0, meetingE164, terminalMoid)
    return json.loads(leave_info_list)

def get_terminal_meeting_score(meetingE164, terminalMoid):
    conn = get_redis_connection()
    fileHandler = open('./nms_server/script/get_terminal_meeting_score.lua')
    content = fileHandler.read()
    meeting_score_list = conn.eval(content, 0, meetingE164, terminalMoid)
    return json.loads(meeting_score_list)