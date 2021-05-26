import logging
import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from nms_server.utils import error_code
from nms_server.utils.server_log_dir import GetServerLogDir
from nms_server.dao.redis.device import get_collector_info
from nms_server.dao import diagnosis
from nms_server.rmq.producer import produce_msg
from nms_server.dao.redis.diagnosis import get_server_resource_info
from nms_server.utils.exception import NotLoginError
import requests
from nms_server.settings import KDFS, REQUESTS_TIMEOUT
from django.http import FileResponse

logger = logging.getLogger("nms." + __name__)


# 获取抓包设备列表
# 编辑抓包设备
class CaptureDevice(APIView):
    def get(self, request, *args, **kwargs):
        """
        获取抓包对象信息
        GET 
        return {
            data: 抓包对象数据,
            total_num: 抓包对象的数量
        }
        """
        logger.info("get capture device")

        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[CaptureDevice] userMoid : %s' % userMoid)

        response = {'success': 1}
        response['data'], response['total_num'] = diagnosis.get_capture_device(userMoid)
        return Response(response)

    def post(self, request):
        """
        修改抓包对象信息
        POST {
            deviceID: 抓包对象数据库唯一id
            deviceType: 抓包对象类型
            netcard: 抓包对象新的网口名
        }
        """
        deviceID = request.data.get('deviceID')
        deviceType = request.data.get('deviceType')
        netcard = request.data.get('netcard')

        if deviceID == None or deviceType == None or netcard == None:
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        if deviceID == '' or deviceType == '' or netcard == '':
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        logger.info('[CaptureDevice] deviceID : %s' % deviceID)
        logger.info('[CaptureDevice] deviceType : %s' % deviceType)
        logger.info('[CaptureDevice] netcard : %s' % netcard)
        
        result = diagnosis.edit_capture_device(deviceID, deviceType, netcard)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"message":"数据库错误"})

# 添加抓包设备
class AddCaptureDevice(APIView):
    def post(self, request):
        """
        添加抓包对象信息
        POST {
            deviceCategory: 抓包设备类型
            deviceMoid: 抓包设备moid
            deviceType: 抓包对象类型
            netcard: 抓包设备网口名
        }
        """
        deviceCategory = request.data.get('deviceCategory')
        deviceMoid = request.data.get('deviceMoid')
        deviceType = request.data.get('deviceType')
        netcard = request.data.get('netcard')

        if deviceCategory == None or deviceMoid == None or deviceType == None or netcard == None:
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        if deviceCategory != 'server' and deviceCategory != 'terminal':
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        if deviceMoid == '' or deviceType == '' or netcard == '':
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})
        
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[AddCaptureDevice] deviceCategory : %s' % deviceCategory)
        logger.info('[AddCaptureDevice] deviceMoid : %s' % deviceMoid)
        logger.info('[AddCaptureDevice] deviceType : %s' % deviceType)
        logger.info('[AddCaptureDevice] netcard : %s' % netcard)
        logger.info('[AddCaptureDevice] userMoid : %s' % userMoid)

        result = diagnosis.add_capture_device(userMoid, deviceCategory, deviceMoid, deviceType, netcard)
        if result == 0:
            return Response({"success":1})
        elif result == 2:
            return Response({"success":2,'message':'抓包对象重复'})
        else:
            return Response({"success":0,'message':'数据库错误'})

# 删除抓包设备
class DeleteCaptureDevice(APIView):
    def post(self, request):
        """
        删除抓包对象信息
        POST {
            deviceID: 抓包对象数据库唯一id
        }
        """
        deviceID = request.data.get('deviceID')
        if deviceID == None or deviceID == '':
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        logger.info("deviceID : %s" % deviceID)

        result = diagnosis.del_capture_device(deviceID)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,'message':'数据库错误'})

# 开始抓包
class StartCaptureDevice(APIView):
    def post(self, request):
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[StartCaptureDevice] userMoid=%s' % userMoid)
            
        # 参数验证
        deviceMoid = request.data.get('deviceMoid')
        deviceType = request.data.get('deviceType')
        deviceCategory = request.data.get('deviceCategory')
        netcard = request.data.get('netcard')

        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceType == None or deviceType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceCategory != 'server' and deviceCategory != 'terminal':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if netcard == None or netcard == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[StartCaptureDevice] userMoid=%s' % userMoid)
        logger.info('[StartCaptureDevice] deviceMoid=%s' % deviceMoid)
        logger.info('[StartCaptureDevice] deviceType=%s' % deviceType)
        logger.info('[StartCaptureDevice] deviceCategory=%s' % deviceCategory)
        logger.info('[StartCaptureDevice] netcard=%s' % netcard)

        isTerminal = 1
        if deviceCategory == 'server':
            isTerminal = 0

        # 获取设备所在collector的moid
        collectorInfo = get_collector_info(deviceMoid,deviceType,isTerminal)
        logger.info("[StartCaptureDevice] collector info: %s"%collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {'success':0,"error_code":error_code.SERVER_ERROR, 'message':'服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        msg = {"eventid": "EV_PACKETCAPTURE_START_REQ",   # 事件号，抓包请求
               "user_moid":userMoid,    # 抓包账户的moid
               "devid":deviceMoid,      # 设备moid
               "devtype":deviceType,    # 设备类型
               "netcard":netcard,       # 抓包网卡
               "isterminal":isTerminal  # 是否终端设备
              }

        # 发RMQ消息
        produce_msg(collectorMoid, msg)

        return Response({'success': 1})

# 结束抓包
class StopCaptureDevice(APIView):
    def post(self, request):
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success': 0, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[StopCaptureDevice] userMoid=%s' % userMoid)
            
        # 参数验证
        deviceMoid = request.data.get('deviceMoid')
        deviceType = request.data.get('deviceType')
        deviceCategory = request.data.get('deviceCategory')

        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceType == None or deviceType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceCategory != 'server' and deviceCategory != 'terminal':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[StopCaptureDevice] userMoid=%s' % userMoid)
        logger.info('[StopCaptureDevice] deviceMoid=%s' % deviceMoid)
        logger.info('[StopCaptureDevice] deviceType=%s' % deviceType)
        logger.info('[StopCaptureDevice] deviceCategory=%s' % deviceCategory)

        isTerminal = 1
        if deviceCategory == 'server':
            isTerminal = 0

        # 获取设备所在collector的moid
        collectorInfo = get_collector_info(deviceMoid,deviceType,isTerminal)
        logger.info("[StopCaptureDevice] collector info: %s"%collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {'success':0,"error_code":error_code.SERVER_ERROR, 'message':'服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        msg = {"eventid": "EV_PACKETCAPTURE_STOP_REQ",   # 事件号，停止抓包请求
               "user_moid":userMoid,     # 抓包账户的moid
               "devid":deviceMoid,       # 设备moid
               "devtype":deviceType,     # 设备类型
               "isterminal":isTerminal
              }

        # 发RMQ消息
        produce_msg(collectorMoid, msg)

        return Response({'success': 1})

# 获取抓包文件
class CaptureFile(APIView):
    def get(self, request, *args, **kwargs):
        """
        POST {
            newPageNum: 页码
        }

        return:{
           data: "抓包文件数据" ,
           total_num: "抓包文件数"
        }
        """
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[CaptureFile] userMoid : %s' % userMoid)

        page = request.GET.get('newPageNum')
        if page == None or page == '':
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        logger.info('[CaptureFile] page : %s' % page)

        response = {'success': 1}
        response['data'], response['total_num'] = diagnosis.get_capture_file(userMoid,page)
        return Response(response)

    def post(self, request):
        """
        删除抓包文件信息
        POST {
            fileID: 抓包文件数据库唯一id
        }
        """
        fileID = request.data.get('fileID')
        if fileID == None or fileID == '':
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        logger.info("[CaptureFile] fileID : %s" % fileID)

        result = diagnosis.del_capture_file(fileID)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"message":"数据库错误"})
    

# 下载抓包文件
class DownloadCaptureFile(APIView):
    def get(self, request):

        user = getattr(request, 'sso_user', None)
        if user == None: 
            response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)
        # 参数验证
        fileName = request.GET.get("fileName")
        deviceMoid = request.GET.get("deviceMoid")

        if fileName == None or fileName == '' or deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)
        
        ip = KDFS['HOST']
        port = KDFS['PORT']

        logger.info('[DownloadCaptureFile] kdfs ip = %s' % ip)
        logger.info('[DownloadCaptureFile] kdfs port = %s' % port)
        logger.info('[DownloadCaptureFile] file name = %s' % fileName)
        logger.info('[DownloadCaptureFile] file deviceMoid = %s' % deviceMoid)   

        download_url = "http://"+ip+":"+port+"/api/inner/kdfs/v1"
        filePath = os.path.join(deviceMoid,fileName)
        
        logger.info('[DownloadCaptureFile] download_url=%s,filePath=%s,',download_url,filePath)
        
        headers = {
            'path': filePath,
            'type': 'download',
            'home': 'platformLog'
        }
        
        file = requests.get(download_url, headers=headers, timeout=REQUESTS_TIMEOUT)
        
        logger.info('[DownloadCaptureFile] file.status_code=%s' % file.status_code)

        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % (fileName)

        return response

# 获取日志列表
class GetLogList(APIView):
    def post(self, request):
        # 获取用户moid
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[GetLogList] userMoid=%s' % userMoid)

        # 参数验证
        deviceMoid = request.data.get('deviceMoid')
        deviceType = request.data.get('deviceType')
        logType = request.data.get('logType')

        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceType == None or deviceType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if logType == None or logType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[GetLogList] deviceMoid=%s' % deviceMoid)
        logger.info('[GetLogList] deviceType=%s' % deviceType)
        logger.info('[GetLogList] logType=%s' % logType)

        logDir = GetServerLogDir(logType)
        if logDir == '':
            logger.info('[GetLogList] logDir is empty')
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        # 获取设备所在collector的moid
        collectorInfo = get_collector_info(deviceMoid,deviceType,0)
        logger.info("[GetLogList] collector info: %s"%collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {'success':0,"error_code":error_code.SERVER_ERROR, 'message':'服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        msg = {"eventid": "EV_GETLOG_LIST_REQ",   # 事件号，获取日志列表
               "devid":deviceMoid,       # 设备moid
               "user_moid":userMoid,     # 用户moid
               "devtype":deviceType,     # 设备类型
               "logical_log_dir":logDir  # 日志目录
              }

        # 发RMQ消息
        produce_msg(collectorMoid, msg)
        
        return Response({'success': 1, 'logDir': logDir})

# 下载日志
class DownloadLogFile(APIView):
    def post(self, request, *args, **kwargs):
        # 获取用户moid
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[DownloadLogFile] userMoid=%s' % userMoid)

        # 参数验证
        deviceMoid = request.data.get('deviceMoid')
        deviceType = request.data.get('deviceType')
        fileList = request.data.get('fileList')
        deviceCategory = request.data.get('deviceCategory')

        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceType == None or deviceType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceCategory != 'server' and deviceCategory != 'terminal':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceCategory == 'server' and fileList == None or fileList == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[DownloadLogFile] deviceMoid=%s' % deviceMoid)
        logger.info('[DownloadLogFile] deviceType=%s' % deviceType)
        logger.info('[DownloadLogFile] fileList=%s' % fileList)
        logger.info('[DownloadLogFile] deviceCategory=%s' % deviceCategory)

        isTerminal = 1
        if deviceCategory == 'server':
            isTerminal = 0

        # 获取设备所在collector的moid
        collectorInfo = get_collector_info(deviceMoid,deviceType,isTerminal)
        logger.info("[DownloadLogFile] collector info: %s"%collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {'success':0,"error_code":error_code.SERVER_ERROR, 'message':'服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        msg = {"eventid":"EV_GETLOG_REQ", # 消息类型
               "devid":deviceMoid,        # 服务器/终端moid
               "user_moid":userMoid,      # 用户moid
               "devtype":deviceType,      # 服务器/终端类型
               "file_list":fileList,       # 日志文件列表
               "isterminal":isTerminal
              }

        # 发RMQ消息
        produce_msg(collectorMoid, msg)

        return Response({'success': 1})

# 服务器诊断
class ServerDiagnose(APIView):
    def get(self, request, *args, **kwargs):
        # 参数验证
        deviceMoid = request.GET.get('deviceMoid')

        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)
        logger.info('[ServerDiagnose] deviceMoid=%s' % deviceMoid)

        server_resource_info = get_server_resource_info(deviceMoid)
        logger.info('[ServerDiagnose] server_resource_info=%s' % server_resource_info)

        response = {'success': 1}
        response['data'] = server_resource_info
        return Response(response)
        
# 终端诊断
class TerminalDiagnose(APIView):
    def post(self, request, *args, **kwargs):
        # 获取用户moid
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            userMoid = user['data']['moid']
        else:
            response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        logger.info('[TerminalDiagnose] userMoid=%s' % userMoid)

        # 参数验证
        deviceMoid = request.data.get('deviceMoid')
        deviceType = request.data.get('deviceType')
        
        if deviceMoid == None or deviceMoid == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceType == None or deviceType == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[TerminalDiagnose] deviceMoid=%s' % deviceMoid)
        logger.info('[TerminalDiagnose] deviceType=%s' % deviceType)

        # 获取设备所在collector的moid
        collectorInfo = get_collector_info(deviceMoid,deviceType,1)
        logger.info("[TerminalDiagnose] collector info: %s"%collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {'success':0,"error_code":error_code.SERVER_ERROR, 'message':'服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        logger.info("[TerminalDiagnose] collectorMoid: %s"%collectorMoid)

        # 终端性能信息请求
        msg1 = {"eventid":"EV_PFMINFO_REQ", # 消息类型
                "devid":deviceMoid,         # 终端moid
                "user_moid":userMoid,       # 用户moid
                "devtype":deviceType,       # 终端类型
                "isterminal": 1
              }
        logger.info("[TerminalDiagnose] 11111")
        produce_msg(collectorMoid, msg1)

        # 终端音视频信号请求回复
        msg2 = {"eventid":"EV_AUDIO_VIDEO_STATUS_REQ", # 消息类型
                "devid":deviceMoid,         # 终端moidc
                "user_moid":userMoid,       # 用户moid
                "devtype":deviceType,       # 终端类型
                "isterminal": 1
              }
        logger.info("[TerminalDiagnose] 22222")
        produce_msg(collectorMoid, msg2)

        # 终端音量能量值请求
        msg3 = {"eventid":"EV_VOLUME_REQ", # 消息类型
                "user_moid":userMoid,      # 用户moid
                "devid":deviceMoid,        # 终端moid
                "devtype":deviceType,      # 终端类型
                "isterminal": 1
              }
        logger.info("[TerminalDiagnose] 33333")
        produce_msg(collectorMoid, msg3)

        return Response({'success': 1})
