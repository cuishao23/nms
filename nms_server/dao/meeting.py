from nms_server.dao.mysql.meeting import *
from nms_server.dao.redis.meeting import *
from nms_server.dao.mysql.system_set import TerminalType
from nms_server.dao.redis.domain import *
from nms_server.utils.date_conversion import get_time
import json
import logging
import datetime, time

logger = logging.getLogger("nms." + __name__)

def getPage( page ):
    if not page:
        page = 1
    else:
        page = int(page)

    start = (page - 1) * 10
    end = page * 10
    return start, end

# -----------------------------实时会议功能函数-----------------------------------
# 获取点对点会议列表
def get_realtime_p2p_meeting(parentMoid, page, meetingName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    meeting_list = []
    total_count = 0

    try:
        result = get_p2p_meeting(parentMoid,meetingName,start,10)
        meeting_list = sorted(result['meeting'], reverse=True, key=lambda x: int(time.mktime(time.strptime(x['start_time'], "%Y-%m-%d %H:%M:%S"))))
        total_count = result['total_count']
    except Exception as e:
        logger.error(e)
        pass

    return meeting_list, total_count

# 会议终端详情
def get_realtime_terminal_detail(terminalE164):
    terminal_detail_info = {}
    try:
        terminal_detail_info = get_meeting_terminal_detail(terminalE164)
        logger.info('terminal detail info:%s' % terminal_detail_info)

        if terminal_detail_info['mt_type'] != '':
          terminal_type_obj = TerminalType.objects.filter(product_name=terminal_detail_info['mt_type']).first()
          if terminal_type_obj.terminal_type == '0':
              terminal_detail_info['mt_type_category'] = '软终端'
          elif terminal_type_obj.terminal_type == '1':
              terminal_detail_info['mt_type_category'] = '硬终端'
          elif terminal_type_obj.terminal_type == '2':
              terminal_detail_info['mt_type_category'] = '终端外设'
          else:
              terminal_detail_info['mt_type_category'] = '未知类型'
          
    except Exception as e:
        logger.error(e)

    logger.info('terminal detail info:%s' % terminal_detail_info)
    return terminal_detail_info

# 会议终端主视频详情
def get_realtime_terminal_privideo(terminalE164):
    privideodata = {}
    try:
        privideodata = get_privideo_info(terminalE164)
    except Exception as e:
        logger.error(e)

    logger.info('pri video data:%s' % privideodata)
    return privideodata

# 会议终端辅视频详情
def get_realtime_terminal_assvideo(terminalE164):
    assvideodata = {}
    try:
        assvideodata = get_assvideo_info(terminalE164)
    except Exception as e:
        logger.error(e)

    logger.info('ass video data:%s' % assvideodata)
    return assvideodata
    
# 多点会议列表
def get_realtime_multi_meeting(parentMoid, page, meetingName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    meeting_list = []
    total_count = 0

    try:

        result = get_multi_meeting_list(parentMoid,meetingName,start,10)
        meeting_list = sorted(result['meeting'], reverse=True, key=lambda x: int(time.mktime(time.strptime(x['start_time'], "%Y-%m-%d %H:%M:%S"))))
        total_count = result['total_count']

    except Exception as e:
        logger.error(e)

    return meeting_list, total_count

# 多点会议详情
def get_realtime_multi_meeting_detail(meetingE164, meetingType):
    meeting_detail_info = {}
    total_score = 0
    count = 0
    try:
        # 获取会议详情
        meeting_detail_info = get_multi_meeting_detail(meetingE164, meetingType)

        # 获取会议下所有终端体验分求平均值
        scorelist = get_softhard_terminal(meetingE164, '', 0, 0)
        if scorelist:
            for value in scorelist:
                total_score = total_score + value['star']
                count = count + 1
            if count == 0:
                meetingscore = 5
            else:
                meetingscore = round(total_score / count, 1)
        else:
            meetingscore = 5
        meeting_detail_info['experience'] = meetingscore

    except Exception as e:
        logger.error(e)
        
    logger.info('meeting detail info:%s' % meeting_detail_info)
    return meeting_detail_info

# 软硬终端列表
def get_realtime_softhard_terminal(meetingE164, page, terminalName):

    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    terminal_list = []
    total_count = 0

    try:
        result = get_softhard_terminal(meetingE164,terminalName,start,10)
        terminal_list = result['terminal']
        total_count = result['total_count']
    except Exception as e:
        logger.error(e)
        pass

    logger.info('terminal_list:%s' % terminal_list)
    return terminal_list, total_count

# 电话终端列表
def get_realtime_phone_terminal(meetingE164, page, terminalName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    phone_list = []
    total_count = 0

    try:
        result = get_phone_terminal(meetingE164,terminalName,start,10)
        phone_list = result['phone']
        total_count = result['total_count']
    except Exception as e:
        logger.error(e)
        pass

    logger.info('phone_list:%s' % phone_list)
    return phone_list, total_count

# 级联会议列表获取
def get_realtime_cascade_meeting(meetingE164, page, meetingName):

    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    meeting_list = []
    total_count = 0

    try:
        result = get_cascade_meeting(meetingE164,meetingName,start,10)
        meeting_list = result['meeting']
        total_count = result['total_count']
    except Exception as e:
        logger.error(e)
        pass
    logger.info('cascade meeting list:%s' % meeting_list)
    return meeting_list, total_count

#  IP和友商列表
def get_realtime_ip_terminal(meetingE164, page, terminalName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    ip_terminal_list = []
    total_count = 0

    try:
        result = get_ip_terminal(meetingE164,terminalName,start,10)
        ip_terminal_list = result['ip_terminal']
        total_count = result['total_count']
    except Exception as e:
        logger.error(e)
        pass

    logger.info('ip_terminal_list:%s' % ip_terminal_list)
    return ip_terminal_list, total_count

#  直播列表
def get_realtime_live_info(meetingE164, page):
  # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))
    
    live_info = {}
    try:
        live_info = get_live_info(meetingE164, start, 10)
    except Exception as e:
        logger.error(e)
        
    logger.info('live_info:%s' % live_info)
    return live_info

# 数据会议信息
def get_realtime_dcs_info(meetingE164,coopState,page):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    dcs_info = {}
    try:
        dcs_info = get_dcs_info(meetingE164,coopState,start,10)
    except Exception as e:
        logger.error(e)

    return dcs_info

# 入会离会原因列表
def get_realtime_terminal_leave_reason(meetingE164, terminalMoid):
  
    leave_reason_list = {}
    try:
        leave_reason_list = get_terminal_leave_reason(meetingE164, terminalMoid)
    except Exception as e:
        logger.error(e)

    return leave_reason_list


# 参会概况列表
def get_realtime_terminal_meeting_score(meetingE164, terminalMoid):
    meeting_score_list = {}
    try:
        meeting_score_list = get_terminal_meeting_score(meetingE164, terminalMoid)
    except Exception as e:
        logger.error(e)

    return meeting_score_list


# -----------------------------历史会议功能函数-----------------------------------
# 获取点对点会议历史记录
def get_history_p2p_meeting(parentMoid, page, meetingName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    try:
        if meetingName != '':
            result = P2PMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list,caller_name__icontains=meetingName).order_by("-start_time")[start:end]
            total_count = P2PMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list,caller_name__icontains=meetingName).count()
        else:
            result = P2PMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list).order_by("-start_time")[start:end]
            total_count = P2PMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list).count()

        meeting_list = []
        for value in result:
            info_value = json.loads(value.info)
            meeting_list.append({'caller_e164': value.caller_e164,
                                 'caller_name': value.caller_name,
                                 'meeting_moid': value.meeting_moid,
                                 'callee_e164': info_value['callee_e164'],
                                 'callee_name': info_value['callee_name'],
                                 'bandwidth': info_value['bandwidth'],
                                 'start_time': get_time(value.start_time)})

    except  Exception as e:
        logger.error(e)
        meeting_list = []
        total_count = 0

    return meeting_list, total_count

# 点对点会议历史记录详情获取(主叫信息)
def get_history_p2p_meeting_detail(meetingMoid):
    caller_detail_info = {}
    try:
        meeting_info = P2PMeetingStatistic.objects.get(meeting_moid=meetingMoid)
        terminal_list = MeetingTerminalDetailStatistic.objects.filter(meeting_moid=meetingMoid)
        for value in terminal_list:
            info_value = json.loads(value.info)
            if info_value['mt_e164'] == meeting_info.caller_e164:
              caller_detail_info['name'] = meeting_info.caller_name
              caller_detail_info['e164'] = meeting_info.caller_e164
              caller_detail_info['moid'] = info_value.get('moid','')
              caller_detail_info['mt_ip'] = info_value.get('ip','')
              caller_detail_info['mt_type'] = info_value.get('mt_type','') # 终端型号

              # 终端类型
              terminal_type_obj = TerminalType.objects.filter(product_name=info_value.get('mt_type','')).first()
              if terminal_type_obj.terminal_type == '0':
                  caller_detail_info['mt_type_category'] = '软终端'
              elif terminal_type_obj.terminal_type == '1':
                  caller_detail_info['mt_type_category'] = '硬终端'
              elif terminal_type_obj.terminal_type == '2':
                  caller_detail_info['mt_type_category'] = '终端外设'
              else:
                  caller_detail_info['mt_type_category'] = '未知类型'

              caller_detail_info['conf_bitrate'] = info_value.get('conf_bitrate','')
              caller_detail_info['softversion'] = info_value.get('softversion','')
              caller_detail_info['nat_ip'] = info_value.get('nat_ip','')
              caller_detail_info['operate'] = info_value.get('operate','')
              caller_detail_info['encryption'] = info_value.get('encryption','')
              caller_detail_info['tamper'] = 'no'
              caller_detail_info['mute'] = info_value.get('mute','')
              caller_detail_info['dumbness'] = info_value.get('dumbness','')
    except Exception as e:
        logger.error(e)

    return caller_detail_info

# 点对点会议历史记录详情获取(被叫信息)
def get_history_p2p_meeting_callee(meetingMoid):
    callee_detail_info = {}
    try:
        meeting_info = P2PMeetingStatistic.objects.get(meeting_moid=meetingMoid)
        terminal_list = MeetingTerminalDetailStatistic.objects.filter(meeting_moid=meetingMoid)
        callee_e164 = ((json.loads(meeting_info.info)).get('callee_e164',''))
        meeting_info_value = json.loads(meeting_info.info)
        callee_detail_info['name'] = meeting_info_value.get('callee_name', '')
        for value in terminal_list:
            info_value = json.loads(value.info)
            if info_value.get('mt_e164','') == callee_e164:
                callee_detail_info['e164'] = info_value.get('mt_e164','')
                callee_detail_info['moid'] = info_value.get('moid','')
                callee_detail_info['mt_ip'] = info_value.get('ip','')
                callee_detail_info['mt_type'] = info_value.get('mt_type','')

                # 终端类型
                terminal_type_obj = TerminalType.objects.filter(product_name=info_value.get('mt_type','')).first()
                if terminal_type_obj.terminal_type == '0':
                  callee_detail_info['mt_type_category'] = '软终端'
                elif terminal_type_obj.terminal_type == '1':
                  callee_detail_info['mt_type_category'] = '硬终端'
                elif terminal_type_obj.terminal_type == '2':
                  callee_detail_info['mt_type_category'] = '终端外设'
                else:
                  callee_detail_info['mt_type_category'] = '未知类型'

                callee_detail_info['conf_bitrate'] = info_value.get('conf_bitrate','')
                callee_detail_info['softversion'] = info_value.get('softversion','')
                callee_detail_info['nat_ip'] = info_value.get('nat_ip','')
                callee_detail_info['operate'] = info_value.get('operate','') #运营商
                callee_detail_info['encryption'] = info_value.get('encryption','')
                callee_detail_info['tamper'] = 'no'
                callee_detail_info['mute'] = info_value.get('mute','')
                callee_detail_info['dumbness'] = info_value.get('dumbness','')
    except Exception as e:
        logger.error(e)

    return callee_detail_info

# 点对点会议历史记录详情获取(主视屏)
def get_history_p2p_privideo(meetingMoid, terminalMoid):
    privideodata = []
    try:
        # 可能有多路视频，所以返回是列表
        privideo_data_list = TerminalMeetingPrivideo.objects.filter(moid=terminalMoid, meeting_moid=meetingMoid)
        for value in privideo_data_list:
            info_value = json.loads(value.info)
            privideodata.append({'channel_id': value.channel_id,
                                 'send_video_format': info_value.get('send_video_format',''), # 发送视屏格式
                                 'send_video_res': info_value.get('send_video_res',''), # 发送视频分辨率
                                 'send_video_framerate': info_value.get('send_video_framerate',''), # 发送视屏频率
                                 'send_video_bitrate': info_value.get('send_video_bitrate',''), # 发送视屏码率
                                 'send_video_pkts_lose' : info_value.get('send_video_pkts_lose',''), # 发送视屏丢包总数
                                 'send_video_pkts_loserate': info_value.get('send_video_pkts_loserate',''), # 发送视屏丢包率
                                 'send_video_resource_exist': info_value.get('send_video_resource_exist',''), #有无视屏源
                                 'recv_video_format': info_value.get('recv_video_format',''), # 接收视屏格式
                                 'recv_video_res': info_value.get('recv_video_res',''), # 接收视频分辨率
                                 'recv_video_framerate': info_value.get('recv_video_framerate',''), # 接收视屏频率
                                 'recv_video_bitrate': info_value.get('recv_video_bitrate',''), # 接收视屏码率
                                 'recv_video_pkts_loserate': info_value.get('recv_video_pkts_loserate',''), # 接收视屏丢包率
                                 'recv_video_pkts_lose' : info_value.get('recv_video_pkts_lose',''), # 接收视屏丢包总数
                                 'send_audio_format': info_value.get('send_audio_format',''), # 发送音频格式
                                 'send_audio_pkts_lose' : info_value.get('send_audio_pkts_lose',''), # 发送音频丢包总数
                                 'send_audio_pkts_loserate': info_value.get('send_audio_pkts_loserate',''), # 发送音频丢包率
                                 'send_audio_bitrate': info_value.get('send_audio_bitrate',''), # 发送音频码率
                                 'recv_audio_format': info_value.get('recv_audio_format',''), # 接收音频格式
                                 'recv_audio_pkts_lose': info_value.get('recv_audio_pkts_lose',''), # 接收音频丢包总数
                                 'recv_audio_pkts_loserate': info_value.get('recv_audio_pkts_loserate',''), # 接收音频丢包率
                                 'recv_audio_bitrate': info_value.get('recv_audio_bitrate','') # 接收音频码率
                                })
    except Exception as e:
        logger.error(e)

    return privideodata

# 点对点会议历史记录详情获取(辅视屏)
def get_history_p2p_assvideo(meetingMoid, terminalMoid):
    assvideodata = []
    try:
        # 可能有多路视频，所以返回是列表
        assvideo_data_list = TerminalMeetingAssvideo.objects.filter(moid=terminalMoid, meeting_moid=meetingMoid)
        for value in assvideo_data_list:
            info_value = json.loads(value.info)
            assvideodata.append({'channel_id': value.channel_id, # 视屏路数，第几路辅视频
                                 'send_format': info_value.get('send_video_format',''), # 发送视屏格式
                                 'send_video_res': info_value.get('send_video_res',''), # 发送视频分辨率
                                 'send_framerate': info_value.get('send_video_framerate',''), # 发送视屏频率
                                 'send_up_bitrate': info_value.get('send_video_bitrate',''), # 发送视屏码率
                                 'send_pkts_lose': info_value.get('send_video_pkts_lose',''), # 发送视屏丢包总数
                                 'send_pkts_loserate': info_value.get('send_video_pkts_loserate',''), # 发送视屏丢包率
                                 'recv_format': info_value.get('recv_video_format',''), # 接收视屏格式
                                 'recv_video_res': info_value.get('recv_video_res',''), # 接收视频分辨率
                                 'recv_framerate':info_value.get('recv_video_framerate',''), # 接收视屏频率
                                 'recv_down_bitrate':info_value.get('recv_video_bitrate',''), # 接收视屏码率
                                 'recv_pkts_lose':info_value.get('recv_video_pkts_lose',''), # 接收视屏丢包总数
                                 'recv_pkts_loserate': info_value.get('recv_video_pkts_loserate',''), # 接收视屏丢包率
                                 'video_resource_exist': info_value.get('video_resource_exist','') # 有无视屏源
                                })
    except Exception as e:
        logger.error(e)

    return assvideodata

# 多点会议历史记录获取
def get_history_multi_meeting(parentMoid, page, meetingName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    try:
        if meetingName != '':
            result = MultiMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list, conf_name__icontains=meetingName).order_by("-start_time")[start:end]
            total_count = MultiMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list, conf_name__icontains=meetingName).count()
        else:
            result = MultiMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list).order_by("-start_time")[start:end]
            total_count = MultiMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list).count()

        meeting_list = []
        for value in result:
            info_value = json.loads(value.info)
            meeting_list.append({'domain_moid': value.domain_moid,
                                 'meeting_moid': value.meeting_moid,
                                 'conf_name': value.conf_name,
                                 'conf_e164': value.conf_e164,
                                 'conf_type': info_value.get("conf_type",''),
                                 'resolution': info_value.get("resolution",''),
                                 'frame': info_value.get("frame", ''),
                                 'bitrate': info_value.get("bitrate", ''),
                                 'start_time': get_time(value.start_time),
                                 'end_time': get_time(value.end_time),
                                 'scale': info_value.get("scale",''),
                                 'organizer': info_value.get("organizer",'')})

    except Exception as e:
        logger.error(e)
        meeting_list = []
        total_count = 0

    logger.info('multi meeting historys:%s' % meeting_list)
    return meeting_list, total_count


# 获取多点会议历史记录详情
def get_history_multi_meeting_detail(meetingMoid):
    meeting_detail_info = {}
    try:
        result = MultiMeetingStatistic.objects.get(meeting_moid=meetingMoid)
        info_value = json.loads(result.info)
        meeting_detail_info['conf_name'] = result.conf_name
        meeting_detail_info['format'] = info_value.get('format','')
        meeting_detail_info['resolution'] = info_value.get('resolution','')
        meeting_detail_info['bitrate'] = info_value.get('bitrate','')
        meeting_detail_info['encryption'] = info_value.get('encryption','')
        meeting_detail_info['guest_mode'] = info_value.get('guest_mode','')
        meeting_detail_info['call_type'] = info_value.get('call_type','')
        meeting_detail_info['frame'] = info_value.get("frame", '')
        meeting_detail_info['experience'] = info_value.get("score", 5)
    except Exception as e:
        logger.error(e)

    logger.info('meeting detail info:%s' % meeting_detail_info)
    return meeting_detail_info

# 软硬终端列表获取
def get_history_softhard_terminal(meetingMoid, page, terminalName):

    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    terminal_list = []
    total_num = 0
    try:
        if terminalName != '':
            terminal_info = MeetingTerminalDetailStatistic.objects.filter(meeting_moid=meetingMoid)
            for value in terminal_info:
                info_value = json.loads(value.info)
                if terminalName in info_value['mt_name']:
                    terminal_list.append({'name': info_value.get('mt_name',''),
                                          'ip': info_value.get('ip',''),
                                          'moid': info_value.get('moid',''),
                                          'mt_type': info_value.get('mt_type',''),
                                          'version': info_value.get('softversion',''),
                                          'e164': info_value.get('mt_e164',''),
                                          'star': info_value.get('score', 5)})
            total_num = len(terminal_list)
            terminal_list = terminal_list[start:end]

        else:
            terminal_info = MeetingTerminalDetailStatistic.objects.filter(meeting_moid=meetingMoid)[start:end]
            total_num = MeetingTerminalDetailStatistic.objects.filter(meeting_moid=meetingMoid).count()
            for value in terminal_info:
                info_value = json.loads(value.info)
                terminal_list.append({'name': info_value.get('mt_name',''),
                                      'ip': info_value.get('ip',''),
                                      'moid': info_value.get('moid',''),
                                      'mt_type': info_value.get('mt_type',''),
                                      'version': info_value.get('softversion',''),
                                      'e164': info_value.get('mt_e164',''),
                                      'star': info_value.get('score', 5)})
    except Exception as e:
        logger.error(e)

    logger.info('terminal_list:%s' % terminal_list)
    return terminal_list, total_num

# 软硬终端详情获取
def get_history_softhard_terminal_detail(meetingMoid, terminalMoid):
    terminal_detail_info = {}
    try:
        terminal_list = MeetingTerminalDetailStatistic.objects.filter(meeting_moid=meetingMoid)
        for value in terminal_list:
            info_value = json.loads(value.info)
            if info_value.get('moid','') == terminalMoid:
                terminal_detail_info['mt_name'] = info_value.get('mt_name','')
                terminal_detail_info['mt_e164'] = info_value.get('mt_e164','')
                terminal_detail_info['mt_ip'] = info_value.get('ip','')
                terminal_detail_info['mt_type'] = info_value.get('mt_type','')

                type_obj = TerminalType.objects.filter(product_name=info_value.get('mt_type','')).first()
                if type_obj.terminal_type == '0':
                    terminal_detail_info['mt_type_category'] = '软终端'
                elif type_obj.terminal_type == '1':
                    terminal_detail_info['mt_type_category'] = '硬终端'
                elif type_obj.terminal_type == '2':
                    terminal_detail_info['mt_type_category'] = '终端外设'
                else:
                    terminal_detail_info['mt_type_category'] = '未知类型'

                terminal_detail_info['conf_bitrate'] = info_value.get('conf_bitrate','')
                terminal_detail_info['softversion'] = info_value.get('softversion','')
                terminal_detail_info['nat_ip'] = info_value.get('nat_ip','')
                terminal_detail_info['operate'] = info_value.get('operate','')
                terminal_detail_info['encryption'] = info_value.get('encryption','')
                terminal_detail_info['tamper'] = info_value.get('tamper','')
                terminal_detail_info['mute'] = info_value.get('mute','')
                terminal_detail_info['dumbness'] = info_value.get('dumbness','')

    except Exception as e:
        logger.error(e)

    logger.info('terminal_detail_info:%s' % terminal_detail_info)
    return terminal_detail_info

# 电话终端列表获取
def get_history_phone_terminal(meetingMoid, page, terminalName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    phone_list = []
    total_num = 0

    try:
        if terminalName != '':
            terminal_list = TelMeetingStatistic.objects.filter(meeting_moid=meetingMoid)
            for value in terminal_list:
                info_value = json.loads(value.info)
                if terminalName in info_value.get('tel_num',''):
                    phone_list.append(info_value.get('tel_num',''))

            total_num = len(phone_list)
            phone_list = phone_list[start:end]

        else:
            terminal_list = TelMeetingStatistic.objects.filter(meeting_moid=meetingMoid)[start:end]
            total_num = TelMeetingStatistic.objects.filter(meeting_moid=meetingMoid).count()
            for value in terminal_list:
                info_value = json.loads(value.info)
                phone_list.append(info_value.get('tel_num',''))

    except Exception as e:
        logger.error(e)

    logger.info('phone_list:%s' % phone_list)
    return phone_list, total_num

#  IP和友商列表获取
def get_history_ip_terminal(meetingMoid, page, terminalName):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    ip_terminal_list = []
    total_num = 0

    try:
        if terminalName != '':
            terminal_list = IpE164MeetingStatistic.objects.filter(meeting_moid=meetingMoid)
            for value in terminal_list:
                info_value = json.loads(value.info)
                if terminalName in info_value.get("name",''):
                    ip_terminal_list.append({'name': info_value.get("name",''), 'ip': info_value.get("ip","")})

            total_num = len(ip_terminal_list)
            ip_terminal_list = ip_terminal_list[start:end]
        else:
            terminal_list = IpE164MeetingStatistic.objects.filter(meeting_moid=meetingMoid)[start:end]
            total_num = IpE164MeetingStatistic.objects.filter(meeting_moid=meetingMoid).count()
            for value in terminal_list:
                info_value = json.loads(value.info)
                ip_terminal_list.append({'name': info_value.get("name",''), 'ip': info_value.get("ip",'')})

    except Exception as e:
        logger.error(e)

    logger.info('ip_terminal_list:%s' % ip_terminal_list)
    return ip_terminal_list, total_num

#  直播列表获取
def get_history_live_info(meetingMoid, page):
    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    live_list = []
    total_num = 0

    try:
        live_info = LiveInfo.objects.filter(meeting_moid=meetingMoid)[start:end]
        total_num = LiveInfo.objects.filter(meeting_moid=meetingMoid).count()

        for value in live_info:
            info_value = json.loads(value.info)
            live_list.append({'live_moid': info_value.get('live_moid',''),
                              'max_user_time': info_value.get('max_user_time',''),
                              'max_user_count': info_value.get('max_user_count',''),
                              'start_time': info_value.get('live_start_time',''),
                              'end_time': info_value.get('live_end_time','')})

    except Exception as e:
        logger.error(e)

    logger.info('live_list:%s' % live_list)
    return live_list, total_num

# 获取直播用户列表
def get_history_live_user_info(liveMoid):

    user_info_list = []
    try:
        live_user_info = UserInfoForLive.objects.filter(live_moid=liveMoid)
        for value in live_user_info:
            info_value = json.loads(value.info)
            user_info_list.append({'user_name': info_value.get('user_name',''),
                                   'start_time': info_value.get('enter_time',''),
                                   'end_time': info_value.get('leave_time',''),
                                   'time': str(datetime.datetime.strptime(info_value.get('leave_time',''), '%Y-%m-%d %H:%M:%S') -
                                               datetime.datetime.strptime(info_value.get('enter_time',''), '%Y-%m-%d %H:%M:%S'))})
    except Exception as e:
        logger.error(e)

    logger.info('user_info_list:%s' % user_info_list)
    return user_info_list


# 数据会议信息
def get_history_meeting_dcs_info(meetingMoid, page):
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    total_num = 0
    dcs_info_list = []
    try:
        dcs_info = MeetingDcsInfo.objects.filter(meeting_moid=meetingMoid)[start:end]
        total_num = MeetingDcsInfo.objects.filter(meeting_moid=meetingMoid).count()
        for value in dcs_info:
            info_value = json.loads(value.info)
            dcs_info_list.append({'start_time': info_value.get("start_time",''),
                                  'end_time': info_value.get("end_time",''),
                                  'dcs_moid': info_value.get("dcs_moid",'')})

    except Exception as e:
        logger.error(e)

    return dcs_info_list, total_num

# 数据会议模式变更记录
def get_history_dcs_mode_change_info(dcsMoid):
    mode_change_list = []
    try:
        mode_change_info = DcsModeChangeRecode.objects.filter(dcs_moid=dcsMoid)
        for value in mode_change_info:
            info_value = json.loads(value.info)
            mode_change_list.append({'dcs_mode': info_value.get('dcs_mode',""),
                                     'mode_start_time': info_value.get('mode_start_time',""),
                                     'mode_end_time': info_value.get('mode_end_time',"")})
    except Exception as e:
        logger.error(e)

    return mode_change_list

# 数据会议终端信息
def get_history_dcs_meeting_terminal(dcsMoid):
    collaborator_list = []
    viewer_list = []
    try:
        terminal_info = TerminalInfoForDcs.objects.filter(dcs_moid=dcsMoid)
        for value in terminal_info:
            info_value = json.loads(value.info)
            if info_value['coop_state'] == 'cooperator':
                collaborator_list.append({'name': info_value.get('name',''),
                                          'e164': info_value.get('e164',''),
                                          'start_time': info_value.get('start_time',''),
                                          'end_time': info_value.get('end_time','')})
            elif info_value['coop_state'] == 'participant':
                viewer_list.append({'name': info_value.get('name',''),
                                    'e164': info_value.get('e164',''),
                                    'start_time': info_value.get('start_time',''),
                                    'end_time': info_value.get('end_time','')})
    except Exception as e:
        logger.error(e)

    return collaborator_list, viewer_list

# 入会离会原因列表
def get_history_terminal_leave_reason(meetingMoid, terminalMoid):

    leave_reason_list = []

    try:
        leave_reason_info = TerminalLeaveMeetingReason.objects.get(meeting_moid=meetingMoid, moid=terminalMoid)
        info_value = json.loads(leave_reason_info.info)

        for value in info_value:
            leave_reason_list.append({'enter_time': value.get('enter_time',''),
                                      'leave_time': value.get('leave_time',''),
                                      'leave_reason': value.get('leave_reason','')})
    except Exception as e:
        logger.error(e)

    return leave_reason_list


# 参会概况列表
def get_history_terminal_meeting_score(meetingMoid, terminalMoid):

    meeting_score_list = []

    try:
        meeting_score_info = TerminalMeetingScore.objects.get(meeting_moid=meetingMoid, moid=terminalMoid)
        info_value = json.loads(meeting_score_info.info)

        for value in info_value:
            meeting_type = value.get('type','')
            if meeting_type == 'blunt':
                count = value.get('count', '')
                note = "卡顿数为" + count + '次'
            elif meeting_type == 'lossrate':
                lossrate = value.get('lossrate', '')
                note = "丢包率为" + lossrate + '%'
            elif meeting_type == 'leave':
                reason = value.get('reason', '')
                note = reason
            else:
                note = ''

            meeting_score_list.append({'score': value.get('score',''),
                                      'time': value.get('time',''),
                                      'event': value.get('type',''),
                                      'note': note})
    except Exception as e:
        logger.error(e)

    return meeting_score_list


# 级联会议列表获取
def get_history_cascade_meeting(meetingMoid, page, meetingName):

    # 获取查询页码
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    meetings_list = []
    total_num = 0

    try:
        # 级联会议列表
        cascade_meeting_list = MeetingMeetingStatistic.objects.get(meeting_moid=meetingMoid)
        for value in cascade_meeting_list:
            cascade_info = json.loads(value.info) # 会议级联信息

            # 每个级联会议的详细信息
            cascade_meeting = MultiMeetingStatistic.objects.get(meeting_moid=cascade_info.get('attend_meeting_moid',''))
            meeting_info = json.loads(cascade_meeting.info) # 级联会议本身的信息

            if meetingName != '':
                if meetingName in cascade_meeting.conf_name:
                    meetings_list.append({'meetingName': cascade_meeting.conf_name,
                                          'meetingE164': cascade_info.get('attend_conf_e164',''),
                                          'cascadeType': cascade_info.get('cascade_type',''),
                                          'bandWidth': (json.loads(meeting_info.info).get('bandwidth','')),
                                          'startTime': cascade_info.get('attend_start_time',''),
                                          'endTime': get_time(cascade_meeting.end_time),
                                          'meetingMoid': cascade_info.get('attend_meeting_moid','')})
            else:
                meetings_list.append({'meetingName': cascade_meeting.conf_name,
                                      'meetingE164': cascade_info.get('attend_conf_e164',''),
                                      'cascadeType': cascade_info.get('cascade_type',''),
                                      'bandWidth': (json.loads(meeting_info.info).get('bandwidth','')),
                                      'startTime': cascade_info.get('attend_start_time',''),
                                      'endTime': get_time(cascade_meeting.end_time),
                                      'meetingMoid': cascade_info.get('attend_meeting_moid','')})

        total_num = len(meetings_list)
        meetings_list = meetings_list[start:end]

    except Exception as e:
        logger.error(e)

    return meetings_list, total_num

