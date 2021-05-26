import logging
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from nms_server.dao.redis.statistic import get_meeting_resource
from nms_server.dao import statistic
from nms_server.utils import error_code

logger = logging.getLogger('nms.'+__name__)

# 以图片形式返回设备cpu使用率图片
class CpuChart(APIView):
    def get(self, request, *args, **kwargs):
        machineRoomMoid = request.GET.get('machineRoomMoid')
        if machineRoomMoid == None or machineRoomMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        logger.info("[CpuChart] machineRoomMoid : %s" % machineRoomMoid)
        logger.info("[CpuChart] deviceMoid : %s" % deviceMoid)
        logger.info("[CpuChart] startTime : %s" % startTime)
        logger.info("[CpuChart] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_cpu_chart(machineRoomMoid,deviceMoid,startTime,stopTime)
        return Response(response)

# 以图片形式返回设备内存使用率图片
class MemChart(APIView):
    def get(self, request, *args, **kwargs):
        machineRoomMoid = request.GET.get('machineRoomMoid')
        if machineRoomMoid == None or machineRoomMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        logger.info("[MemChart] machineRoomMoid : %s" % machineRoomMoid)
        logger.info("[MemChart] deviceMoid : %s" % deviceMoid)
        logger.info("[MemChart] startTime : %s" % startTime)
        logger.info("[MemChart] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_mem_chart(machineRoomMoid,deviceMoid,startTime,stopTime)
        return Response(response)

# 以图片形式返回设备的网卡使用率图片
class NetcardChart(APIView):
    def get(self, request, *args, **kwargs):
        machineRoomMoid = request.GET.get('machineRoomMoid')
        if machineRoomMoid == None or machineRoomMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        logger.info("[NetcardChart] machineRoomMoid : %s" % machineRoomMoid)
        logger.info("[NetcardChart] deviceMoid : %s" % deviceMoid)
        logger.info("[NetcardChart] startTime : %s" % startTime)
        logger.info("[NetcardChart] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_netcard_chart(machineRoomMoid,deviceMoid,startTime,stopTime)
        return Response(response)

# 会议质量
class MetingQuality(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userDomainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info("[MetingQuality] userDomainMoid : %s" % userDomainMoid)

        response = {'success': 1}
        response['data'] = statistic.get_meeting_quality(userDomainMoid)
        return Response(response)

# 会议资源
class MeetingResource(APIView):
    def get(self, request, *args, **kwargs):
        
        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[MeetingResource] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = get_meeting_resource(parentMoid)
        return Response(response)

# 预约会议
class AppointMeeting(APIView):
    def get(self, request, *args, **kwargs):

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[AppointMeeting] startTime : %s" % startTime)
        logger.info("[AppointMeeting] stopTime : %s" % stopTime)
        logger.info("[AppointMeeting] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['datapoints'] = statistic.get_appoint_meeting_statistic(parentMoid,startTime,stopTime)
        return Response(response)


class CpuUsage(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            parentMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info("[CpuUsage] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = statistic.get_cpuusage_statistic(parentMoid)
        return Response(response)

class MemUsage(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            parentMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info("[MemUsage] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = statistic.get_memusage_statistic(parentMoid)
        return Response(response)

class NetcardUp(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            parentMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info("[NetcardUp] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = statistic.get_netcardup_statistic(parentMoid)
        return Response(response)

class NetCardDown(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            parentMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info("[NetCardDown] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = statistic.get_netcarddown_statistic(parentMoid)
        return Response(response)

class WarningStatistic(APIView):
    def get(self, request, *args, **kwargs):

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[WarningStatistic] parentMoid : %s" % parentMoid)
        logger.info("[WarningStatistic] startTime : %s" % startTime)
        logger.info("[WarningStatistic] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_warning_statistic(parentMoid,startTime,stopTime)
        return Response(response)

class MeetingStatistic(APIView):
    def get(self, request, *args, **kwargs):

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[MeetingStatistic] parentMoid : %s" % parentMoid)
        logger.info("[MeetingStatistic] startTime : %s" % startTime)
        logger.info("[MeetingStatistic] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_meeting_statistic(parentMoid,startTime,stopTime)
        return Response(response)

class ServerStatistic(APIView):
    def get(self, request, *args, **kwargs):

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[ServerStatistic] parentMoid : %s" % parentMoid)
        logger.info("[ServerStatistic] startTime : %s" % startTime)
        logger.info("[ServerStatistic] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_server_statistic(parentMoid,startTime,stopTime)
        return Response(response)

class TerminalStatistic(APIView):
    def get(self, request, *args, **kwargs):

        startTime = request.GET.get('startTime')
        stopTime = request.GET.get('stopTime')
        if startTime == None or startTime == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if stopTime == None:
            stopTime = ''

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[TerminalStatistic] parentMoid : %s" % parentMoid)
        logger.info("[TerminalStatistic] startTime : %s" % startTime)
        logger.info("[TerminalStatistic] stopTime : %s" % stopTime)

        response = {'success': 1}
        response['data'] = statistic.get_terminal_statistic(parentMoid,startTime,stopTime)
        return Response(response)

class DiskAgeStatistic(APIView):
    def get(self, request, *args, **kwargs):

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[DiskAgeStatistic] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = statistic.get_disk_age_statistic(parentMoid)
        return Response(response)

class DiskUsageStatistic(APIView):
    def get(self, request, *args, **kwargs):

        parentMoid = request.GET.get('parentMoid')
        if parentMoid == None or parentMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if parentMoid == 'all':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info("[DiskUsageStatistic] parentMoid : %s" % parentMoid)

        response = {'success': 1}
        response['data'] = statistic.get_disk_usage_statistic(parentMoid)
        return Response(response)