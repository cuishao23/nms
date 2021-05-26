import json
import xlwt
import os
import logging
from itertools import chain
from nms_server.dao.redis import inspect as redis_inspect, domain
from nms_server.dao.mysql.warning import ServerWarningUnrepaired, TerminalWarningUnrepaired
from nms_server.dao.mysql import inspection as inspect_model
from nms_server.utils.page import NmsPaginator

logger = logging.getLogger("nms." + __name__)


# 历史巡检数据查询
def get_inspect_license(taskid, page=1):
    paginator = NmsPaginator(
        inspect_model.InspectLicenseResult.objects.filter(
            taskid=taskid).order_by('id'),
        inspect_model.InspectLicenseResultSerializer)
    return {'license_list': paginator.get_data(page), 'max_page': paginator.get_max_page()}


def get_inspect_resource(taskid):
    try:
        r = inspect_model.InspectResourceResult.objects.get(
            taskid=taskid)
    except Exception:
        return
    return json.loads(r.resource_json)


def get_inspect_server(taskid, page=1):
    paginator = NmsPaginator(
        inspect_model.InspectServerResult.objects.filter(taskid=taskid).order_by('id'))
    return {'server_list': paginator.get_values(page), 'max_page': paginator.get_max_page()}


def get_inspect_server_resource(taskid, device_moid):
    try:
        r = inspect_model.InspectServerHwResult.objects.get(
            taskid=taskid, device_moid=device_moid)
        return json.loads(r.hw_json)
    except Exception:
        return


def get_inspect_terminal(taskid, page=1):
    paginator = NmsPaginator(
        inspect_model.InspectTerminalResult.objects.filter(taskid=taskid).order_by('id'))
    return {'terminal_list': paginator.get_values(page), 'max_page': paginator.get_max_page()}


def get_inspect_unrepaired_warning(taskid, device_moid, device_type='server', page=1):
    if device_type == 'server':
        object_list = inspect_model.InspectServerUnrepairedWarnning.objects.filter(
            taskid=taskid, device_moid=device_moid).order_by('id')
        serializer_class = inspect_model.InspectServerUnrepairedWarnningSerializer
    else:
        object_list = inspect_model.InspectTerminalUnrepairedWarnning.objects.filter(
            taskid=taskid, device_moid=device_moid).order_by('id')
        serializer_class = inspect_model.InspectTerminalUnrepairedWarnningSerializer
    paginator = NmsPaginator(object_list, serializer_class)
    return {'warning_list': paginator.get_data(page), 'max_page': paginator.get_max_page()}


def create_inspect_result(user_moid, taskid):
    template = {
        'license': {
            'title': ('授权许可ID', '文件状态', '所属服务域', '授权到期日期'),
            'field': ('auth_id', 'auth_status_display', 'service_domain_name', 'auth_dead_time')
        },
        '资源信息': {
            'title': ('资源信息',),
            'field': ('resource_json', )
        },
        '服务器状态': {
            'title': ('设备名称', '设备moid', '运行状态', '设备IP', '设备类型', '所属机房'),
            'field': ('device_name', 'device_moid', 'level_display', 'device_ip', 'device_type', 'machine_room_name')
        },
        '服务器资源': {
            'title': ('设备moid', '信息'),
            'field': ('device_moid', 'hw_json')
        },
        '服务器告警': {
            'title': ('设备moid', '告警等级', '告警描述', '授权到期日期告警时间'),
            'field': ('device_moid', 'level_display', 'description', 'start_time')
        },
        '终端状态': {
            'title': ('设备名称', '设备moid', '运行状态', 'E164号码', '设备IP', '所属用户域'),
            'field': ('device_name', 'device_moid', 'level_display', 'e164', 'device_ip', 'user_domain_name')
        },
        '终端告警': {
            'title': ('设备moid', '告警等级', '告警描述', '授权到期日期告警时间'),
            'field': ('device_moid', 'level_display', 'description', 'start_time')
        }
    }

    inspect_result = xlwt.Workbook(encoding='utf-8')

    def write_data(sheet_name, query_set):
        nonlocal inspect_result
        sheet = inspect_result.add_sheet(sheet_name)
        for c, name in enumerate(template[sheet_name]['title']):
            sheet.write(0, c, name)
        for r, info in enumerate(query_set):
            for c, name in enumerate(template[sheet_name]['field']):
                value = getattr(info, name, '')
                sheet.write(r+1, c, str(value))
    # license
    [write_data(*info) for info in (
        ('license', inspect_model.InspectLicenseResult.objects.filter(taskid=taskid)),
        ('资源信息', inspect_model.InspectResourceResult.objects.filter(taskid=taskid)),
        ('服务器状态', inspect_model.InspectServerResult.objects.filter(taskid=taskid)),
        ('服务器告警', inspect_model.InspectServerUnrepairedWarnning.objects.filter(
            taskid=taskid)),
        ('服务器资源', inspect_model.InspectServerHwResult.objects.filter(
            taskid=taskid)),
        ('终端状态', inspect_model.InspectTerminalResult.objects.filter(taskid=taskid)),
        ('终端告警', inspect_model.InspectTerminalUnrepairedWarnning.objects.filter(
            taskid=taskid)),
    )]

    os.makedirs('/opt/data/nms_webserver/inspect', exist_ok=True)
    inspect_result.save(
        '/opt/data/nms_webserver/inspect/%s.xls' % user_moid)


# 巡检任务相关设置和信息获取
def get_inspect_tasks(user_moid, page):
    import time
    '''
    获取定时巡检列表
    status: 0: 未开始, 1: 正在执行, 2: 已完成
    '''
    paginator = NmsPaginator(inspect_model.InspectTask.objects.filter(
        sub_task=0, task_flag=1, user_moid=user_moid).order_by('id'),
        inspect_model.InspectTaskSerializer
    )
    inspect_tasks = paginator.get_data(page)
    for data in inspect_tasks:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        data.status = 0 if now < data['start_time'] else 2
        if data['recycle']:
            try:
                recycle_obj = inspect_model.InspectRecycle.objects.get(
                    taskid=data['id'])
                data['recycle'] = inspect_model.InspectRecycleSerializer(
                    recycle_obj).data
                data['status'] = 1 if data['recycle']['end_time'] > now else 2
            except:
                data['recycle'] = {}
        data['inspect_range'] = get_inspect_range(data['id'])
    return {'max_page': paginator.get_max_page(), 'inspect_tasks': inspect_tasks}


def get_inspect_sub_task(taskid):
    '''
    获取子任务详情
    '''
    return inspect_model.InspectTask.objects.filter(parent_task=taskid).extra(select={"start_time": "DATE_FORMAT(start_time, '%%Y-%%m-%%d %%H:%%i:%%s')"}).values('id', 'start_time')


def get_inspect_range(taskid):
    '''
    获取巡检范围
    '''
    result = {}
    for info in inspect_model.InspectRange.objects.filter(taskid=taskid).values():
        result[info['inspect_type']] = info
        result[info['inspect_type']]['service_domain_name'] = '全部服务域' if info['service_domain_moid'] == 'all' else domain.get_domain_info_field(
            info['service_domain_moid'], 'name')
        result[info['inspect_type']]['platform_domain_name'] = '全部平台域' if info['platform_domain_moid'] == 'all' else domain.get_domain_info_field(
            info['platform_domain_moid'], 'name')
        result[info['inspect_type']]['user_domain_name'] = '全部用户域' if info['user_domain_moid'] == 'all' else domain.get_domain_info_field(
            info['user_domain_moid'], 'name')
        result[info['inspect_type']]['virtual_machine_room_name'] = '全部机房' if info['virtual_machine_room_moid'] == 'all' else domain.get_machine_room_info_field(
            info['virtual_machine_room_moid'], 'name')
    return result


def set_inspect_task(domain_moid, user_moid, start_time, inspect_ranges, inspect_recycle, flag, top_service_domain_moid, top_user_domain=''):
    task = inspect_model.InspectTask(
        domain_moid=domain_moid,
        user_moid=user_moid,
        start_time=start_time,
        license=1 if inspect_ranges.get('license') else 0,
        resource=1 if inspect_ranges.get('resource') else 0,
        server=1 if inspect_ranges.get('server') else 0,
        terminal=1 if inspect_ranges.get('terminal') else 0,
        recycle=1 if inspect_recycle else 0,
        executed=0,
        sub_task=0,
        task_flag=flag
    )
    task.save()

   # 巡检范围
    for inspect_type, inspect_range in inspect_ranges.items():
        service_domain_moid = inspect_range.get(
            'service_domain_moid', top_service_domain_moid)

        if top_user_domain:
            user_domain_moid = top_user_domain
            virtual_machine_room_moid = domain.get_domain_info(user_domain_moid)[
                'machine_room_moid']
        else:
            user_domain_moid = inspect_range.get('user_domain_moid', 'all')
            virtual_machine_room_moid = inspect_range.get(
                'virtual_machine_room_moid', 'all')
        inspect_model.InspectRange(
            taskid=task,
            inspect_type=inspect_type,
            service_domain_moid=top_service_domain_moid if service_domain_moid == 'all' else service_domain_moid,
            platform_domain_moid=inspect_range.get(
                'platform_domain_moid', 'all'),
            virtual_machine_room_moid=virtual_machine_room_moid,
            user_domain_moid=user_domain_moid
        ).save()

    # 巡检周期
    if inspect_recycle:
        inspect_model.InspectRecycle(taskid=task, **inspect_recycle).save()

    return task.id


def update_inspect_task(user_moid, taskid, inspect_ranges, inspect_recycle, top_service_domain_moid, start_time):
    task = inspect_model.InspectTask.objects.get(id=taskid)
    if task.user_moid == user_moid:
        task.license = 1 if inspect_ranges.get('license') else 0
        task.resource = 1 if inspect_ranges.get('resource') else 0
        task.server = 1 if inspect_ranges.get('server') else 0
        task.terminal = 1 if inspect_ranges.get('terminal') else 0
        task.recycle = 1 if inspect_recycle else 0
        task.start_time = start_time
        task.save()
        inspect_model.InspectRange.objects.filter(taskid=taskid).delete()
        inspect_model.InspectRecycle.objects.filter(taskid=taskid).delete()
        task = inspect_model.InspectTask.objects.get(id=taskid)
        for inspect_type, inspect_range in inspect_ranges.items():
            service_domain_moid = inspect_range.get(
                'service_domain_moid', top_service_domain_moid)
            inspect_model.InspectRange(
                taskid=task,
                inspect_type=inspect_type,
                service_domain_moid=top_service_domain_moid if service_domain_moid == 'all' else service_domain_moid,
                platform_domain_moid=inspect_range.get(
                    'platform_domain_moid', 'all'),
                virtual_machine_room_moid=inspect_range.get(
                    'virtual_machine_room_moid', 'all'),
                user_domain_moid=inspect_range.get('user_domain_moid', 'all')
            ).save()

        # 巡检周期
        if inspect_recycle:
            inspect_model.InspectRecycle(taskid=task, **inspect_recycle).save()


def del_inspect_task(taskid, user_moid):
    '''
    删除巡检任务
    '''
    task = inspect_model.InspectTask.objects.get(id=taskid)
    if task.user_moid == user_moid:
        sub_tasks = inspect_model.InspectTask.objects.filter(
            parent_task=taskid).values('id')
        for task_info in chain(sub_tasks, ({'id': taskid},)):
            # 清理巡检结果
            inspect_model.InspectLicenseResult.objects.filter(
                taskid=task_info['id']).delete()
            inspect_model.InspectResourceResult.objects.filter(
                taskid=task_info['id']).delete()
            inspect_model.InspectServerResult.objects.filter(
                taskid=task_info['id']).delete()
            inspect_model.InspectServerHwResult.objects.filter(
                taskid=task_info['id']).delete()
            inspect_model.InspectServerUnrepairedWarnning.objects.filter(
                taskid=task_info['id']).delete()
            inspect_model.InspectTerminalResult.objects.filter(
                taskid=task_info['id']).delete()
            inspect_model.InspectTerminalUnrepairedWarnning.objects.filter(
                taskid=task_info['id']).delete()
        inspect_model.InspectTask.objects.filter(parent_task=taskid).delete()
        inspect_model.InspectRange.objects.filter(taskid__id=taskid).delete()
        inspect_model.InspectRecycle.objects.filter(taskid__id=taskid).delete()
        inspect_model.InspectTask.objects.filter(id=taskid).delete()

def del_inspectchild_task(taskids, user_moid):
    '''
    删除巡检子任务
    '''
    for childtaskid in taskids:
        task = inspect_model.InspectTask.objects.get(id=childtaskid)
        if task.user_moid == user_moid:
            # 清理巡检结果
            inspect_model.InspectLicenseResult.objects.filter(
                taskid=childtaskid).delete()
            inspect_model.InspectResourceResult.objects.filter(
                taskid=childtaskid).delete()
            inspect_model.InspectServerResult.objects.filter(
                taskid=childtaskid).delete()
            inspect_model.InspectServerHwResult.objects.filter(
                taskid=childtaskid).delete()
            inspect_model.InspectServerUnrepairedWarnning.objects.filter(
                taskid=childtaskid).delete()
            inspect_model.InspectTerminalResult.objects.filter(
                taskid=childtaskid).delete()
            inspect_model.InspectTerminalUnrepairedWarnning.objects.filter(
                taskid=childtaskid).delete()
            # 清理当前巡检子任务   
            inspect_model.InspectTask.objects.filter(id=childtaskid).delete()    

def set_sub_inspect_task(taskid, start_time):
    task = inspect_model.InspectTask.objects.get(id=taskid)
    task.id = None
    task.start_time = start_time
    task.parent_task = taskid
    task.sub_task = 1
    task.save()
    return task.id


# 巡检数据转储
def inspect_license(taskid, domain_moid_list):
    instance_list = []
    for info in redis_inspect.get_license(domain_moid_list):
        instance_list.append(
            inspect_model.InspectLicenseResult(taskid=taskid, **info))
    inspect_model.InspectLicenseResult.objects.bulk_create(instance_list)


def inspect_resource(taskid, parent_domain_moid):
    data = redis_inspect.get_resource_info(parent_domain_moid)
    inspect_model.InspectResourceResult(
        taskid=taskid, resource_json=json.dumps(data)).save()


def inspect_server(taskid, machine_room_moid_list):
    instance_list = []
    for info in redis_inspect.get_server(machine_room_moid_list):
        instance_list.append(
            inspect_model.InspectServerResult(taskid=taskid, **info))
    inspect_model.InspectServerResult.objects.bulk_create(instance_list)


def inspect_server_resource(taskid, machine_room_moid_list):
    instance_list = []
    data = redis_inspect.get_server_hw_result(machine_room_moid_list)
    if data:
        for device_moid, json_data in data.items():
            instance_list.append(
                inspect_model.InspectServerHwResult(taskid=taskid, device_moid=device_moid, hw_json=json.dumps(json_data)))
        inspect_model.InspectServerHwResult.objects.bulk_create(instance_list)


def inspect_server_warning(taskid, machine_room_moid_list):
    instance_list = []
    for info in get_server_unrepaired_warning(machine_room_moid_list):
        instance_list.append(
            inspect_model.InspectServerUnrepairedWarnning(taskid=taskid, **info))
    inspect_model.InspectServerUnrepairedWarnning.objects.bulk_create(
        instance_list)


def inspect_terminal(taskid, domain_moid_list):
    instance_list = []
    for info in redis_inspect.get_terminal(domain_moid_list):
        instance_list.append(
            inspect_model.InspectTerminalResult(taskid=taskid, **info))
    inspect_model.InspectTerminalResult.objects.bulk_create(instance_list)


def inspect_terminal_warning(taskid, domain_moid_list):
    instance_list = []
    for info in get_terminal_unrepaired_warning(domain_moid_list):
        instance_list.append(
            inspect_model.InspectTerminalUnrepairedWarnning(taskid=taskid, **info))
    inspect_model.InspectTerminalUnrepairedWarnning.objects.bulk_create(
        instance_list)


def get_server_unrepaired_warning(machine_room_moid_list):
    return ServerWarningUnrepaired.objects.filter(machine_room_moid__in=machine_room_moid_list).values(
        'device_moid', 'code', 'level', 'description', 'start_time')


def get_terminal_unrepaired_warning(domain_moid_list):
    return TerminalWarningUnrepaired.objects.filter(domain_moid__in=domain_moid_list).values(
        'device_moid', 'code', 'level', 'description', 'start_time')
