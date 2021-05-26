from nms_server.dao.mysql.warning import *
from nms_server.dao.redis.domain import get_machine_room_moid_list,get_user_domain_moid_list
from nms_server.utils.date_conversion import get_time
from nms_server.dao.mysql.system_set import SubWarningCode
from django.db.models import Q
from datetime import datetime
from django_redis import get_redis_connection
import itertools
import logging
import xlwt
import os


logger = logging.getLogger('nms.'+__name__)

def getPage( page ):
    if not page:
        page = 1
    else:
        page = int(page)

    start = (page - 1) * 10
    end = page * 10

    return start, end

# 订阅服务器告警信息数据列表接口
def get_server_sub_warning(userMoid, userDomainMoid, critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(parentMoid)
    logger.info("machine_room_list:%s"%machine_room_list)
    
    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 查出订阅的告警码
    sub_codes = []
    code_result = SubWarningCode.objects.filter(domain_moid=userDomainMoid, user_id=userMoid)
    for value in code_result:
        sub_codes.append(value.sub_code)

    logger.info("sub_codes=%s"%sub_codes)

    # 没有订阅任何告警或者每有选择任何告警级别，返回空
    if len(sub_codes) == 0 or len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result1_num = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]  
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
        else:
            if deviceName == '':
                result1_num = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
       
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result1_num = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
        
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
        else:
            if deviceName == '':
                result1_num = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
                result2_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()

                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
    
    result = itertools.chain(result1,result2)
    total_num = result1_num + result2_num
    
    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name, 
                             'device_type': warning.device_type,'device_ip': warning.device_ip, 
                             'machine_room_moid': warning.machine_room_moid,'machine_room_name': warning.machine_room_name, 
                             'code': warning.code, 'level': warning.level,'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})
    return warning_list, total_num

# 订阅终端告警信息数据列表接口
def get_terminal_sub_warning(userMoid, userDomainMoid, critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 查出订阅的告警码
    sub_codes = []
    code_result = SubWarningCode.objects.filter(domain_moid=userDomainMoid, user_id=userMoid)
    for value in code_result:
        sub_codes.append(value.sub_code)

    logger.info("sub_codes=%s"%sub_codes)

    # 没有订阅任何告警或者没有选任何告警级别，返回空
    if len(sub_codes) == 0 or len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result1_num = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]  
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else: 
                result1_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
        else:
            if deviceName == '':
                result1_num = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]  
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
   
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result1_num = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
       
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
        else:
            if deviceName == '':
                result1_num = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            
                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
            else:
                result1_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
                result2_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()

                # 未修复告警满一页，只返回未修复告警
                if result1_num > end:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                    result2 = []
                # 未修复告警数据为0，只返回已修复告警
                elif result1_num < start:
                    result1 = []
                    start = start - result1_num
                    end = end - result1_num
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                # 未修复告警不满一页，需要返回一部分未修复告警+一部分已修复告警
                else:
                    result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:result1_num]
                    result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[0:end-result1_num]
                
    result = itertools.chain(result1,result2)
    total_num = result1_num + result2_num

    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name, 
                             'device_type': warning.device_type, 'device_ip': warning.device_ip, 
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid, 
                             'domain_name': warning.domain_name, 'level': warning.level, 'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 'code': warning.code})
    return warning_list, total_num

# 未修复服务器告警信息数据列表接口
def get_server_unrepaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(parentMoid)
    logger.info("machine_room_list:%s"%machine_room_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")
    logger.info("warning_level_list:%s"%warning_level_list)

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()

    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type,'device_ip': warning.device_ip, 
                             'machine_room_moid': warning.machine_room_moid,'machine_room_name': warning.machine_room_name, 
                             'code': warning.code, 'level': warning.level,'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})
    return warning_list, warning_total_num


# 已修复服务器告警信息数据列表接口
def get_server_repaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime):

    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(parentMoid)
    logger.info("machine_room_list:%s"%machine_room_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")
    
    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).count()

    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip,
                             'machine_room_moid': warning.machine_room_moid, 'machine_room_name': warning.machine_room_name,
                             'code': warning.code, 'level': warning.level, 'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})
    return warning_list, warning_total_num

# 未修复终端告警信息数据列表接口
def get_terminal_unrepaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()

    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip,
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid,
                             'domain_name': warning.domain_name, 'level': warning.level,
                             'description': warning.description, 'start_time': warning.start_time,
                             'resolve_time': warning.resolve_time, 'code': warning.code})
    return warning_list, warning_total_num

# 已修复终端告警信息数据列表接口
def get_terminal_repaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
        else:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
                warning_total_num = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).count()

    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip,
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid,
                             'domain_name': warning.domain_name, 'level': warning.level,
                             'description': warning.description, 'start_time': warning.start_time,
                             'resolve_time': warning.resolve_time, 'code': warning.code})
    return warning_list, warning_total_num

# 非受管终端告警数据列表接口
def get_uncontroled_terminal_warning(critical, important, normal, deviceIp, page, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if len(warning_level_list) == 3:
        # 未修复
        unRepairedResult = OldTerminalWarningUnrepaired.objects.filter(device_ip=deviceIp, start_time__range=(startTime, stopTime)).order_by("-start_time")
        total_num_unrepaired = OldTerminalWarningUnrepaired.objects.filter(device_ip=deviceIp, start_time__range=(startTime, stopTime)).count()
        # 已修复
        repairedResult = OldTerminalWarningRepaired.objects.filter(device_ip=deviceIp, start_time__range=(startTime, stopTime)).order_by("-start_time")
        total_num_repaired = OldTerminalWarningRepaired.objects.filter(device_ip=deviceIp, start_time__range=(startTime, stopTime)).count()
    else:
        # 未修复
        unRepairedResult = OldTerminalWarningUnrepaired.objects.filter(device_ip=deviceIp, level__in=warning_level_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        total_num_unrepaired = OldTerminalWarningUnrepaired.objects.filter(device_ip=deviceIp, level__in=warning_level_list, start_time__range=(startTime, stopTime)).count()
        # 已修复
        repairedResult = OldTerminalWarningRepaired.objects.filter(device_ip=deviceIp, level__in=warning_level_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        total_num_repaired = OldTerminalWarningRepaired.objects.filter(device_ip=deviceIp, level__in=warning_level_list, start_time__range=(startTime, stopTime)).count()

    # 合并已修复和未修复终端告警QuerySet集
    result = unRepairedResult.union(repairedResult)[start:end]
    warning_total_num = total_num_unrepaired + total_num_repaired

    # 序列化
    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'id': warning.id, 'level': warning.level, 'description': warning.description,
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time})
    return warning_list, warning_total_num


# 受管终端详情此终端未修复告警列表接口
def get_terminal_detail_warning(critical, important, normal, page, deviceMoid, startTime, stopTime):
    
    # 获取查询页码
    start,end = getPage( page )
    logger.info("start:%s, end:%s"%(start,end))

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if len(warning_level_list) == 3:
        result = TerminalWarningUnrepaired.objects.filter(device_moid=deviceMoid, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
        warning_total_num = TerminalWarningUnrepaired.objects.filter(device_moid=deviceMoid, start_time__range=(startTime, stopTime)).count()
    else:
        result = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, device_moid=deviceMoid, start_time__range=(startTime, stopTime)).order_by("-start_time")[start:end]
        warning_total_num = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, device_moid=deviceMoid, start_time__range=(startTime, stopTime)).count()

    warning_list = []
    for warning in result:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({ 'level': warning.level, 'description': warning.description,
                              'start_time': warning.start_time, 'resolve_time': warning.resolve_time})
    return warning_list, warning_total_num

# 主界面未修复服务器告警信息数据列表
def get_server_unrepaired(userMoid,domainMoid):

    # 通过domainMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(domainMoid)
    logger.info("machine_room_list:%s"%machine_room_list)

    # 从数据库获取告警级别
    warning_level_list = []
    try:
        warning_notify_obj = WarningLevelForBaseInfo.objects.get(user_moid=userMoid, domain_moid=domainMoid)
        warning_level_list = warning_notify_obj.server_level.strip(',').split(',')
        logger.info("warning_level_list:%s"%warning_level_list)
    except Exception as e:
        logger.error(e)
        # 级别查询失败，默认就查询所有级别
        warning_level_list = ['critical','important','normal']

    if len(warning_level_list) == 0:
        return []

    if len(warning_level_list) == 3:
        server_unrepaired_warning = ServerWarningUnrepaired.objects.filter(machine_room_moid__in=machine_room_list).order_by("-start_time")[0:5]
    else:
        server_unrepaired_warning = ServerWarningUnrepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list).order_by("-start_time")[0:5]

    warning_list = []
    for warning in server_unrepaired_warning:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type,'device_ip': warning.device_ip, 
                             'machine_room_moid': warning.machine_room_moid,'machine_room_name': warning.machine_room_name, 
                             'code': warning.code, 'level': warning.level,'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})

    return warning_list

# 主界面未修复终端告警信息数据列表
def get_terminal_unrepaired(userMoid,domainMoid):

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(domainMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 从数据库获取告警级别
    warning_level_list = []
    try:
        warning_notify_obj = WarningLevelForBaseInfo.objects.get(user_moid=userMoid, domain_moid=domainMoid)
        warning_level_list = warning_notify_obj.terminal_level.strip(',').split(',')
    except Exception as e:
        logger.error(e)
        # 级别查询失败，默认就查询所有级别
        warning_level_list = ['critical','important','normal']

    if len(warning_level_list) == 0:
        return []

    if len(warning_level_list) == 3:
        terminal_unrepaired_warning = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list).order_by("-start_time")[0:5]

    else:
        terminal_unrepaired_warning = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list).order_by("-start_time")[0:5]

    warning_list = []
    for warning in terminal_unrepaired_warning:
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip, 
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid, 
                             'domain_name': warning.domain_name, 'level': warning.level, 
                             'description': warning.description, 'start_time': warning.start_time, 
                             'resolve_time': warning.resolve_time})
    return warning_list

def repair_server_warning(machineRoomMoid,deviceMoid,code):

    try:
        unRepairedWarning = ServerWarningUnrepaired.objects.get(machine_room_moid=machineRoomMoid,device_moid=deviceMoid,code=code)
        
        # 从未修复告警表删除这个告警
        ServerWarningUnrepaired.objects.get(machine_room_moid=machineRoomMoid,device_moid=deviceMoid,code=code).delete()

        # 把这个未修复告警添加到已修复告警
        now = datetime.now()
        resolve_time = now.strftime('%Y-%m-%d %H:%M:%S')

        repairedWarning = ServerWarningRepaired()
        repairedWarning.device_moid = unRepairedWarning.device_moid
        repairedWarning.device_name = unRepairedWarning.device_name
        repairedWarning.device_type = unRepairedWarning.device_type
        repairedWarning.device_ip = unRepairedWarning.device_ip
        repairedWarning.machine_room_moid = unRepairedWarning.machine_room_moid
        repairedWarning.machine_room_name = unRepairedWarning.machine_room_name
        repairedWarning.code = unRepairedWarning.code
        repairedWarning.level = unRepairedWarning.level
        repairedWarning.description = unRepairedWarning.description
        repairedWarning.start_time = unRepairedWarning.start_time
        repairedWarning.resolve_time = resolve_time
        repairedWarning.server_type = unRepairedWarning.server_type
        repairedWarning.save()


        # 手动修复告警后删除redis中的告警状态  使其节点服务器未修复告警和节点告警状态一致      
        try:
            connect = get_redis_connection()
            fileHandler = open('./nms_server/script/del_warning_unrepaired.lua')
            content = fileHandler.read()
            if unRepairedWarning.server_type == 0:
                server_type = 'p_server'
                connect.eval(content, 0, server_type,unRepairedWarning.device_moid,unRepairedWarning.code)
        except Exception as e:
            logger.error(e)
        
        return 1

    except Exception as e:
        logger.error(e)
        return 0

def repair_terminal_warning(domainMoid,deviceMoid,code):

    try:
        unRepairedWarning = TerminalWarningUnrepaired.objects.get(domain_moid=domainMoid,device_moid=deviceMoid,code=code)
        
        # 从未修复告警表删除这个告警
        TerminalWarningUnrepaired.objects.get(domain_moid=domainMoid,device_moid=deviceMoid,code=code).delete()

        # 把这个未修复告警添加到已修复告警
        now = datetime.now()
        resolve_time = now.strftime('%Y-%m-%d %H:%M:%S')
        
        repairedWarning = TerminalWarningRepaired()
        repairedWarning.device_moid = unRepairedWarning.device_moid
        repairedWarning.device_name = unRepairedWarning.device_name
        repairedWarning.device_type = unRepairedWarning.device_type
        repairedWarning.device_ip = unRepairedWarning.device_ip
        repairedWarning.domain_moid = unRepairedWarning.domain_moid
        repairedWarning.domain_name = unRepairedWarning.domain_name
        repairedWarning.code = unRepairedWarning.code
        repairedWarning.level = unRepairedWarning.level
        repairedWarning.description = unRepairedWarning.description
        repairedWarning.start_time = unRepairedWarning.start_time
        repairedWarning.resolve_time = resolve_time
        repairedWarning.save()

        return 1

    except Exception as e:
        logger.error(e)
        return 0

# 导出告警
def export_warning_info_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime, warningType, userDomainMoid, userMoid):
    try:
        template = {
            'warning': {
                'title': ('设备名称', '设备类型', '设备IP', '所属机房', '告警描述', '告警级别', '告警时间'),
                'field': ('device_name', 'device_type', 'device_ip', 'machine_room_name', 'description', 'level', 'start_time')
            },
        }
        if warningType == "sub_server_warning":
            warning_list = get_sub_server_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime, userDomainMoid, userMoid)
        elif warningType == "sub_terminal_warning":
            warning_list = get_sub_terminal_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime, userDomainMoid, userMoid)
        elif warningType == "unrepaired_server_warning":
            warning_list = get_unrepaired_server_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime)
        elif warningType == "unrepaired_terminal_warning":
            warning_list = get_unrepaired_terminal_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime)
        elif warningType == "repaired_server_warning":
            warning_list = get_repaired_server_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime)
        elif warningType == "repaired_terminal_warning":
            warning_list = get_repaired_terminal_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime)

        inspect_result = xlwt.Workbook(encoding='utf-8')

        sheet = inspect_result.add_sheet('warning')

        for c, name in enumerate(template['warning']['title']):
            sheet.write(0, c, name)
        for r, info in enumerate(warning_list):
            for c, name in enumerate(template['warning']['field']):
                value = info.get(name, '')
                sheet.write(r + 1, c, str(value))
        os.makedirs('/opt/data/nms_webserver/inspect', exist_ok=True)
        inspect_result.save(
            '/opt/data/nms_webserver/inspect/%s.xls' % parentMoid)
        return 1
    except Exception as e:
        logger.error(e)
        return 0

def get_sub_server_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime, userDomainMoid, userMoid):
    
    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(parentMoid)
    logger.info("machine_room_list:%s"%machine_room_list)
    
    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 查出订阅的告警码
    sub_codes = []
    code_result = SubWarningCode.objects.filter(domain_moid=userDomainMoid, user_id=userMoid)
    for value in code_result:
        sub_codes.append(value.sub_code)

    logger.info("sub_codes=%s"%sub_codes)

    # 没有订阅任何告警或者每有选择任何告警级别，返回空
    if len(sub_codes) == 0 or len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))    
            else:
                result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))     
        else:
            if deviceName == '':
                result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)) 
            else:
                result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))     
            else:
                result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))        
        else:
            if deviceName == '':
                result1 = ServerWarningUnrepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))         
            else:
                result1 = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))
                result2 = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),code__in=sub_codes, device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime))

    result = itertools.chain(result1,result2)
    
    warning_list = []
    for warning in result:
        if warning.level == 'critical':
            warning.level = '严重'
        elif warning.level == 'important':
            warning.level = '重要'
        elif warning.level == 'normal':
            warning.level = '一般'
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name, 
                             'device_type': warning.device_type,'device_ip': warning.device_ip, 
                             'machine_room_moid': warning.machine_room_moid,'machine_room_name': warning.machine_room_name, 
                             'code': warning.code, 'level': warning.level,'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})
    return warning_list

def get_sub_terminal_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime, userDomainMoid, userMoid):
    
    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 查出订阅的告警码
    sub_codes = []
    code_result = SubWarningCode.objects.filter(domain_moid=userDomainMoid, user_id=userMoid)
    for value in code_result:
        sub_codes.append(value.sub_code)

    logger.info("sub_codes=%s"%sub_codes)

    # 没有订阅任何告警或者没有选任何告警级别，返回空
    if len(sub_codes) == 0 or len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result1 = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))      
            else: 
                result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))       
        else:
            if deviceName == '':
                result1 = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))    
            else:
                result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))         
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result1 = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))      
            else:
                result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))      
        else:
            if deviceName == '':
                result1 = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))   
            else:
                result1 = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
                result2 = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime))
          
    result = itertools.chain(result1,result2)

    warning_list = []
    for warning in result:
        if warning.level == 'critical':
            warning.level = '严重'
        elif warning.level == 'important':
            warning.level = '重要'
        elif warning.level == 'normal':
            warning.level = '一般'
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name, 
                             'device_type': warning.device_type, 'device_ip': warning.device_ip, 
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid, 
                             'domain_name': warning.domain_name, 'level': warning.level, 'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 'code': warning.code})
    return warning_list

def get_unrepaired_server_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime):
    
    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(parentMoid)
    logger.info("machine_room_list:%s"%machine_room_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")
    logger.info("warning_level_list:%s"%warning_level_list)

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = ServerWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")

    warning_list = []
    for warning in result:
        if warning.level == 'critical':
            warning.level = '严重'
        elif warning.level == 'important':
            warning.level = '重要'
        elif warning.level == 'normal':
            warning.level = '一般'
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type,'device_ip': warning.device_ip, 
                             'machine_room_moid': warning.machine_room_moid,'machine_room_name': warning.machine_room_name, 
                             'code': warning.code, 'level': warning.level,'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})
    return warning_list

def get_unrepaired_terminal_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime):
    
    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = TerminalWarningUnrepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningUnrepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")

    warning_list = []
    for warning in result:
        if warning.level == 'critical':
            warning.level = '严重'
        elif warning.level == 'important':
            warning.level = '重要'
        elif warning.level == 'normal':
            warning.level = '一般'
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip,
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid,
                             'domain_name': warning.domain_name, 'level': warning.level,
                             'description': warning.description, 'start_time': warning.start_time,
                             'resolve_time': warning.resolve_time, 'code': warning.code})
    return warning_list

def get_repaired_server_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime):

    # 通过parentMoid获取域下的所有的机房Moid
    machine_room_list = get_machine_room_moid_list(parentMoid)
    logger.info("machine_room_list:%s"%machine_room_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")
    
    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = ServerWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = ServerWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_ip__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, machine_room_moid__in=machine_room_list, start_time__range=(startTime, stopTime)).order_by("-start_time")

    warning_list = []
    for warning in result:
        if warning.level == 'critical':
            warning.level = '严重'
        elif warning.level == 'important':
            warning.level = '重要'
        elif warning.level == 'normal':
            warning.level = '一般'
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip,
                             'machine_room_moid': warning.machine_room_moid, 'machine_room_name': warning.machine_room_name,
                             'code': warning.code, 'level': warning.level, 'description': warning.description, 
                             'start_time': warning.start_time, 'resolve_time': warning.resolve_time, 
                             'server_type': warning.server_type})
    return warning_list

def get_repaired_terminal_warning_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime):
    
    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 统计告警级别
    warning_level_list = []
    if critical == "true":
        warning_level_list.append("critical")
    if important == "true":
        warning_level_list.append("important")
    if normal == "true":
        warning_level_list.append("normal")

    # 没有选任何告警级别，返回空
    if len(warning_level_list) == 0:
        return [],0

    if deviceType == "all":
        if len(warning_level_list) == 3:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
    else:
        if len(warning_level_list) == 0:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
        else:
            if deviceName == '':
                result = TerminalWarningRepaired.objects.filter(device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")
            else:
                result = TerminalWarningRepaired.objects.filter(Q(device_name__icontains=deviceName)|Q(device_e164__icontains=deviceName),device_type=deviceType, level__in=warning_level_list, domain_moid__in=user_domain_moid_list, start_time__range=(startTime, stopTime)).order_by("-start_time")

    warning_list = []
    for warning in result:
        if warning.level == 'critical':
            warning.level = '严重'
        elif warning.level == 'important':
            warning.level = '重要'
        elif warning.level == 'normal':
            warning.level = '一般'
        warning.start_time = get_time(warning.start_time)
        warning.resolve_time = get_time(warning.resolve_time)
        warning_list.append({'device_moid': warning.device_moid, 'device_name': warning.device_name,
                             'device_type': warning.device_type, 'device_ip': warning.device_ip,
                             'device_e164': warning.device_e164, 'domain_moid': warning.domain_moid,
                             'domain_name': warning.domain_name, 'level': warning.level,
                             'description': warning.description, 'start_time': warning.start_time,
                             'resolve_time': warning.resolve_time, 'code': warning.code})
    return warning_list

# 获取终端告警状态（巡检剩余终端消息字段-告警状态）
def get_terminal_warning_status(deviceMoid, devType):
    result = TerminalWarningUnrepaired.objects.filter(device_moid=deviceMoid, device_type=devType)
    warning_list = []
    for warning in result:
        warning_list.append(warning.level)
        
    if len(warning_list) > 0:
        return warning_list[0]
    else:
        return ''