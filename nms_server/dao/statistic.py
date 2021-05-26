# -*- coding: utf-8 -*-
from nms_server.dao.redis import statistic
from nms_server.dao.redis.domain import get_user_domain_moid_list,get_machine_room_moid_list
from nms_server.dao.redis.device import get_physical_server_info
from nms_server.dao.mysql.meeting import P2PMeetingStatistic, MultiMeetingStatistic
from datetime import datetime
from nms_server.settings import GRAPHITE, REQUESTS_TIMEOUT
from nms_server.utils.date_conversion import graphite_time
import json
import calendar
import logging
import requests
import base64

logger = logging.getLogger("nms." + __name__)

def graphite_request(graphite_args):
    ip = GRAPHITE['HOST']
    port = GRAPHITE['PORT']

    graphite_url = "http://"+ip+":"+port+"/render/?" + graphite_args
    logger.info("[graphite_request] graphite_url :%s" % graphite_url)

    # 向graphite请求数据
    response_data =  requests.get(graphite_url, timeout=REQUESTS_TIMEOUT)
    logger.info("[graphite_request] response_data.status_code :%s" % response_data.status_code)
    logger.info("[graphite_request] response_data.headers :%s" % response_data.headers)

    if response_data.status_code == 200:
        if response_data.headers.get('Content-Type','') == 'application/json':
            json_data = response_data.json()
            return json_data
        else:
            image_url = base64.b64encode(response_data.content)
            return image_url # 二进制内容
    else:
        logger.info("[graphite_request] graphite_args :%s" % graphite_args)
        logger.info("[graphite_request] status_code :%s" % response_data.status_code)
        return []


def get_cpu_chart(machineRoomMoid,deviceMoid,startTime,stopTime):
    cpuchart_args = "width=650&height=386&minyStep=1&vtitle=percent&yMin=0&yMax=100&hideLegend=true&target=aliasByMetric(nms.resource.%s.%s.cpu.*)&from=%s&until=%s" % (machineRoomMoid,deviceMoid,graphite_time(startTime,"from"),graphite_time(stopTime,"to"))
    cpuchart_data = graphite_request(cpuchart_args)
    return cpuchart_data

def get_mem_chart(machineRoomMoid,deviceMoid,startTime,stopTime):
    memchart_args = "width=650&height=386&minyStep=1&vtitle=percent&yMin=0&yMax=100&hideLegend=false&target=aliasByMetric(nms.resource.%s.%s.mem)&from=%s&until=%s" % (machineRoomMoid,deviceMoid,graphite_time(startTime,"from"),graphite_time(stopTime,"to"))
    memchart_data = graphite_request(memchart_args)
    return memchart_data

def get_netcard_chart(machineRoomMoid,deviceMoid,startTime,stopTime):
    netcardchart_args = "width=650&height=386&minyStep=1&vtitle=M&yMin=0&hideLegend=false&target=aliasByMetric(nms.resource.%s.%s.netcard.*)&target=aliasSub(nms.resource.%s.%s.netcard.*.*,'nms.resource.*.*.netcard.','')&from=%s&until=%s" % (machineRoomMoid,deviceMoid,machineRoomMoid,deviceMoid,graphite_time(startTime,"from"),graphite_time(stopTime,"to"))
    netcardchart_data = graphite_request(netcardchart_args)
    return netcardchart_data

def get_history_meeting_quality(parentMoid):
    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    Year  = datetime.now().year
    Month = datetime.now().month
    Day   = datetime.now().day
    DayStart = datetime(Year, Month, Day, 0, 0, 0)
    DayEnd= datetime(Year, Month, Day, 23, 59, 59)

    meeting_list = []
    try:
        # 筛选出今天的点对点历史数据
        result = P2PMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list,start_time__range=(DayStart, DayEnd))
        for value in result:
            info_value = json.loads(value.info)
            meeting_list.append({'conf_e164': value.caller_e164,'score': info_value['score']})

        # 筛选出今天的多点历史数据
        result = MultiMeetingStatistic.objects.filter(domain_moid__in=user_domain_moid_list,start_time__range=(DayStart, DayEnd))
        for value in result:
            info_value = json.loads(value.info)
            meeting_list.append({'conf_e164': value.conf_e164,'score': info_value['score']})

    except Exception as e:
        logger.error(e)
        meeting_list = []

    return meeting_list

# 今日会议质量
def get_meeting_quality(parentMoid):
    try:
        # 获取历史会议质量列表
        historyQualityList = get_history_meeting_quality(parentMoid)
        logger.info('history meeting quality list : %s' % historyQualityList)
        # 获取实时会议质量列表
        realQualityList = statistic.get_realtime_meeting_quality(parentMoid)
        logger.info('real time meeting quality list : %s' % realQualityList)

        realMeetingCount = len(realQualityList)
        historyMeetingCount = len(historyQualityList)

        goodQalityCount = 0
        betterQalityCount = 0
        normalQalityCount = 0
        worseQalityCount = 0

        for value in realQualityList:
            if value['quality'] == 5:
                goodQalityCount = goodQalityCount+1
            elif value['quality'] >= 4 and value['quality'] <= 4.5:
                betterQalityCount = betterQalityCount+1
            elif value['quality'] >= 3 and value['quality'] <= 3.5:
                normalQalityCount = normalQalityCount+1
            elif value['quality'] >= 0.5 and value['quality'] <= 2.5:
                worseQalityCount = worseQalityCount+1

        for value in historyQualityList:
            if value['score'] == 5:
                goodQalityCount = goodQalityCount+1
            elif value['score'] >= 4 and value['score'] <= 4.5:
                betterQalityCount = betterQalityCount+1
            elif value['score'] >= 3 and value['score'] <= 3.5:
                normalQalityCount = normalQalityCount+1
            elif value['score'] >= 0.5 and value['score'] <= 2.5:
                worseQalityCount = worseQalityCount+1

        meetingQality = {'realMeeting':realMeetingCount,
                         'historyMeeting':historyMeetingCount,
                         'goodQality':goodQalityCount,
                         'betterQality':betterQalityCount,
                         'normalQality':normalQalityCount,
                         'worseQality':worseQalityCount}

        logger.info('meeting quality : %s' % meetingQality)
        return meetingQality
    except Exception as e:
        logger.error(e)
        meetingQality = {'realMeeting':0,
                         'historyMeeting':0,
                         'goodQality':0,
                         'betterQality':0,
                         'normalQality':0,
                         'worseQality':0}
        return meetingQality

# 预约会议列表
def get_appoint_meeting_statistic(parentMoid,startTime,stopTime):
    meeting_statistic = []
    try:
        meeting_list = statistic.get_appoint_meeting_list(parentMoid)
        logger.info('appoint meeting list : %s' % meeting_list)

        filter_meeting_list = []

        DayStart = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
        DayEnd = datetime.strptime(stopTime, '%Y-%m-%d %H:%M:%S')
        # 最近一小时
        if str(DayEnd - DayStart) == "1:00:00":
            DayEnd = datetime(DayEnd.year, DayEnd.month, DayEnd.day, DayEnd.hour, DayEnd.minute, DayEnd.second)
        else:
            DayEnd = datetime(DayEnd.year, DayEnd.month, DayEnd.day, 23, 59, 59)

        logger.info('DayStart : %s' % DayStart)
        logger.info('DayEnd : %s' % DayEnd)
        # 筛选出满足条件的预约会议列表

        for meeting in meeting_list:
            if meeting.get('start_time','') != '':
                meetingStartTime = datetime.strptime(meeting['start_time'], '%Y-%m-%d %H:%M:%S')
                if meetingStartTime >= DayStart and meetingStartTime <= DayEnd:
                    filter_meeting_list.append({'start_time': meeting['start_time']})

        logger.info('filter meeting list : %s' % filter_meeting_list)
        
        Year  = DayStart.year
        Month = DayStart.month
        Day   = DayStart.day
        Hour  = DayStart.hour

        while Year <= DayEnd.year:
            while Month <= DayEnd.month:
                if Month == DayEnd.month:
                    DayCount = DayEnd.day
                else:
                    # 算出这个月有多少天
                    DayCount = calendar.monthrange(Year,Month)[1]

                while Day <= DayCount:
                    # 筛选框为最近一小时时
                    if str(DayEnd - DayStart) == "1:00:00":
                        if DayStart.minute == 0:
                            MinuteList = [0, 15, 30, 45]
                        elif DayStart.minute > 0 and DayStart.minute <= 15:
                            MinuteList = [15, 30, 45, 0]
                        elif DayStart.minute > 15 and DayStart.minute <= 30:
                            MinuteList = [30, 45, 0, 15]
                        elif DayStart.minute > 30 and DayStart.minute <= 59:
                            MinuteList = [45, 0, 15, 30]
                        change = 0
                        for Minute in MinuteList:
                            if change == 1:
                                meetingStart = datetime(DayEnd.year, DayEnd.month, DayEnd.day, DayEnd.hour, Minute)
                                meetingEnd = datetime(DayEnd.year, DayEnd.month, DayEnd.day, DayEnd.hour, Minute + 14)
                            else:
                                meetingStart = datetime(Year, Month, Day, Hour, Minute)
                                meetingEnd = datetime(Year, Month, Day, Hour, Minute + 14)
                            if Minute == 45:
                                change = 1

                            meetingCount = 0
                            for meeting in filter_meeting_list:
                                meetingTime = datetime.strptime(meeting['start_time'], '%Y-%m-%d %H:%M:%S')
                                if meetingTime >= meetingStart and meetingTime <= meetingEnd:
                                    meetingCount = meetingCount + 1

                            meeting_statistic.append([meetingCount, meetingStart.timestamp()])
                    else:
                        # 统计每个时间点的会议数量
                        while Hour <= 23:
                            # 每15分钟统计一次
                            if Hour == DayStart.hour and Day == DayStart.day and Month == DayStart.month:

                                    if DayStart.minute == 0:
                                        MinuteList = [0, 15, 30, 45]
                                    elif DayStart.minute > 0 and DayStart.minute <=15:
                                        MinuteList = [15, 30, 45]
                                    elif DayStart.minute > 15 and DayStart.minute <= 30:
                                        MinuteList = [30, 45]
                                    elif DayStart.minute > 30 and DayStart.minute <= 59:
                                        MinuteList = [45]

                                    for Minute in MinuteList:
                                        meetingStart = datetime(Year, Month, Day, Hour, Minute)
                                        meetingEnd = datetime(Year, Month, Day, Hour, Minute + 14)

                                        meetingCount = 0
                                        for meeting in filter_meeting_list:
                                            meetingTime = datetime.strptime(meeting['start_time'], '%Y-%m-%d %H:%M:%S')
                                            if meetingTime >= meetingStart and meetingTime <= meetingEnd:
                                                meetingCount = meetingCount + 1

                                        meeting_statistic.append([meetingCount, meetingStart.timestamp()])

                                        if Minute == 45 and Hour == 23:
                                            meeting_statistic.append([0, meetingEnd.timestamp()])
                            else:
                                for Minute in [0, 15, 30, 45]:
                                    meetingStart = datetime(Year, Month, Day, Hour, Minute)
                                    meetingEnd = datetime(Year, Month, Day, Hour, Minute+14)

                                    meetingCount = 0
                                    for meeting in filter_meeting_list:
                                        meetingTime = datetime.strptime(meeting['start_time'], '%Y-%m-%d %H:%M:%S')
                                        if meetingTime >= meetingStart and meetingTime <= meetingEnd:
                                            meetingCount = meetingCount+1

                                    meeting_statistic.append([meetingCount,meetingStart.timestamp()])

                                    if Minute == 45 and Hour == 23:
                                        meeting_statistic.append([0, meetingEnd.timestamp()])

                            # 统计下一个小时的预约会议数量
                            Hour = Hour+1

                    Day = Day+1
                    Hour = 0

                Month = Month+1
                Day = 1

            Year = Year+1
            Month = 1

        logger.info('meeting_statistic : %s' % meeting_statistic)

    except Exception as e:
        print(e)
        logger.error(e)
    return meeting_statistic

def get_cpuusage_statistic(parentMoid):
    machine_room_list = get_machine_room_moid_list(parentMoid)
    cpuusage_args = "target=highestCurrent(nms.resource.{%s}.*.cpu.cpuusage,5)&from=-62min&format=json&noNullPoints=true" % (','.join(machine_room_list))
    statistic_data = graphite_request(cpuusage_args)

    result_data = []
    for value in statistic_data:
        target = value['target']
        pServerMoid = target.split('.')[3]
        pServerInfo = get_physical_server_info(pServerMoid)
        result_data.append({'datapoints':value['datapoints'],'name':pServerInfo.get('name','')})

    return result_data

def get_memusage_statistic(parentMoid):
    machine_room_list = get_machine_room_moid_list(parentMoid)
    memusage_args = "target=highestCurrent(nms.resource.{%s}.*.mem,5)&from=-62min&format=json&noNullPoints=true" % (','.join(machine_room_list))
    statistic_data = graphite_request(memusage_args)

    result_data = []
    for value in statistic_data:
        target = value['target']
        pServerMoid = target.split('.')[3]
        pServerInfo = get_physical_server_info(pServerMoid)
        result_data.append({'datapoints':value['datapoints'],'name':pServerInfo.get('name','')})

    return result_data

def get_netcardup_statistic(parentMoid):
    machine_room_list = get_machine_room_moid_list(parentMoid)
    netcard_args = "target=highestCurrent(nms.resource.{%s}.*.netcard.up,5)&from=-62min&format=json&noNullPoints=true" % (','.join(machine_room_list))
    statistic_data = graphite_request(netcard_args)

    result_data = []
    for value in statistic_data:
        target = value['target']
        pServerMoid = target.split('.')[3]
        pServerInfo = get_physical_server_info(pServerMoid)
        for num in value['datapoints']:
            if num[0] != None and num[0] > 1:
                num[0] = int(num[0])
        result_data.append({'datapoints':value['datapoints'],'name':pServerInfo.get('name','')})

    return result_data

def get_netcarddown_statistic(parentMoid):
    machine_room_list = get_machine_room_moid_list(parentMoid)
    netcard_args = "target=highestCurrent(nms.resource.{%s}.*.netcard.down,5)&from=-62min&format=json&noNullPoints=true" % (','.join(machine_room_list))
    statistic_data = graphite_request(netcard_args)

    result_data = []
    for value in statistic_data:
        target = value['target']
        pServerMoid = target.split('.')[3]
        pServerInfo = get_physical_server_info(pServerMoid)
        for num in value['datapoints']:
            if num[0] != None and num[0] > 1:
                num[0] = int(num[0])
        result_data.append({'datapoints':value['datapoints'],'name':pServerInfo.get('name','')})

    return result_data

def get_warning_statistic(parentMoid,startTime,stopTime):
    machine_room_list = get_machine_room_moid_list(parentMoid)
    server_warning_args = "target=sumSeries(nms.warning.{%s}.server)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(machine_room_list),startTime,stopTime)
    server_warning_data = graphite_request(server_warning_args)

    user_domain_list = get_user_domain_moid_list(parentMoid)
    terminal_warning_args = "target=sumSeries(nms.warning.{%s}.terminal)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list),startTime,stopTime)
    terminal_warning_data = graphite_request(terminal_warning_args)

    result_data = {
            'server':server_warning_data,
            'terminal':terminal_warning_data
        }

    return result_data

def get_meeting_statistic(parentMoid,startTime,stopTime):
    user_domain_list = get_user_domain_moid_list(parentMoid)
    multi_meeting_args = "target=sumSeries(nms.meeting.{%s}.multi_count)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list),startTime,stopTime)
    multi_meeting_data = graphite_request(multi_meeting_args)

    p2p_meeting_args = "target=sumSeries(nms.meeting.{%s}.p2p_count)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list),startTime,stopTime)
    p2p_meeting_data = graphite_request(p2p_meeting_args)

    result_data = {
            'multi':multi_meeting_data,
            'p2p':p2p_meeting_data
        }

    return result_data

def get_server_statistic(parentMoid,startTime,stopTime):
    machine_room_list = get_machine_room_moid_list(parentMoid)
    online_count_args = "target=sumSeries(nms.device.{%s}.physical.online_count)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(machine_room_list),startTime,stopTime)
    online_count_data = graphite_request(online_count_args)

    offline_count_args = "target=sumSeries(nms.device.{%s}.physical.offline_count)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(machine_room_list),startTime,stopTime)
    offline_count_data = graphite_request(offline_count_args)

    result_data = {
            'online':online_count_data,
            'offline':offline_count_data
        }

    return result_data

def get_terminal_statistic(parentMoid,startTime,stopTime):
    user_domain_list = get_user_domain_moid_list(parentMoid)
    online_count_args = "target=sumSeries(nms.device.{%s}.terminal.online_count)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list),startTime,stopTime)
    online_count_data = graphite_request(online_count_args)

    offline_count_args = "target=sumSeries(nms.device.{%s}.terminal.offline_count)&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list), startTime, stopTime)
    offline_count_data = graphite_request(offline_count_args)

    allline_count_args = "target=sumSeries(nms.device.{%s}.terminal.{online_count,offline_count})&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list),startTime,stopTime)
    allline_count_data = graphite_request(allline_count_args)

    meetingline_count_args = "target=sumSeries(nms.meeting.{%s}.{multi_terminal_count,p2p_terminal_count})&from=%s&until=%s&format=json&noNullPoints=true" % (','.join(user_domain_list), startTime, stopTime)
    meetingline_count_data = graphite_request(meetingline_count_args)
    result_data = {
            'online':online_count_data,
            'offline': offline_count_data,
            'allline':allline_count_data,
            'meetingline': meetingline_count_data
        }

    return result_data

def get_disk_age_statistic(parentMoid):
    server_list = statistic.get_disk_age(parentMoid)
    logger.info('server_list : %s' % server_list)

    result_list = []
    for server in server_list:
        serverName = server.get('name','')
        diskCount =  int(server.get('disk_count',0))
        while diskCount > 0:
            diskNameKey = "disk%s_name" % diskCount
            diskName = server.get(diskNameKey,'')

            diskAgeKey = "disk%s_age" % diskCount
            diskAge = server.get(diskAgeKey,'0')
            if diskAge != '':
                diskAge = int(diskAge)
                Name = serverName + ":" + diskName

                if len(result_list) < 5:
                    result_list.append({"name":Name,"age":diskAge})
                else:
                    for result in result_list:
                        Age = int(result.get("age",0))
                        if Age < diskAge:
                            backName = result['name']
                            backAge = result['age']

                            result['name'] = Name
                            result['age'] = diskAge

                            Name = backName
                            diskAge = backAge

            diskCount = diskCount-1

    logger.info('disk age result : %s' % result_list)
    return result_list

def get_disk_usage_statistic(parentMoid):
    server_list = statistic.get_disk_usage(parentMoid)
    logger.info('server_list : %s' % server_list)

    result_list = []
    for server in server_list:
        serverName = server.get('name','')
        diskCount =  int(server.get('disk_count',0))
        while diskCount > 0:
            diskNameKey = "disk%s_name" % diskCount
            diskName = server.get(diskNameKey,'')

            diskTotalKey = "disk%s_total" % diskCount
            diskTotal = server.get(diskTotalKey,'0')

            diskUsedKey = "disk%s_used" % diskCount
            diskUsed = server.get(diskUsedKey,'0')

            diskUserateKey = "disk%s_userate" % diskCount
            diskUserate = server.get(diskUserateKey,'0')

            if diskTotal != '' and diskUsed != '' and diskUserate != '':
                diskTotal = int(diskTotal)
                diskUsed = int(diskUsed)
                diskUserate = int(diskUserate)
                Name = serverName + ":" + diskName

                if len(result_list) < 5:
                    result_list.append({"name":Name,"total":diskTotal,"used":diskUsed,"userate":diskUserate})
                else:
                    for result in result_list:
                        Userate = int(result.get("userate",0))
                        if Userate < diskUserate:
                            backName = result['name']
                            backTotal = result['total']
                            backUsed = result['used']
                            backUserate = result['userate']

                            result['name'] = Name
                            result['total'] = diskTotal
                            result['used'] = diskUsed
                            result['userate'] = diskUserate

                            Name = backName
                            diskTotal = backTotal
                            diskUsed = backUsed
                            diskUserate = backUserate

            diskCount = diskCount-1

    logger.info('disk usage result : %s' % result_list)
    return result_list