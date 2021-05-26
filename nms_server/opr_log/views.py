import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from nms_server.dao import opr_log
from django.http import FileResponse

logger = logging.getLogger("nms." + __name__)

# 网管日志数据列表
class LogInfoList(APIView):
    def get(self, request, *args, **kwargs):
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            accountDomainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        page = request.GET.get('newPageNum')
        userName = request.GET.get('userName')
        operateType = request.GET.get('operateType')
        operateLevel = request.GET.get('operateLevel')
        startTime = request.GET.get('starttime')
        stopTime = request.GET.get('stoptime')

        logger.info('accountDomainMoid:%s,userName:%s, operateType:%s, operateLevel:%s, page:%s, startTime:%s, stopTime:%s'%(accountDomainMoid,userName,operateType,operateLevel,page,startTime,stopTime))
        
        log_list, total_num = opr_log.get_opr_log(accountDomainMoid,userName, operateType, operateLevel, page, startTime, stopTime)
        response = {'success': 1}
        response['logs'] = log_list
        response['log_total_num'] = total_num
        return Response(response)

# 导出网管日志
class DownloadLog(APIView):
    def get(self, request, *args, **kwargs):
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            accountDomainMoid = user['data']['accountDomainMoid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        userName = request.GET.get('userName')
        operateType = request.GET.get('operateType')
        operateLevel = request.GET.get('operateLevel')
        startTime = request.GET.get('starttime')
        stopTime = request.GET.get('stoptime')

        logger.info('accountDomainMoid:%s, userName:%s, operateType:%s, operateLevel:%s, startTime:%s, stopTime:%s'%(accountDomainMoid,userName,operateType,operateLevel,startTime,stopTime))
        
        opr_log.export_log_info_list(accountDomainMoid,userName, operateType, operateLevel, startTime, stopTime)
        f = open('/opt/data/nms_webserver/inspect/%s.xls' % startTime, 'rb')
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=inspect_result.xls'
        return response