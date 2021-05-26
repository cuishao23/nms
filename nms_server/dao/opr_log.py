from nms_server.dao.mysql.opr_log import Log
from nms_server.utils.date_conversion import get_time
import logging
from django.utils import timezone
import xlwt
import os
from nms_server.dao.redis import domain

logger = logging.getLogger("nms." + __name__)

# user
def get_opr_log(accountDomainMoid,userName, operateType, operateLevel, page, startTime, stopTime):
    if not page:
        page = 1
    else:
        page = int(page)
        
    start = (page - 1) * 10
    end = page * 10

    domain_moid_list = domain.get_domain_moid_list(accountDomainMoid)

    logger.info("domain_moid_list = %s" % domain_moid_list)

    if userName == "" and operateType == ".*" and operateLevel == ".*":
        result = Log.objects.filter(domain_moid__in=domain_moid_list,time__range=(startTime,stopTime)).order_by("-time")[start:end]
        total_num = Log.objects.filter(domain_moid__in=domain_moid_list,time__range=(startTime,stopTime)).count()
    else:
        type_list = Log.objects.values('type')
        level_list = Log.objects.values('level')

        operateTypeList = []
        if operateType == ".*":
            for value in type_list:
                operateTypeList.append(value["type"])
        else:
            operateTypeList.append(operateType)

        operateLevelList = []
        if operateLevel == ".*":
            for value in level_list:
                operateLevelList.append(value["level"])
        else:
            operateLevelList.append(operateLevel)
        
        if userName == "":
            result = Log.objects.filter(domain_moid__in=domain_moid_list,type__in=operateTypeList, level__in=operateLevelList, time__range=(startTime, stopTime)).order_by("-time")[start:end]

            logger.info("result = %s" % result)
            total_num = Log.objects.filter(domain_moid__in=domain_moid_list,type__in=operateTypeList, level__in=operateLevelList, time__range=(startTime, stopTime)).count()
        else:
            result = Log.objects.filter(user__icontains=userName,domain_moid__in=domain_moid_list,type__in=operateTypeList, level__in=operateLevelList, time__range=(startTime, stopTime)).order_by("-time")[start:end]
            total_num = Log.objects.filter(user__icontains=userName, domain_moid__in=domain_moid_list,type__in=operateTypeList, level__in=operateLevelList, time__range=(startTime, stopTime)).count()
            logger.info("result = %s" % result)

    log_list = []
    for value in result:
        value.time = get_time(value.time)
        log_list.append({'ip': value.ip, 'user': value.user, 'time': value.time, 'log_type': value.type, 'description': value.description, 'level': value.level, 'result': value.result, 'fail_reason': value.fail_reason})
    return log_list, total_num


def operate_log(detail):
    logger.info("detail = %s" % detail)
    create_time = timezone.now()
    logger.info("log_time = %s" % create_time)

    Log.objects.create(
            user=detail['user_name'],
            domain_moid=detail['domain_moid'],
            user_moid=detail['user_moid'],
            description=detail['description'],
            ip=detail['ip'],
            time=create_time,
            level=detail['level'],
            type=detail['type'],
            result=detail['result'] ,
            fail_reason=detail['reason'])

# 导出日志
def export_log_info_list(accountDomainMoid, userName, operateType, operateLevel, startTime, stopTime):
    try:
        template = {
            'log': {
                'title': ('用户名', '操作时间', 'IP地址', '操作类型', '操作描述', '操作等级', '操作结果', '失败原因'),
                'field': ('user', 'time', 'ip', 'log_type', 'description', 'level', 'result', 'fail_reason')
            },
        }

        log_list = get_log_list(accountDomainMoid,userName, operateType, operateLevel, startTime, stopTime)

        inspect_result = xlwt.Workbook(encoding='utf-8')

        sheet = inspect_result.add_sheet('log')

        for c, name in enumerate(template['log']['title']):
            sheet.write(0, c, name)
        for r, info in enumerate(log_list):
            for c, name in enumerate(template['log']['field']):
                value = info.get(name, '')
                sheet.write(r + 1, c, str(value))
        os.makedirs('/opt/data/nms_webserver/inspect', exist_ok=True)
        inspect_result.save(
            '/opt/data/nms_webserver/inspect/%s.xls' % startTime)
    except Exception as e:
        logger.error(e)

def get_log_list(accountDomainMoid,userName, operateType, operateLevel, startTime, stopTime):

    domain_moid_list = domain.get_domain_moid_list(accountDomainMoid)

    if userName == "" and operateType == ".*" and operateLevel == ".*":
        result = Log.objects.filter(domain_moid__in=domain_moid_list,time__range=(startTime,stopTime)).order_by("-time")
    else:
        type_list = Log.objects.values('type')
        level_list = Log.objects.values('level')

        operateTypeList = []
        if operateType == ".*":
            for value in type_list:
                operateTypeList.append(value["type"])
        else:
            operateTypeList.append(operateType)

        operateLevelList = []
        if operateLevel == ".*":
            for value in level_list:
                operateLevelList.append(value["level"])
        else:
            operateLevelList.append(operateLevel)
        
        if userName == "":
            result = Log.objects.filter(domain_moid__in=domain_moid_list,type__in=operateTypeList, level__in=operateLevelList, time__range=(startTime, stopTime)).order_by("-time")
        else:
            result = Log.objects.filter(domain_moid__in=domain_moid_list,user__icontains=userName, type__in=operateTypeList, level__in=operateLevelList, time__range=(startTime, stopTime)).order_by("-time")

    log_list = []
    for value in result:
        value.time = get_time(value.time)
        log_list.append({'ip': value.ip, 'user': value.user, 'time': value.time, 'log_type': value.type, 'description': value.description, 'level': value.level, 'result': value.result, 'fail_reason': value.fail_reason})
    return log_list