from rest_framework.views import Response, Request
from nms_server.utils.date_conversion import graphite_time
from nms_server.dao.redis.api import *
from nms_server.dao.redis.domain import get_domain_list
from nms_server.dao.api import *
from nms_server.utils.error_code import *
from rest_framework.views import APIView
from django.shortcuts import render

# Create your views here.
import logging
logger = logging.getLogger("nms." + __name__)


# Create your views here.


class BmcTerminalType(APIView):
    def get(self, request, *args, **kwargs):
        ret_data = get_bmc_terminal_type()
        logger.info('ret_data:%s' % ret_data)
        return Response(ret_data)

# 媒体资源
class MediaResourceStatistic(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info('domain_moid %s',domain_moid)
        ret_data = get_media_vmr_api(domain_moid)
        return Response(ret_data)

# 服务器未修复告警
class UnrepairedWarning(APIView):
    def get(self, request, *args, **kwargs):
        count = request.GET.get('count', False)
        domain_moid = request.GET.get('moid', False)
        warning_level = request.GET.get('level', False)
        logger.info('count :%s, domain_moid:%s, warning_level:%s',count,domain_moid,warning_level)

        if count and count.isdigit() and domain_moid and warning_level:
            ret_data = get_top_unrepaired_warning(
                int(count), domain_moid, warning_level)
            return Response(ret_data)
        else:
            return Response({
                'success':0,
                'error_code':INPUT_ERROR
            })

# 会议数量统计
class MeetingStatistic(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("start_time:%s ,end_time : %s", start_time, end_time)
        if start_time and end_time:
            ret_data = get_meeting_count_statistic(domain_moid, graphite_time(
                start_time, 'from'), graphite_time(end_time, 'to'))
            return Response(ret_data)
        else:
            return Response({
                'success':0,
                'error_code':INPUT_ERROR
            })

# 入会终端统计
class TerminalStatistic(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("start_time:%s ,end_time : %s", start_time, end_time)
        if start_time and end_time:
            ret_data = get_meeting_terminal_statistic(domain_moid, graphite_time(
                start_time, 'from'), graphite_time(end_time, 'to'))

            return Response(ret_data)
        else:
            return Response({
                'success':0,
                'error_code':INPUT_ERROR
            })

# pas注册终端统计（sip，h323）
class TerminalOnlineStatistic(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("start_time:%s ,end_time : %s", start_time, end_time)
        if start_time and end_time:
            ret_data = get_pas_terminal_online_statistic(domain_moid, graphite_time(
                start_time, 'from'), graphite_time(end_time, 'to'))

            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

# 物理服务器列表
class Physicals(APIView):
    def get(self, request, *args, **kwargs):
        domain_moid = request.GET.get('moid', False)
        logger.info("moid:%s" % domain_moid)
        if domain_moid:
            ret_data = get_physical_server_list(domain_moid)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class PhysicalsResource(APIView):
    def get(self, request, *args, **kwargs):
        p_server_moid_list = request.GET.get('moid_list', False)
        logger.info("moid_list:%s" % type(p_server_moid_list))
        if p_server_moid_list:
            ret_data = get_physicals_res_api(p_server_moid_list)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

# 获取cpu使用率前n的物理服务器
class PhysicalsByCpu(APIView):
    def get(self, request, *args, **kwargs):
        domain_moid = request.GET.get('moid', False)
        count = request.GET.get('count', False)

        logger.info("moid:%s,count:%s",domain_moid,count)
        if count and count.isdigit() and domain_moid:
            ret_data = get_topn_physicals_by_cpu_api(domain_moid,int(count))
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class PhysicalsByMemory(APIView):
    def get(self, request, *args, **kwargs):
        domain_moid = request.GET.get('moid', False)
        count = request.GET.get('count', False)

        logger.info("moid:%s,count:%s",domain_moid,count)
        if count and count.isdigit() and domain_moid:
            ret_data = get_topn_physicals_by_mem_api(domain_moid,int(count))
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class PhysicalCpuHistory(APIView):
    def get(self, request, p_server_moid, **kwargs):
        logger.info("p_server_moid:%s" % p_server_moid)
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("start_time:%s ,end_time : %s", start_time, end_time)
        if start_time and end_time:
            ret_data = get_p_server_cpu_statistic(p_server_moid, graphite_time(
                start_time, 'from'), graphite_time(end_time, 'to'))

            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class PhysicalMemoryHistory(APIView):
    def get(self, request, p_server_moid, **kwargs):
        logger.info("p_server_moid:%s" % p_server_moid)
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("start_time:%s ,end_time : %s", start_time, end_time)
        if start_time and end_time:
            ret_data = get_p_server_mem_statistic(p_server_moid, graphite_time(
                start_time, 'from'), graphite_time(end_time, 'to'))

            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

class physicalsUsbStorageState(APIView):
    def get(self, request, *args, **kwargs):
        p_server_moid_list = request.GET.get('moid_list', False)
        logger.info("moid_list:%s" % p_server_moid_list)
        if p_server_moid_list:
            ret_data = get_physicals_usb_storage_state_api(p_server_moid_list)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class Domains(APIView):
    def get(self, request, *args, **kwargs):
        domain_moid = request.GET.get('moid', False)
        logger.info("domain_moid:%s" % domain_moid)
        if domain_moid:
            ret_data = {
            'success':1,
            'domains':  get_domain_list(domain_moid)
            }
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

class Lives(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        ret_data = get_live_list_api(domain_moid)
        return Response(ret_data)


class AppointmentMeetings(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        ret_data = get_appointment_list_api(domain_moid)
        return Response(ret_data)        


class AppointmentMeetingStatistic(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("start_time:%s ,end_time : %s", start_time, end_time)
        if start_time and end_time:

            ret_data = get_appointment_future_api(domain_moid, start_time, end_time)
            return Response(ret_data)
        else:
            ret_data = {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class Meetings(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        conf_type = request.GET.get('conf_type', False)
        count = request.GET.get('count', False)
        logger.info("conf_type:%s ,count : %s", conf_type, count)
        if conf_type and count and count.isdigit():
            ret_data = get_domain_meetings_api(domain_moid, conf_type, int(count))
            return Response(ret_data)
        else:
            ret_data= {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)


class HistoryMeetings(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        conf_type = request.GET.get('conf_type', 'multi')
        start_time = request.GET.get('start_time', False)
        end_time = request.GET.get('end_time', False)
        logger.info("conf_type:%s ,start_time : %s, end_time : %s", conf_type, start_time, end_time)
        if conf_type and start_time and end_time:
            ret_data = get_meeting_history_api(domain_moid, conf_type, start_time.replace('/','-'),end_time.replace('/','-'))
            return Response(ret_data)
        else:
            ret_data= {'success':0,'error_code':INPUT_ERROR}
            logger.info("ret_data:%s", ret_data)
            return Response(ret_data)

class Aplives(APIView):
    def get(self, request, domain_moid, **kwargs):
        logger.info("domain_moid:%s" % domain_moid)
        ret_data = get_aplive_list_api(domain_moid)
        return Response(ret_data)
        
class TerminalDiagnosis(APIView):
    def get(self, request, terminal_moid, terminal_type, **kwargs):
        logger.info("terminal_moid:%s, terminal_type:%s", terminal_moid,terminal_type)
        ret_data = get_terminal_hardwarestate_api(terminal_moid,terminal_type)
        return Response(ret_data)


class TerminalDetail(APIView):
    def get(self, request, param_type, param_value, **kwargs):
        ret_data = get_terminal_meeting_detail_api(param_type, param_value)
        return Response(ret_data)
