from nms_server.dao.mysql.device import OldTerminal
from nms_server.dao.redis.device import get_physical_server_list,get_terminal_list,get_terminal_detail_info
from nms_server.dao.redis.domain import get_user_domain_moid_list
from nms_server.dao.mysql.sus import DevVerInfo
from rest_framework import serializers
from django.db.models import Q
import logging
import xlwt
import os
logger = logging.getLogger("nms." + __name__)

def getPage( page ):
    if not page:
        page = 1
    else:
        page = int(page)

    start = (page - 1) * 10
    end = page * 10

    return start, end

def export_terminal_info_list(parentMoid,deviceName):
    try:
        template = {
            'terminal': {
                'title': ('设备名称', '设备IP', 'E164号码', '在线状态', '版本号'),
                'field': ('name', 'ip', 'e164', 'online', 'version')
            },
        }

        result = get_terminal_list(parentMoid,deviceName,'','')
        terminal_list = result['terminal']

        inspect_result = xlwt.Workbook(encoding='utf-8')

        sheet = inspect_result.add_sheet('terminal')

        for c, name in enumerate(template['terminal']['title']):
            sheet.write(0, c, name)
        for r, info in enumerate(terminal_list):
            for c, name in enumerate(template['terminal']['field']):
                value = info.get(name, '')
                sheet.write(r + 1, c, str(value))
        os.makedirs('/opt/data/nms_webserver/inspect', exist_ok=True)
        inspect_result.save(
            '/opt/data/nms_webserver/inspect/%s.xls' % parentMoid)
    except Exception as e:
        logger.error(e)

def get_physical_frame_info_list(parentMoid,deviceType,deviceName):
    result_list = get_physical_server_list(parentMoid)

    frame_result_list = []
    for server in result_list:
        if server['is_frame'] == '1':
            server['online'], server['ip'] = '---', '---'
            frame_result_list.append(server)
    
        elif server['belong_moid'] == '' and server['is_frame'] == '0':
            frame_result_list.append(server)
        else:
            pass
        
    logger.info('[get_physical_frame_info_list] result_list count:{}'.format(len(result_list)))
    logger.info('[get_physical_frame_info_list] frame_result_list count:{}'.format(len(frame_result_list)))

    # 筛选设备类型
    server_list1 = [] 
    if deviceType != 'all':
        for server in frame_result_list:
            if server['type_ser'] == deviceType:
                server_list1.append(server)
    else:
        server_list1 = frame_result_list
    logger.info('[get_physical_frame_info_list] server_list1 count:{}'.format(len(server_list1)))

    # 筛选设备名称
    server_list = []

    if deviceName != '':
        for server in server_list1:
            if deviceName in server['name'] or deviceName in server['ip']:
                server_list.append(server)
    else:
        server_list = server_list1

    logger.info('[get_physical_frame_info_list] server_list:{}'.format(server_list))
    logger.info('[get_physical_frame_info_list] server_list count:{}'.format(len(server_list)))

    return server_list


def get_physical_frame_info_detail(parentMoid, frameMoid):
    result_list = get_physical_server_list(parentMoid)
    logger.info('[get_physical_server_info_detail] result_list count:{}'.format(len(result_list)))
    #筛选机框moid
    server_list = []

    for server in result_list:
        if server['belong_moid'] == frameMoid:
            # server['belong_slot'] = '槽位' + server['belong_slot']
            server_list.append(server)
        elif server['moid'] == frameMoid and server['is_frame'] == '0':
            server_list.append(server)

    logger.info('[get_physical_server_info_detail] server_list:{}'.format(server_list))
    logger.info('[get_physical_server_info_detail] server_list count:{}'.format(len(server_list)))

    return server_list

def get_physical_server_info_list(parentMoid,deviceType,deviceName):
    result_list = get_physical_server_list(parentMoid)
    noframe_result_list = []
    for server in result_list:
        if server['is_frame'] == '0' and server['belong_moid'] != '':
            noframe_result_list.append(server)
        elif server['is_frame'] == '0' and server['belong_moid'] == '':
            noframe_result_list.append(server)
        else:
            pass
    logger.info('[get_physical_server_info_list] result_list count:{}'.format(len(result_list)))
    logger.info('[get_physical_server_info_list] frame_result_list count:{}'.format(len(noframe_result_list)))

    # 筛选设备类型
    server_list1 = []
    if deviceType != 'all':
        for server in noframe_result_list:

            if server['type_ser'] == deviceType:
                server_list1.append(server)
    else:
        server_list1 = noframe_result_list

    logger.info('[get_physical_server_info_list] server_list1 count:{}'.format(len(server_list1)))

    # 筛选设备名称
    server_list = []
    if deviceName != '':
        for server in server_list1:
            if deviceName in server['name'] or deviceName in server['ip']:
                server_list.append(server)
    else:
        server_list = server_list1

    logger.info('[get_physical_server_info_list] server_list:{}'.format(server_list))
    logger.info('[get_physical_server_info_list] server_list count:{}'.format(server_list))

    return server_list


def get_terminal_info_list(parentMoid,deviceName,page):
    # 分页
    start, end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    terminal_list = []
    total_count = 0

    try:
        result = get_terminal_list(parentMoid,deviceName,start,10)
        terminal_list = result['terminal']
        total_count = result['total_count']
    except Exception as e:
        logger.error(e)

    return terminal_list, total_count

def get_terminal_detail(deviceMoid):

    # 基本详情信息
    terminal_detail = get_terminal_detail_info(deviceMoid)

    for terminal in terminal_detail:

        # 补充是否推荐版本信息
        terminalVersion = terminal.get('version','')
        terminalVersion = terminalVersion.strip()
        terminalOem = terminal.get('oem','')
        terminalDomainMoid = terminal.get('domain_moid','')
        terminalE164 = terminal.get('e164','')
        terminalType =terminal.get('type_ver','')

        if terminalOem == '':
            terminalOem = 'kedacom'

        logger.info('[get_terminal_detail] terminalVersion:%s' % terminalVersion)
        logger.info('[get_terminal_detail] terminalType:%s' % terminalType)
        logger.info('[get_terminal_detail] terminalOem:%s' % terminalOem)
        logger.info('[get_terminal_detail] terminalDomainMoid:%s' % terminalDomainMoid)
        logger.info('[get_terminal_detail] terminalE164:%s' % terminalE164)

        if terminalOem != '' and terminalDomainMoid != '' and terminalE164 != '' and terminalType != '' and terminalVersion != '':
            version_list = DevVerInfo.objects.filter(oem_mark=terminalOem,device_type=terminalType,release_attribute__in=[2,4])
            logger.info('[get_terminal_detail] version list len : %s' % len(version_list))

            # 没有找到推荐版本
            # 那终端自己的版本就是推荐版本
            if len(version_list) == 0:
                logger.info('[get_terminal_detail] no version in mysql')
                terminal['recomand'] = 1
                terminal['recomand_version'] = terminalVersion
            else:
                for version in version_list:
                    if version.release_attribute == 4:
                        DomainMoidList = version.grayrange_moidlist
                        E164List = version.grayrange_e164list

                        if terminalDomainMoid in DomainMoidList or terminalE164 in E164List:
                            if terminalVersion == version.soft_ver:
                                terminal['recomand'] = 1
                                terminal['recomand_version'] = terminalVersion
                                break
                            else:
                                terminal['recomand'] = 0
                                terminal['recomand_version'] = version.soft_ver
                                break
                    else:
                        if terminalVersion == version.soft_ver:
                            terminal['recomand'] = 1
                            terminal['recomand_version'] = terminalVersion
                        else:
                            terminal['recomand'] = 0
                            terminal['recomand_version'] = version.soft_ver
        else:
            terminal['recomand'] = 0
            terminal['recomand_version'] = ''

    return terminal_detail

# 获取非受管终端信息列表
def get_uncontroled_terminal(parentMoid,page,deviceName):
    
    # 获取查询页码
    start,end = getPage(page)
    logger.info('start:%s,end:%s'%(start,end))

    # 通过parentMoid获取域下的所有用户域的Moid
    user_domain_moid_list = get_user_domain_moid_list(parentMoid)
    logger.info("user_domain_moid_list:%s"%user_domain_moid_list)

    # 分页查询
    if deviceName == '':
        result = OldTerminal.objects.filter(user_domain_moid__in=user_domain_moid_list)[start:end]
        total_num = OldTerminal.objects.filter(user_domain_moid__in=user_domain_moid_list).count()
    else:
        result = OldTerminal.objects.filter(Q(e164__icontains=deviceName)|Q(ip__icontains=deviceName),user_domain_moid__in=user_domain_moid_list)[start:end]
        total_num = OldTerminal.objects.filter(Q(e164__icontains=deviceName)|Q(ip__icontains=deviceName),user_domain_moid__in=user_domain_moid_list).count()

    # 序列化
    terminal_list = []
    for value in result:
        terminal_list.append({'id': value.id, 'user_domain_moid': value.user_domain_moid, 'moid': value.moid, 'type': value.type, 'name': value.name, 'e164': value.e164, 'ip': value.ip, 'online': value.online, 'version': value.version})
    return terminal_list, total_num

# 编辑非受管终端信息
def save_uncontroled_terminal(terminalID, terminalType, terminalE164, terminalVersion):
    
    terminal_info = OldTerminal.objects.get(id=terminalID)
    terminal_info.type = terminalType
    terminal_info.e164 = terminalE164
    terminal_info.version = terminalVersion
    terminal_info.save()

    return True
