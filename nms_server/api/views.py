from rest_framework.views import Response, Request
from nms_server.dao.redis.api import *
from nms_server.dao.redis.domain import get_domain_list,get_domain_list_by_Leaf
from nms_server.dao.redis.device import get_physical_server_info
from nms_server.dao.api import *
from nms_server.utils.error_code import *
from nms_server.utils.date_conversion import *
from rest_framework.views import APIView
from nms_server.settings import VERSION,API_LEVEL

from django.shortcuts import render

# Create your views here.
import logging
logger = logging.getLogger("nms." + __name__)

# Create your views here.

class Version(APIView):
    def get(self, request, *args, **kwargs):

        ret_data = {
            'success':1,
            'version':VERSION,
            'api_level':API_LEVEL
        }
        return Response(ret_data)

def get_user_info(sso_user):
    user_domain_moid = sso_user['data'].get('userDomainMoid', None)
    server_domain_moid = sso_user['data'].get('serviceDomainMoid', None)
    service_domain_admin = sso_user['data'].get('serviceDomainAdmin', False)
    default_service_domain_admin = sso_user['data'].get('defaultServiceDomainAdmin', False)
    
    if service_domain_admin or default_service_domain_admin or user_domain_moid is None:
        return {
            'user_type':'service',
            'domain_moid':server_domain_moid
        }
        
    else:
        return {
            'user_type':'user',
            'domain_moid':user_domain_moid
        }

class Domains(APIView):
    def get(self, request, *args, **kwargs):
        user_info = get_user_info(request.sso_user)
        logger.info('user_type:%s,domain_moid:%s',user_info['user_type'],user_info['domain_moid'])
        
        ret_data = {'success': 1}

        if user_info['user_type'] == 'user':
            # 用户域账户，获取本身、绑定机房、机房所属平台和所属服务域信息
            machine_room_moid = get_domain_info_field(user_info['domain_moid'],'machine_room_moid')
        
            domain_info = get_domain_info(user_info['domain_moid'])

            if machine_room_moid and domain_info:
                ret_data['domains'] = get_domain_list_by_Leaf(machine_room_moid,'')
                
                ret_data['domains'].append(domain_info)
            else:
                ret_data['sucess'] = 0
                ret_data['error_code'] = INPUT_ERROR

        else:    
            ret_data['domains'] = get_domain_list(user_info['domain_moid'])

        return Response(ret_data)

# 物理服务器列表
class Physicals(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        if domain_moid:
            ret_data = get_physical_server_list(domain_moid)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

class Logicals(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        if domain_moid:
            ret_data = get_logic_server_list(domain_moid)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

class Terminals(APIView):
    def get(self, request, domain_moid, **kwargs):
        start = request.GET.get('start', 0)
        count = request.GET.get('count', 10)
        logger.info("domain_moid:%s,start:%s,count:%s" ,domain_moid,start,count)

        ret_data = get_terminal_list(domain_moid,start,count)
        return Response(ret_data)

class LogicalsByPhysical(APIView):
    def get(self, request, p_server_moid, **kwargs):
        logger.info("p_server_moid:%s" ,p_server_moid)
        ret_data = get_physical_logic_server(p_server_moid)
        return Response(ret_data)

class PhysicalDetail(APIView):
    def get(self, request, p_server_moid, **kwargs):
        logger.info("p_server_moid:%s" ,p_server_moid)
        ret_data = get_physical_server_detail(p_server_moid)
        return Response(ret_data)

class OldTerminals(APIView):
    def get(self, request, *args, **kwargs):
        ret_data = get_old_terminals_api()
        return Response(ret_data)

class OldTerminalDetail(APIView):
    def get(self, request, terminal_ip, **kwargs):
        ret_data = get_old_terminal_detail(terminal_ip)
        return Response(ret_data)

class TerminalOnlineStatistic(APIView):
    def get(self, request, domain_moid, **kwargs):
        start = int(request.GET.get('start', 0))
        count = int(request.GET.get('count', 10))
        period = period_transform(request.GET.get('period', False))
        start_time = iso_time_format(request.GET.get('start_time', False))
        end_time = iso_time_format(request.GET.get('end_time', False))
        logger.info("domain_moid:%s,start:%d, count: %d, period:%s, start_time:%s,end_time:%s" ,domain_moid,start,count,period,start_time, end_time)

        if period or ( start_time and end_time):
            ret_data = get_terminal_online_statistic(domain_moid,  start, count, period, start_time, end_time)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.error("ret_data:%s", ret_data)
            return Response(ret_data)

class Meetings(APIView):
    def get(self, request, domain_moid, **kwargs):
        ret_data = get_meeting_info_list(domain_moid)
        return Response(ret_data)

class MeetingTerminalDetail(APIView):
    def get(self, request, conf_e164, **kwargs):
        ret_data = get_meeting_terminal_detail(conf_e164)
        return Response(ret_data) 

class DomainMediaResource(APIView):
    def get(self, request, domain_moid, **kwargs):
        ret_data = get_domain_media_resource_api(domain_moid)
        return Response(ret_data) 

class ServerMediaResource(APIView):
    def get(self, request, l_server_moid, **kwargs):
        ret_data = get_server_media_resource_api(l_server_moid)
        return Response(ret_data) 

class ServerWarningUnrepaired(APIView):
    def get(self, request, server_moid, **kwargs):
        ret_data = get_server_unrepaired_warning(server_moid)
        return Response(ret_data) 

class TerminalWarningUnrepaired(APIView):
    def get(self, request, terminal_moid, **kwargs):
        ret_data = get_terminal_unrepaired_warning(terminal_moid)
        return Response(ret_data) 