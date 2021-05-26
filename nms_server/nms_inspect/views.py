import logging
import json
from django.http import FileResponse
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from nms_server.utils import error_code
from nms_server.dao import inspect
from nms_server.dao.redis import domain as dao_domain
from nms_server.rmq.producer import produce
from nms_server.utils.exception import NotLoginError

logger = logging.getLogger("nms." + __name__)


class InspectListView(APIView):
    def get(self, request):
        '''
        获取巡检列表
        '''
        user = getattr(request, 'sso_user', None)
        if user is not None:
            user_moid = user['data']['moid']
            data = inspect.get_inspect_tasks(
                user_moid, request.GET.get('page', 1))
            return Response({'success': 1, 'data': data})
        else:
            raise NotLoginError()

    @transaction.atomic
    def post(self, request):
        '''
        提交巡检计划
        post
        {
            "inspect_range": {
                "license": {
                    "service_domain_moid": "all"
                },
                "resource": {
                    "service_domain_moid": "all",
                    "platform_domain_moid": "all",
                    "virtual_machine_room_moid": "all"
                },
                "server": {
                    "service_domain_moid": "all",
                    "platform_domain_moid": "all",
                    "virtual_machine_room_moid": "all"
                },
                "terminal": {
                    "service_domain_moid": "all",
                    "user_domain_moid": "all"
                }
            },
            "inspect_recycle": {
                "end_time": "2020-05-01 12:00:00",
                "monday": 0,
                "tuesday": 1,
                "wednesday": 1,
                "thursday": 1,
                "friday": 1,
                "saturday": 1,
                "sunday": 1
            },
            "task_flag": 0,
            "start_time": "2020-04-08 13:51:00"
        }
        '''
        user = getattr(request, 'sso_user', None)
        data = request.data
        if user is not None:
            user_moid = user['data']['moid']
            service_domain_moid = user['data']['serviceDomainMoid']
            user_domain_moid = user['data'].get('userDomainMoid')

            logger.info("service_domain_moid=%s"%service_domain_moid)
            logger.info("user_domain_moid=%s"%user_domain_moid)

            domain_moid = user_domain_moid if user_domain_moid else service_domain_moid
            taskid = inspect.set_inspect_task(
                domain_moid,
                user_moid,
                data['start_time'],
                data['inspect_range'],
                data.get('inspect_recycle', None),
                data.get('task_flag', 0),
                service_domain_moid,
                user_domain_moid
            )
            if data.get('task_flag', 0) == 0:
                inspect_handler(
                    taskid, data['inspect_range'], user_domain_moid, service_domain_moid)
            else:
                # 定时巡检, 发送消息
                msg = {'eventid': 'add_inspect', 'taskid': taskid, 'domain_moid': domain_moid}
                produce("nms.webserver.ex", "nms.inspection.k",
                        "nms.inspection.q", msg)
            return Response({'success': 1, 'taskid': taskid})
        else:
            raise NotLoginError()


class InspectView(APIView):
    def get(self, request, taskid):
        data = inspect.get_inspect_sub_task(taskid)
        return Response({'success': 1, 'data': data})

    @transaction.atomic
    def post(self, request, taskid):
        inspect_range = inspect.get_inspect_range(taskid)
        sub_taskid = inspect.set_sub_inspect_task(
            taskid, request.data['start_time'])
            
        user_domain_moid = request.data['user_domain_moid']
        logger.info("user_domain_moid=%s"%user_domain_moid)

        inspect_handler(sub_taskid, inspect_range, user_domain_moid = user_domain_moid)
        return Response({'success': 1})

    @transaction.atomic
    def put(self, request, taskid):
        # 定时巡检, 发送消息
        user = getattr(request, 'sso_user', None)
        if user is not None:
            user_moid = user['data']['moid']
            service_domain_moid = user['data']['serviceDomainMoid']
            user_domain_moid = user['data'].get('userDomainMoid')
            domain_moid = user_domain_moid if user_domain_moid else service_domain_moid

            inspect.update_inspect_task(
                user_moid,
                taskid,
                request.data['inspect_range'],
                request.data.get('inspect_recycle', None),
                service_domain_moid,
                request.data.get('start_time', None))
            msg = {'eventid': 'update_inspect', 'taskid': taskid, 'domain_moid': domain_moid}
            produce("nms.webserver.ex", "nms.inspection.k",
                    "nms.inspection.q", msg)
            return Response({'success': 1})
        else:
            raise NotLoginError()

    @transaction.atomic
    def delete(self, request, taskid):
        # 定时巡检, 发送消息
        user = getattr(request, 'sso_user', None)
        if user is not None:
            user_moid = user['data']['moid']
            service_domain_moid = user['data']['serviceDomainMoid']
            user_domain_moid = user['data'].get('userDomainMoid')
            domain_moid = user_domain_moid if user_domain_moid else service_domain_moid

            inspect.del_inspect_task(taskid, user_moid)
            msg = {'eventid': 'del_inspect', 'taskid': taskid, 'domain_moid': domain_moid}
            produce("nms.webserver.ex", "nms.inspection.k",
                    "nms.inspection.q", msg)
            return Response({'success': 1})
        else:
            raise NotLoginError()


class DownloadView(APIView):
    def get(self, request):
        '''
        导出巡检结果
        '''
        user = getattr(request, 'sso_user', None)
        if user is not None:
            user_moid = user['data']['moid']
            inspect.create_inspect_result(user_moid, request.GET['taskid'])
            f = open('/opt/data/nms_webserver/inspect/%s.xls' %
                     user_moid, 'rb')
            response = FileResponse(f)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=inspect_result.xls'
            return response


class LicenseView(APIView):
    def get(self, request, taskid):
        '''
        查询license巡检结果
        '''
        return Response({'success': 1, 'data': inspect.get_inspect_license(taskid, request.GET.get('page', 1))})


class ResourceView(APIView):
    def get(self, request, taskid):
        '''
        查询资源巡检结果
        '''
        return Response({'success': 1, 'data': inspect.get_inspect_resource(taskid)})


class ServerView(APIView):
    def get(self, request, taskid):
        '''
        查询服务器巡检结果
        '''
        return Response({'success': 1, 'data': inspect.get_inspect_server(taskid, request.GET.get('page', 1))})


class ServerResourceView(APIView):
    def get(self, request, taskid, device_moid):
        '''
        查询服务器资源巡检结果
        '''
        return Response({'success': 1, 'data': inspect.get_inspect_server_resource(taskid, device_moid)})


class TerminalView(APIView):
    def get(self, request, taskid):
        '''
        查询终端巡检结果
        '''
        return Response({'success': 1, 'data': inspect.get_inspect_terminal(taskid, request.GET.get('page', 1))})


class UnrepairWarningView(APIView):
    def get(self, request, taskid, device_type, device_moid):
        '''
        查询未修复告警
        '''
        return Response({'success': 1, 'data': inspect.get_inspect_unrepaired_warning(
            taskid, device_moid, device_type, request.GET.get('page', 1))})

class DeleteInspectChildView(APIView):
    def post(self, request):
        '''
        删除定时巡检 子任务
        '''
        taskids = request.data
        logger.info('[DeleteInspectChildView] taskids:%s'%taskids)

        user = getattr(request, 'sso_user', None)
        if user is not None:
            user_moid = user['data']['moid']
            inspect.del_inspectchild_task(taskids, user_moid)
            return Response({'success': 1})
        else:
            raise NotLoginError()

def inspect_handler(taskid, inspect_range, user_domain_moid, service_domain_moid='-1'):
    # license
    if inspect_range.get('license'):
        parent_domain_moid = inspect_range['license']['service_domain_moid']
        parent_domain_moid = service_domain_moid if parent_domain_moid == 'all' else parent_domain_moid
        inspect.inspect_license(taskid, [
                                info['moid'] for info in dao_domain.get_service_domain_tree(parent_domain_moid)])
    # resource
    if inspect_range.get('resource'):
        parent_domain_moid = inspect_range['resource'].get(
            'virtual_machine_room_moid', 'all')
        if parent_domain_moid == 'all':
            parent_domain_moid = inspect_range['resource'].get(
                'platform_domain_moid', 'all')
        if parent_domain_moid == 'all':
            parent_domain_moid = inspect_range['resource'].get(
                'service_domain_moid', 'all')
            parent_domain_moid = service_domain_moid if parent_domain_moid == 'all' else parent_domain_moid
        if user_domain_moid != None:
            parent_domain_moid = user_domain_moid
        inspect.inspect_resource(taskid, parent_domain_moid)

    # server
    if inspect_range.get('server'):
        parent_domain_moid = inspect_range['server'].get(
            'virtual_machine_room_moid', 'all')
        if parent_domain_moid == 'all':
            parent_domain_moid = inspect_range['server'].get(
                'platform_domain_moid', 'all')
        if parent_domain_moid == 'all':
            parent_domain_moid = inspect_range['server'].get(
                'service_domain_moid', 'all')
            parent_domain_moid = service_domain_moid if parent_domain_moid == 'all' else parent_domain_moid
        machine_room_moid_list = dao_domain.get_machine_room_moid_list(
            parent_domain_moid)
        inspect.inspect_server(taskid, machine_room_moid_list)
        inspect.inspect_server_resource(taskid, machine_room_moid_list)
        inspect.inspect_server_warning(taskid, machine_room_moid_list)

    # terminal
    if inspect_range.get('terminal'):
        parent_domain_moid = inspect_range['terminal'].get(
            'user_domain_moid', 'all')
        if parent_domain_moid == 'all':
            parent_domain_moid = inspect_range['terminal'].get(
                'service_domain_moid', 'all')
            parent_domain_moid = service_domain_moid if parent_domain_moid == 'all' else parent_domain_moid
        if user_domain_moid == None:
            user_domain_moid_list = dao_domain.get_user_domain_moid_list(
                parent_domain_moid)
        else:
            user_domain_moid_list = []
            user_domain_moid_list.append(user_domain_moid)
        inspect.inspect_terminal(taskid, user_domain_moid_list)
        inspect.inspect_terminal_warning(taskid, user_domain_moid_list)
