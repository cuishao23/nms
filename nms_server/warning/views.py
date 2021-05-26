import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from nms_server.dao import warning
from django.http import FileResponse, HttpResponse

logger = logging.getLogger('nms.'+__name__)

# 订阅服务器告警信息数据列表
class ServerWarningSubList(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
            userDomainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        if parentMoid == None or parentMoid == '':
            parentMoid = userDomainMoid

        logger.info('[ServerWarningSubList] critical:%s, important:%s, normal:%s' % (critical, important, normal))
        logger.info('[ServerWarningSubList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName, deviceType,parentMoid))
        logger.info('[ServerWarningSubList] userMoid:%s, userDomainMoid:%s' % (userMoid,userDomainMoid))
        logger.info('[ServerWarningSubList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, total_num = warning.get_server_sub_warning(userMoid, userDomainMoid, critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime)
        logger.info('[ServerWarningSubList] warning_total_num:%s'%total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = total_num
        return Response(response)

# 订阅终端告警信息数据列表
class TerminalWarningSubList(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
            userDomainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        if parentMoid == None or parentMoid == '':
            parentMoid = userDomainMoid

        logger.info('[TerminalWarningSubList] critical:%s, important:%s, normal:%s' % (critical, important, normal))
        logger.info('[TerminalWarningSubList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName, deviceType,parentMoid))
        logger.info('[TerminalWarningSubList] userMoid:%s,userDomainMoid:%s' % (userMoid,userDomainMoid))
        logger.info('[TerminalWarningSubList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, total_num = warning.get_terminal_sub_warning(userMoid, userDomainMoid, critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime)
        logger.info('[TerminalWarningSubList] warning_total_num:%s'%total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = total_num
        return Response(response)

# 未修复服务器告警信息数据列表
class ServerWarningUnrepairedList(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid','')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[ServerWarningUnrepairedList] critical:%s, important:%s, normal:%s' % (critical, important, normal))
        logger.info('[ServerWarningUnrepairedList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName, deviceType,parentMoid))
        logger.info('[ServerWarningUnrepairedList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, warning_total_num = warning.get_server_unrepaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime)
        logger.info('[ServerWarningUnrepairedList] warning_total_num:%s'%warning_total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = warning_total_num
        return Response(response)

# 已修复服务器告警信息数据列表
class ServerWarningRepairedList(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[ServerWarningRepairedList] critical:%s, important:%s, normal:%s' % (critical,important,normal))
        logger.info('[ServerWarningRepairedList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName,deviceType,parentMoid))
        logger.info('[ServerWarningRepairedList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, warning_total_num = warning.get_server_repaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime)
        logger.info('[ServerWarningRepairedList] warning_total_num:%s'%warning_total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = warning_total_num
        return Response(response)

# 未修复终端告警信息数据列表
class TerminalWarningUnrepairedList(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[TerminalWarningUnrepairedList] critical:%s, important:%s, normal:%s' % (critical,important,normal))
        logger.info('[TerminalWarningUnrepairedList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName,deviceType,parentMoid))
        logger.info('[TerminalWarningUnrepairedList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, warning_total_num = warning.get_terminal_unrepaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime)
        logger.info('[TerminalWarningUnrepairedList] warning_total_num:%s'%warning_total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = warning_total_num
        return Response(response)

# 已修复终端告警信息数据列表
class TerminalWarningRepairedList(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[TerminalWarningRepairedList] critical:%s, important:%s, normal:%s' % (critical,important,normal))
        logger.info('[TerminalWarningRepairedList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName,deviceType,parentMoid))
        logger.info('[TerminalWarningRepairedList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, warning_total_num = warning.get_terminal_repaired_warning(critical, important, normal, deviceName, deviceType, page, parentMoid, startTime, stopTime)
        logger.info('[TerminalWarningRepairedList] warning_total_num:%s'%warning_total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = warning_total_num
        return Response(response)

# 非受管终端告警数据列表
class unControledTerminalWarningList(APIView):
    def get(self, request):
        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceIp = request.GET.get('deviceIp')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        logger.info('[UnControledTerminalWarning] critical:%s, important:%s, normal:%s, deviceIp:%s' % (critical,important,normal,deviceIp))
        logger.info('[UnControledTerminalWarning] startTime:%s, stopTime:%s' % (startTime,stopTime))

        warning_list, warning_total_num = warning.get_uncontroled_terminal_warning(critical, important, normal, deviceIp, page, startTime, stopTime)
        logger.info('[UnControledTerminalWarning] warning_total_num:%s'%warning_total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = warning_total_num
        return Response(response)

# 受管终端详情此终端未修复告警列表
class TerminalDetailWarning(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")

        logger.info('[TerminalDetailWarning] critical:%s, important:%s, normal:%s, deviceMoid:%s' % (critical,important,normal,deviceMoid))
        logger.info('[TerminalDetailWarning] startTime:%s, stopTime:%s' % (startTime,stopTime))
        
        warning_list, warning_total_num = warning.get_terminal_detail_warning(critical, important, normal, page, deviceMoid, startTime, stopTime)
        logger.info('[TerminalDetailWarning] warning_total_num:%s'%warning_total_num)

        response = {'success': 1}
        response['data'] = warning_list
        response['total_num'] = warning_total_num
        return Response(response)

# 主界面未修复服务器告警信息数据列表
class ServerWarningUnrepaired(APIView):
    def get(self, request, *args, **kwargs):

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
            domainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[ServerWarningUnrepaired] userMoid:%s, domainMoid:%s' % (userMoid,domainMoid))
        
        server_warning_list = warning.get_server_unrepaired(userMoid,domainMoid)
        logger.info('[ServerWarningUnrepaired] warning_total_num:%s'%len(server_warning_list))

        response = {'success': 1}
        response['data'] = server_warning_list
        return Response(response)

# 主界面未修复终端告警信息数据列表
class TerminalWarningUnrepaired(APIView):
    def get(self, request, *args, **kwargs):
        
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
            domainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[TerminalWarningUnrepaired] userMoid:%s,domainMoid:%s' % (userMoid,domainMoid))
        terminal_warning_list = warning.get_terminal_unrepaired(userMoid,domainMoid)
        logger.info('[TerminalWarningUnrepaired] warning_total_num:%s'%len(terminal_warning_list))

        response = {'success': 1}
        response['data'] = terminal_warning_list
        return Response(response)

# 修复服务器告警
class RepairServerWarning(APIView):
    def get(self, request, *args, **kwargs):
        
        machineRoomMoid = request.GET.get('machineRoomMoid')
        deviceMoid = request.GET.get('deviceMoid')
        code = request.GET.get('code')

        logger.info('[RepairServerWarning] machineRoomMoid:%s' % machineRoomMoid)
        logger.info('[RepairServerWarning] deviceMoid:%s' % deviceMoid)
        logger.info('[RepairServerWarning] code:%s' % code)

        result = warning.repair_server_warning(machineRoomMoid,deviceMoid,code)
        if result == 1:
            return Response({'success': 1})
        else:
            return Response({'success': 0})

# 修复终端告警
class RepairTerminalWarning(APIView):
    def get(self, request, *args, **kwargs):
        
        domainMoid = request.GET.get('domainMoid')
        deviceMoid = request.GET.get('deviceMoid')
        code = request.GET.get('code')

        logger.info('[RepairTerminalWarning] domainMoid:%s' % domainMoid)
        logger.info('[RepairTerminalWarning] deviceMoid:%s' % deviceMoid)
        logger.info('[RepairTerminalWarning] code:%s' % code)

        result = warning.repair_terminal_warning(domainMoid,deviceMoid,code)
        if result == 1:
            return Response({'success': 1})
        else:
            return Response({'success': 0})

# 导出告警
class DownloadWarning(APIView):
    def get(self, request, *args, **kwargs):
        critical = request.GET.get('critical')
        important = request.GET.get('important')
        normal = request.GET.get('normal')
        deviceName = request.GET.get('deviceName')
        deviceType = request.GET.get('deviceType')
        parentMoid = request.GET.get('parentMoid')
        startTime = request.GET.get('starttime')
        startTime = startTime.replace("+ ", " ")
        stopTime = request.GET.get('stoptime')
        stopTime = stopTime.replace("+ ", " ")
        warningType = request.GET.get('warningType')

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
                userMoid = user['data']['moid']
                userDomainMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[ServerWarningRepairedList] critical:%s, important:%s, normal:%s' % (critical,important,normal))
        logger.info('[ServerWarningRepairedList] deviceName:%s, deviceType:%s, parentMoid:%s' % (deviceName,deviceType,parentMoid))
        logger.info('[ServerWarningRepairedList] startTime:%s, stopTime:%s' % (startTime,stopTime))

        result = warning.export_warning_info_list(critical, important, normal, deviceName, deviceType, parentMoid, startTime, stopTime, warningType, userDomainMoid, userMoid)
        if result == 1:
            f = open('/opt/data/nms_webserver/inspect/%s.xls' % parentMoid, 'rb')
            response = FileResponse(f)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=inspect_result.xls'
            return response
        else:
            response = HttpResponse()
            response.status_code = 500
            return response

