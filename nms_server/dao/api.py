# coding:utf-8
import ast
from rest_framework import serializers
from nms_server.settings import GRAPHITE, REQUESTS_TIMEOUT

from nms_server.dao.mysql.system_set import TerminalType
from nms_server.dao.redis.domain import *
from nms_server.dao.redis.api import *
from nms_server.dao.mysql.warning import ServerWarningUnrepaired,TerminalWarningUnrepaired
from nms_server.dao.mysql.meeting import MultiMeetingStatistic,P2PMeetingStatistic,EntityMeetingStatistic
from nms_server.dao.mysql.device import OldTerminal
from nms_server.utils.error_code import *
from nms_server.utils.date_conversion import graphite_time,timestamp_to_time,timestamp_to_iso_time
import requests

USB_STORAGE_EXISTS_WARNING_CODE = 2044  # 系统检测u盘告警码

import logging
logger = logging.getLogger("nms." + __name__)

class BmcTerminalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TerminalType  # 定义关联的 Model
        fields = ('name', 'terminal_type', 'device_tag', 'platform_type')  # 指定返回的 fields

'''
@description: 获取终端型号列表
@param 无
@return: {json}
example：
{
    'success':1,
    'data':
    [
        {
            "data": [
                {
                    "terminalType": "1",
                    "deviceTag": "TSMT"
                }
            ],
            "name": "TS400"
        },
        {
            "data": [
                {
                    "terminalType": "1",
                    "deviceTag": "T300E"
                },
                {
                    "terminalType": "1",
                    "deviceTag": "T300E-CS"
                },
                {
                    "terminalType": "1",
                    "deviceTag": "T300E-S"
                }
            ],
            "name": "T300E"
        }
    ]    
}
'''
def get_bmc_terminal_type():
    try:
        terminal_type_obj = TerminalType.objects.values(
            'name', 'terminal_type', 'device_tag', 'platform_type').distinct()
        ser_data = BmcTerminalTypeSerializer(terminal_type_obj, many=True)

        dic_data = {}
        for target_list in ser_data.data:
            dic_data[target_list['name']] = []

        for target_list in ser_data.data:
            dic_data[target_list['name']].append({
                'terminalType': target_list['terminal_type'],
                'deviceTag': target_list['device_tag'],
                'platformType': target_list['platform_type']
            })

        
        ret_data = {
            'success':1,
            'data':[]
        }
        for k in dic_data:
            ret_data['data'].append({
                'name': k,
                'data': dic_data[k]
            })
        return ret_data
    except:
        return {'success':0,'error_code':MYSQL_ERROR}

class ServerUnrepairedWarningSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ServerWarningUnrepaired  # 定义关联的 Model
        fields = ('device_name', 'device_moid', 'device_type', 'device_ip', 'machine_room_moid',
                  'machine_room_name', 'code', 'start_time', 'description')  # 指定返回的 fields

'''
@description: 获取制定制定域下制定level的最新的n条服务器未修复告警
@param {int} count
@param {str} count
@param {str} warning_level
@return: 

'''
def get_top_unrepaired_warning(count, domain_moid, warning_level):
    # try:
    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(domain_moid)
    warning_obj = ServerWarningUnrepaired.objects.filter(level__exact=warning_level, machine_room_moid__in=machine_room_list).order_by("-start_time")[:count]
    ser_data = ServerUnrepairedWarningSerializer(warning_obj, many=True)

    ret_data = {
        'success': 1,
        'unrepaired_warnings': ser_data.data
    }
    return ret_data
    # except:
    #     return {'success':0,'error_code':MYSQL_ERROR}

'''
@description: 定义求平均值的函数
@param {list} num_list
@return: {int}
'''
def avg(num_list):
    num_count = 0
    for item in num_list:
        if item:
            num_count += item
    res = num_count // len(num_list)
    # 将求得的结果返回
    return res

'''
@description: graphite request
@param {str} graphite_args
    example: "target=summarize(sumSeries(nms.meeting.mooooooo-oooo-oooo-oooo-defaultmachi.{traditional_count,port_count}),'15min','last')&from=&until=&format=json"
@return: 
    example:
    {
        'max': 0,
        'min': 0,
        'average': 0,
        'time': ["2020/03/16 02:30:00",
                "2020/03/16 02:45:00",
                "2020/03/16 03:00:00"],
        'values': [0, 0, 0]
    }
'''

def graphite_request(graphite_args):
    ip = GRAPHITE['HOST']
    port = GRAPHITE['PORT']

    graphite_url = "http://"+ip+":"+port+"/render/?" + graphite_args

    # 向graphite请求数据
    response_data =  requests.get(graphite_url, timeout=REQUESTS_TIMEOUT)
    statistic_data = {
                'max':0,
                'min':0,
                'average':0,
                'time':[],
                'values':[]
            }

    if response_data.status_code == 200:
        json_data = response_data.json()

        if json_data != []:
            for k in json_data[0]['datapoints']:
                value = k[0] if k[0] else 0
                statistic_data['values'].append(value)
                statistic_data['time'].append(timestamp_to_time(k[1]))
            statistic_data['max'] = max(statistic_data['values'])
            statistic_data['min'] = min(statistic_data['values'])
            statistic_data['average'] = avg(statistic_data['values'])
    return statistic_data


'''
@description: 获取指定域下会议数量统计
@param  {str} domain_moid   example: '05geh68ddr8j5u7ijs6mwwms'    
@param  {str} start_time    example: '0000_20200316'
@param  {str} end_time      example: '2359_20200316'
@return: {json}
    example:
    {
        'success': 1,
        'statistic': {
            'multi': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            },
            'p2p': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            }
        }
    }
'''
def get_meeting_count_statistic(domain_moid, start_time, end_time):
    if domain_moid != 'all':
        user_domain_moid_list = get_user_domain_moid_list(domain_moid)
        muliti_args = "target=summarize(sumSeries(nms.meeting.{%s}.multi_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)
        
        p2p_args = "target=summarize(sumSeries(nms.meeting.{%s}.p2p_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)
    else:
        muliti_args = "target=summarize(sumSeries(nms.meeting.*.multi_count),'15min','last'&noNullPoints=true)&from=%s&until=%s&format=json" % (start_time, end_time)
        
        p2p_args = "target=summarize(sumSeries(nms.meeting.*.p2p_count),'15min','last'&noNullPoints=true)&from=%s&until=%s&format=json" % (start_time, end_time)
    
    multi_statistic = graphite_request(muliti_args)
    p2p_statistic = graphite_request(p2p_args)

    ret_data = {
        'success':1,
        'statistic':{
            'multi':multi_statistic,
            'p2p':p2p_statistic
        }
    }
    
    return ret_data

'''
@description: 获取指定域下入会终端（软硬终端、电话终端、ipe164友商终端,ipc）数量统计
@param  {str} domain_moid   example: '05geh68ddr8j5u7ijs6mwwms'    
@param  {str} start_time    example: '0000_20200316'
@param  {str} end_time      example: '2359_20200316'
@return: {json}
    example:
    {
        'success': 1,
        ''
        'statistic': {
            'multi': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            },
            'p2p': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            }
        }
    }
'''
def get_meeting_terminal_statistic(domain_moid, start_time, end_time):
    user_domain_moid_list = get_user_domain_moid_list(domain_moid)
    multi_terminal_args = "target=summarize(sumSeries(nms.meeting.{%s}.multi_terminal_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)

    multi_terminal_statistic = graphite_request(multi_terminal_args)

    p2p_terminal_args = "target=summarize(sumSeries(nms.meeting.{%s}.p2p_terminal_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)

    p2p_terminal_statistic = graphite_request(p2p_terminal_args)

    ret_data = {
        'success':1,
        'total_count':len(p2p_terminal_statistic['time']),
        'statistic':{
            'multi':multi_terminal_statistic,
            'p2p':p2p_terminal_statistic
        }
    }
    
    return ret_data



'''
@description: 获取指定域下入会终端（软硬终端、电话终端、ipe164友商终端,ipc）数量统计
@param  {str} domain_moid   example: '05geh68ddr8j5u7ijs6mwwms'    
@param  {str} start_time    example: '0000_20200316'
@param  {str} end_time      example: '2359_20200316'
@return: {json}
    example:
    {
        'success': 1,
        'statistic':{
            'sip': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            },
            'h323': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            },
            'rtc': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            },
            'all': {
                'max': 0,
                'min': 0,
                'average': 0,
                'time': ["2020/03/16 02:30:00",
                        "2020/03/16 02:45:00",
                        "2020/03/16 03:00:00"],
                'values': [0, 0, 0]
            }         
        }

    }
'''
def get_pas_terminal_online_statistic(domain_moid, start_time, end_time):
    user_domain_moid_list = get_user_domain_moid_list(domain_moid)
    sip_args = "target=summarize(sumSeries(nms.device.{%s}.sip_online_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)

    sip_statistic = graphite_request(sip_args)

    h323_args = "target=summarize(sumSeries(nms.device.{%s}.h323_online_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)

    h323_statistic = graphite_request(h323_args)

    rtc_args = "target=summarize(sumSeries(nms.device.{%s}.rtc_online_count),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)

    rtc_statistic = graphite_request(rtc_args)

    all_args = "target=summarize(sumSeries(nms.device.{%s}.{sip_online_count,h323_online_count,rtc_online_count}),'15min','last')&noNullPoints=true&from=%s&until=%s&format=json" % (','.join(user_domain_moid_list), start_time, end_time)

    all_statistic = graphite_request(all_args)

    ret_data = {
        'success':1,
        'statistic':{
            'sip':sip_statistic,
            'h323':h323_statistic,
            'rtc':rtc_statistic,
            'all':all_statistic
        }
    }
    
    return ret_data

def get_terminal_online_statistic(domain_moid, start, count, period = False, start_time = False, end_time = False):
    user_domain_moid_list = get_user_domain_moid_list(domain_moid)
    
    if period:
        time_str = '&from=' + period
    else:
        time_str = "&from=%s&until=%s" % (start_time,end_time)
    
    args = "target=summarize(nms.device.{%s}.{sip_online_count,h323_online_count,rtc_online_count},'15min','last')&noNullPoints=true%s&format=json" % (','.join(user_domain_moid_list),time_str)

    logger.info("user_domain_moid_list : %s",user_domain_moid_list)
    ip = GRAPHITE['HOST']
    port = GRAPHITE['PORT']

    graphite_url = "http://"+ip+":"+port+"/render/?" + args

    ret_data = {
        'success':1,
        'total_count':0,
        'statistic':[]
    }

    end_pos = start + count

    logger.info("graphite_url:%s", graphite_url)
    # 向graphite请求数据
    response_data =  requests.get(graphite_url, timeout=REQUESTS_TIMEOUT)
    if response_data.status_code == 200:
        json_data = response_data.json()
        static_data = {}
        if json_data != []:
            for i in json_data:
                user_moid = i['tags']['name'].split('.')[2]
                data_type = i['tags']['name'].split('.')[3][:-6]

                for k in i['datapoints']:
                    if user_moid in static_data:
                        static_time = k[1]
                        if static_time in static_data[user_moid]:
                            static_data[user_moid][static_time][data_type] = k[0] if k[0] else 0
                        else:
                            static_data[user_moid][static_time] = {}
                    else:
                        static_data[user_moid] = {}

    # logger.info("static_data:%s",static_data)

    for domain_moid in static_data:
        for static_time in static_data[domain_moid]:
            tmp_data =  static_data[domain_moid][static_time]

            ret_data['statistic'].append({
                'domain_moid':domain_moid,
                'statistic_time':static_time,
                'sip_online':int(tmp_data.get('sip_online',0)),
                'h323_online':int(tmp_data.get('h323_online',0)),
                'rtc_online':int(tmp_data.get('rtc_online',0)),
                'xmpp_online':0,
                'monitor_online':0
            })

    ret_data['statistic'].sort(key=lambda x:x['statistic_time'])
    ret_data['total_count'] = len(ret_data['statistic'])
    # 数据截取
    ret_data['statistic'] = ret_data['statistic'][start:end_pos]
    # 时间格式转化
    for x in ret_data['statistic']:
        x['statistic_time'] = timestamp_to_iso_time(x['statistic_time'])
    return ret_data

'''
@description: 获取指定服务器的总的cpu使用率统计
@param  {str} p_server_moid  example: '992ce364-62ad-11ea-8dad-a4bf01519af2'    
@param  {str} start_time    example: '0000_20200316'
@param  {str} end_time      example: '2359_20200316'
@return: {json}
    example:
    {
        "success": 1,
        "physical": {
            "values": [],
            "time": [],
            "cpu": 2,
            "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
            "machine_room_name": "默认机房",
            "frame_type": "",
            "frame_moid": "",
            "frame_name": ""
        }
    }
'''
def get_p_server_cpu_statistic(p_server_moid, start_time, end_time):
    p_server_info = get_physical_server_info_api(p_server_moid)
    cpu_args = "target=nms.resource.%s.%s.cpu.cpuusage&noNullPoints=true&from=%s&until=%s&format=json" % (p_server_info['machine_room_moid'],p_server_moid, start_time, end_time)
    cpu_statistic = graphite_request(cpu_args)
    
    ret_data = {
        'success':1,
        'physical':{
            'machine_room_moid':p_server_info['machine_room_moid'],
            'machine_room_name':p_server_info['machine_room_name'],
            'frame_moid':p_server_info.get('frame_moid',''),
            'frame_name':p_server_info.get('frame_name',''),
            'frame_type':p_server_info.get('frame_type',''),
            'cpu':p_server_info.get('cpu'),
            'time':cpu_statistic['time'],
            'values':cpu_statistic['values']
        }
    }
    
    return ret_data

'''
@description: 获取指定服务器的mem使用率统计
@param  {str} p_server_moid  example: '992ce364-62ad-11ea-8dad-a4bf01519af2'    
@param  {str} start_time    example: '0000_20200316'
@param  {str} end_time      example: '2359_20200316'
@return: {json}
    example:
    {
        "physical": {
            "memory": 57,
            "frame_moid": "",
            "values": [],
            "machine_room_name": "默认机房",
            "memused": 18662968,
            "memtotal": 32660852,
            "machine_room_moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
            "time": [],
            "frame_name": "",
            "frame_type": ""
        },
        "success": 1
    }
'''
def get_p_server_mem_statistic(p_server_moid, start_time, end_time):
    p_server_info = get_physical_server_info_api(p_server_moid)
    cpu_args = "target=nms.resource.%s.%s.mem&noNullPoints=true&from=%s&until=%s&format=json" % (p_server_info['machine_room_moid'],p_server_moid, start_time, end_time)
    cpu_statistic = graphite_request(cpu_args)
    
    ret_data = {
        'success':1,
        'physical':{
            'machine_room_moid':p_server_info['machine_room_moid'],
            'machine_room_name':p_server_info['machine_room_name'],
            'frame_moid':p_server_info.get('frame_moid',''),
            'frame_name':p_server_info.get('frame_name',''),
            'frame_type':p_server_info.get('frame_type',''),
            'memory':p_server_info.get('memory',0),
            'memtotal':p_server_info.get('memtotal',0),
            'memused':p_server_info.get('memused',0),
            'time':cpu_statistic['time'],
            'values':cpu_statistic['values']
        }
    }
    
    return ret_data

'''
@description: 获取置顶服务器的usb状态
@param {str} p_server_moid_list     ','分隔
@return: 
{
  "success": 1,
  "physicals": [
    {
      "moid": "143c3c43-bd1a-4c7d-9e17-72a8c94ffb2b",
      "ip": "192.168.1.5",
      "usb_storage_exists": 1
    },
    {
      "moid": "2bb14171-9a5f-43e9-a09d-143a78fefffa",
      "ip": "192.168.1.6",
      "usb_storage_exists": 0
    }
  ]
}
'''
def get_physicals_usb_storage_state_api(p_server_moid_list):
    moid_list = p_server_moid_list.split(',')
    ret_data = {'success':1,'physicals':[]}
    for moid in moid_list:
        server_info = get_physical_server_info_api(moid)
        UsbWarnExists = ServerWarningUnrepaired.objects.filter(
            device_moid__exact=moid, code__exact=USB_STORAGE_EXISTS_WARNING_CODE).exists()
        ret_data['physicals'].append({
            'moid': moid,
            'ip': server_info.get('ip', ''),
            'usb_storage_exists': 0 if UsbWarnExists else 1
        })
    return ret_data



class MultiMeetingStatisticSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    class Meta:
        model = MultiMeetingStatistic  # 定义关联的 Model
        fields = ['start_time','end_time','info']  # 指定返回的 fields

class P2PMeetingStatisticSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    class Meta:
        model = P2PMeetingStatistic  # 定义关联的 Model
        fields = ['start_time','end_time','info']  # 指定返回的 fields

class EntityMeetingStatisticSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    class Meta:
        model = EntityMeetingStatistic  # 定义关联的 Model
        fields = ['start_time','end_time','info']  # 指定返回的 fields

def get_meeting_history_api(domain_moid, conf_type, start_time,end_time):
    user_domain_moid_list = get_user_domain_moid_list(domain_moid)
    ret_data = {'success':1,'meetings':[]}

    if conf_type == 'multi':
        meeting_obj = MultiMeetingStatistic.objects.filter(domain_moid__in = user_domain_moid_list,start_time__gte = start_time,start_time__lte = end_time )

        for x in MultiMeetingStatisticSerializer(meeting_obj, many=True).data:
            conf_info = json.loads(x['info'])
            # 转化为api需要的参数格式
            conf_info['confe164'] = conf_info.get('e164','')
            conf_info['multi'] = int(conf_info.get('scale',0))
            conf_info['bandwidth'] = int(conf_info.get('bandwidth',0))
            conf_info['start_time'] = x.get('start_time','').replace('-','/')
            conf_info['end_time'] = x.get('end_time','').replace('-','/')
            conf_info['stop_time'] = conf_info.get('stop_time','').replace('-','/')
            del conf_info['e164']
            del conf_info['scale']
            ret_data['meetings'].append(conf_info)
            
    elif conf_type == 'p2p':
        meeting_obj = P2PMeetingStatistic.objects.filter(domain_moid__in = user_domain_moid_list,start_time__gte = start_time,start_time__lte = end_time )

        for x in P2PMeetingStatisticSerializer(meeting_obj, many=True).data:
            conf_info = json.loads(x['info'])
            conf_info['start_time'] = x.get('start_time','').replace('-','/')
            conf_info['end_time'] = x.get('end_time','').replace('-','/')
            ret_data['meetings'].append(conf_info)
            
    elif conf_type == 'entity':
        meeting_obj = EntityMeetingStatistic.objects.filter(domain_moid__in = user_domain_moid_list,start_time__gte = start_time,start_time__lte = end_time )

        for x in EntityMeetingStatisticSerializer(meeting_obj, many=True).data:
            # 转化为api需要的参数格式
            conf_info = json.loads(x['info'])
            conf_info['name'] = conf_info.get('subject','')
            conf_info['start_time'] = x.get('start_time','')
            conf_info['end_time'] = x.get('end_time','')
            conf_info['regular_id'] = conf_info.get('regularId','')
            conf_info['organizer'] = conf_info.get('creator','')

            conf_info['organizer_moid'] = conf_info.get('organizerMoid','')
            conf_info['is_video_meeting'] = conf_info.get('isVideoMeeting','')
            conf_info['meeting_type'] = conf_info.get('meetingType','')
            conf_info['last_modify_time'] = conf_info.get('lastModifyTime','').replace('-','/')

            del conf_info['subject']
            del conf_info['startTime']
            del conf_info['endTime']
            del conf_info['regularId']
            del conf_info['creator']
            del conf_info['organizerMoid']
            del conf_info['isVideoMeeting']
            del conf_info['meetingType']
            del conf_info['lastModifyTime']          

            ret_data['meetings'].append(conf_info)
    
    return ret_data

class OldTerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldTerminal  # 定义关联的 Model
        fields = ('e164','type','version','ip','online')  # 指定返回的 fields

'''
@description: 获取非受管终端列表
@param {type} 
@return: 
{
    "success": 1,
    "old_terminal": [
        {
            "e164": "",
            "type": "22",
            "version": "22",
            "ip": "192.168.39.112",
            "online": "online"
        },
        {
            "e164": "",
            "type": "",
            "version": "",
            "ip": "172.16.0.3",
            "online": "offline"
        }
    ]
}
'''
def get_old_terminals_api():
    old_terminal_obj = OldTerminal.objects.all()
    ret_data = {'success': 1}

    terminal_list = OldTerminalSerializer(old_terminal_obj, many=True).data
    for info in terminal_list:
        info['e164'] = info['e164'] if info['e164'] is not None else ''
        info['type'] = info['type'] if info['type'] is not None else ''
        info['version'] = info['version'] if info['version'] is not None else ''
        info['online'] = 'online' if info['online'] == '1' else 'offline'

    ret_data['old_terminals'] = terminal_list 
    ret_data['total_count'] = len(terminal_list)
    return ret_data


'''
@description: 获取置顶ip的非受管终端的信息
@param {str}  terminal_ip
@return: 
{
    "e164": "",
    "success": 1,
    "type": "22",
    "online": "online",
    "version": "22"
}
'''
def get_old_terminal_detail(terminal_ip):
    old_terminal_obj = OldTerminal.objects.filter(ip__exact=terminal_ip).first()

    ret_data = {'success': 1}
    terminal_info = OldTerminalSerializer(old_terminal_obj).data

    ret_data['e164'] = terminal_info['e164'] if terminal_info['e164'] is not None else ''
    ret_data['type'] = terminal_info['type'] if terminal_info['type'] is not None else ''
    ret_data['version'] = terminal_info['version'] if terminal_info['version'] is not None else ''
    ret_data['online'] = 'online' if terminal_info['online'] == '1' else 'offline'
    
    return ret_data



class ServerUnrepairedWarningSerializerApi(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S+08:00")
    class Meta:
        model = ServerWarningUnrepaired  # 定义关联的 Model
        exclude = ('id','code','resolve_time')

'''
@description: 获取指定服务器的未修复告警
@param {type} 
@return: 
'''
def get_server_unrepaired_warning(server_moid):
    # try:
    warning_obj = ServerWarningUnrepaired.objects.filter(device_moid__exact=server_moid).order_by("-start_time")
    ser_data = ServerUnrepairedWarningSerializerApi(warning_obj, many=True)

    warning_list = ser_data.data
    if len(warning_list) > 0:
        domain_moid = get_machine_room_info_field(warning_list[0]["machine_room_moid"],"domain_moid")
        domain_name = get_domain_info_field(domain_moid,"name")

    for warning_info in warning_list:
        warning_info['device_name'] = warning_info['device_name'] if warning_info['device_name'] is not None else ''
        warning_info['machine_room_name'] = warning_info['machine_room_name'] if warning_info['machine_room_name'] is not None else ''
        warning_info['warning_level'] = warning_info['level']
        warning_info['domain_moid'] = domain_moid
        warning_info['domain_name'] = domain_name
        del warning_info['level']

    ret_data = {
        'success': 1,
        'unrepaired_warnings': warning_list
    }
    return ret_data
    # except:
    #     return {'success':0,'error_code':MYSQL_ERROR}


class TerminalUnrepairedWarningSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S+08:00")
    class Meta:
        model = TerminalWarningUnrepaired  # 定义关联的 Model
        # fields = '__all__'  # 指定返回的 fields
        exclude = ('id','code','resolve_time')

'''
@description: 获取指定终端的未修复告警
@param {type} 
@return: 
'''
def get_terminal_unrepaired_warning(dev_moid):
    try:
        warning_obj = TerminalWarningUnrepaired.objects.filter(device_moid__exact=dev_moid)
        ser_data = TerminalUnrepairedWarningSerializer(warning_obj, many=True)

        warning_list = ser_data.data
        for warning_info in warning_list:
            warning_info['device_name'] = warning_info['device_name'] if warning_info['device_name'] is not None else ''
            warning_info['domain_name'] = warning_info['domain_name'] if warning_info['domain_name'] is not None else ''
            warning_info['device_ip'] = warning_info['device_ip'] if warning_info['device_ip'] is not None else ''
            warning_info['warning_level'] = warning_info['level']
            del warning_info['level']

        ret_data = {
            'success': 1,
            'unrepaired_warnings': warning_list
        }
        return ret_data
    except:
        return {'success':0,'error_code':MYSQL_ERROR}

