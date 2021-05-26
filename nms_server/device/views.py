import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from nms_server.dao.device import export_terminal_info_list, get_physical_frame_info_list, get_physical_frame_info_detail, get_physical_server_info_list, get_terminal_info_list, get_terminal_detail, get_uncontroled_terminal, save_uncontroled_terminal
from nms_server.dao.redis import device
from nms_server.dao.warning import get_terminal_warning_status
from django.core.cache import cache
from nms_server.utils.sso import admin_authenticate
from django.conf import settings
from nms_server.rmq.producer import produce_msg
from nms_server.utils import error_code
from django.http import FileResponse

logger = logging.getLogger("nms." + __name__)


# physical
# 所有服务器设备类型列表
class ServerTypeList(APIView):
    def get(self, request, *args, **kwargs):
        logger.info('start get server_type_list')
        server_type_list = device.get_server_type_list()
        logger.info('server_type_list : %s' % server_type_list)
        response = {'success': 1}
        response['data'] = server_type_list
        return Response(response)


# physical设备类型列表
class PhysicalTypeList(APIView):
    def get(self, request, *args, **kwargs):
        logger.info('start get physical_type_list')
        physical_type_list = device.get_physical_type_list()
        logger.info('physical_type_list : %s' % physical_type_list)
        response = {'success': 1}
        response['data'] = physical_type_list
        return Response(response)

# 机框设备类型列表
class FrameTypeList(APIView):
    def get(self, request, *args, **kwargs):
        logger.info('start get frame_type_list')
        frame_type_list = device.get_frame_type_list()
        logger.info('frame_type_list : %s' % frame_type_list)
        response = {'success': 1}
        response['data'] = frame_type_list
        return Response(response)

# 非机框设备类型列表
class NoframeTypeList(APIView):
    def get(self, request, *args, **kwargs):
        logger.info('start get noframe_type_list')
        noframe_type_list = device.get_noframe_type_list()
        logger.info('noframe_type_list : %s' % noframe_type_list)
        response = {'success': 1}
        response['data'] = noframe_type_list
        return Response(response)

# 机框列表信息
class PhysicalFrameInfoList(APIView):
    def get(self, request, *args, **kwargs):
        parentMoid = request.GET.get('parentMoid')
        deviceType = request.GET.get('deviceType')
        deviceName = request.GET.get('deviceName')

        if parentMoid == None or deviceType == None or deviceName == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success': 0,
                            "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[PhysicalServerInfoList] parentMoid=%s' % parentMoid)
        logger.info('[PhysicalServerInfoList] deviceType=%s' % deviceType)
        logger.info('[PhysicalServerInfoList] deviceName=%s' % deviceName)

        server_list = get_physical_frame_info_list(
            parentMoid, deviceType, deviceName)
        response = {'success': 1}
        response['data'] = server_list
        return Response(response)

#设备名称详情
class DeviceNameDetail(APIView):
    def get(self, request, *args, **kwargs):
        parentMoid = request.GET.get('parentMoid')
        frameMoid = request.GET.get('frameMoid')

        if parentMoid == None or frameMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {
                    'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[DeviceNameDetail] parentMoid={}'.format(parentMoid))
        logger.info('[DeviceNameDetail] frameMoid={}'.format(frameMoid))

        server_list = get_physical_frame_info_detail(parentMoid, frameMoid)
        response = {'success': 1}
        response['data'] = server_list
        return Response(response)

# 服务器列表信息
class PhysicalServerInfoList(APIView):
    def get(self, request, *args, **kwargs):
        parentMoid = request.GET.get('parentMoid')
        deviceType = request.GET.get('deviceType')
        deviceName = request.GET.get('deviceName')

        if parentMoid == None or deviceType == None or deviceName == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {
                    'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[PhysicalServerInfoList] parentMoid={}'.format(parentMoid))
        logger.info('[PhysicalServerInfoList] deviceType={}'.format(deviceType))
        logger.info('[PhysicalServerInfoList] deviceName={}'.format(deviceName))

        server_list = get_physical_server_info_list(
            parentMoid, deviceType, deviceName)
        response = {'success': 1}
        response['data'] = server_list
        return Response(response)



# 单个物理服务器的详细信息
class PhysicalServerDetailInfo(APIView):
    def get(self, request, *args, **kwargs):
        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == '' or deviceMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[PhysicalServerDetailInfo] deviceMoid : %s' % deviceMoid)

        server_info = device.get_physical_server_info(deviceMoid)
        response = {'success': 1}
        response['data'] = server_info
        return Response(response)


# 物理服务器磁盘信息
class PhysicalDiskInfo(APIView):
    def get(self, request, *args, **kwargs):
        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == '' or deviceMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[PhysicalDiskInfo] deviceMoid : %s' % deviceMoid)

        disk_info = device.get_physical_disk_info(deviceMoid)
        response = {'success': 1}
        response['data'] = disk_info
        return Response(response)


# Terminal 
# 终端类型列表
class TerminalTypeList(APIView):
    def get(self, request, *args, **kwargs):
        logger.info('start get get_terminal_type_list')
        terminal_type_list = device.get_terminal_type_list()
        logger.info('terminal_type_list : %s' % terminal_type_list)
        response = {'success': 1}
        response['data'] = terminal_type_list
        return Response(response)


# 终端设备列表
class TerminalInfoList(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")
        parentMoid = request.GET.get('parentMoid')
        deviceName = request.GET.get('deviceName')

        if parentMoid == None or deviceName == None or page == None or page == '':
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {
                    'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[TerminalInfoList] parentMoid=%s' % parentMoid)
        logger.info('[TerminalInfoList] deviceName=%s' % deviceName)
        logger.info('[TerminalInfoList] page=%s' % page)
        terminal_list, total_num = get_terminal_info_list(
            parentMoid, deviceName, page)
        response = {'success': 1}
        response['data'] = terminal_list
        response['total_num'] = total_num
        return Response(response)

# 终端设备导出
class TerminalInfoDownLoad(APIView):
    def get(self, request, *args, **kwargs):
        parentMoid = request.GET.get('parentMoid')
        deviceName = request.GET.get('deviceName')

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']

        logger.info('[TerminalInfoList] parentMoid=%s' % parentMoid)
        logger.info('[TerminalInfoList] deviceName=%s' % deviceName)

        export_terminal_info_list(parentMoid, deviceName)
        f = open('/opt/data/nms_webserver/inspect/%s.xls' % parentMoid, 'rb')
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=inspect_result.xls'
        return response


# 终端详情信息
class TerminalDetailInfo(APIView):
    def get(self, request, *args, **kwargs):
        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == '' or deviceMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[TerminalDetailInfo] deviceMoid=%s' % deviceMoid)
        terminal_info = get_terminal_detail(deviceMoid)
        response = {'success': 1}
        response['data'] = terminal_info
        return Response(response)

# 终端性能信息
class TerminalPerformanceInfo(APIView):
    def get(self, request, *args, **kwargs):
        deviceMoid = request.GET.get('deviceMoid')
        devType = request.GET.get('devType')
        if deviceMoid == '' or deviceMoid == None or devType == '' or devType == None:
            response = {'success': 0, "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[TerminalPerformanceInfo] deviceMoid=%s' % deviceMoid)
        logger.info('[TerminalPerformanceInfo] devType=%s' % devType)
        terminal_performance_info = device.get_terminal_performance_info(deviceMoid, devType)
        warning_status = get_terminal_warning_status(deviceMoid, devType)
        response = {'success': 1}
        response['data'] = terminal_performance_info
        response['data']['warning_status'] = warning_status
        return Response(response)

# 终端外设信息列表
class TerminalPeripherals(APIView):
    def get(self, request, *args, **kwargs):
        deviceMoid = request.GET.get('deviceMoid')
        if deviceMoid == '' or deviceMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[TerminalPeripherals] deviceMoid=%s' % deviceMoid)

        peripherals_list = device.get_terminal_peripherals_list(deviceMoid)
        response = {'success': 1}
        response['data'] = peripherals_list
        return Response(response)


# 非受管终端信息数据列表
class UncontroledTerminalList(APIView):
    # 获取列表显示
    def get(self, request, *args, **kwargs):
        page = request.GET.get("newPageNum")
        deviceName = request.GET.get("deviceName")
        parentMoid = request.GET.get('parentMoid')

        if parentMoid == None or page == None or deviceName == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {
                    'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[UncontroledTerminalList] parentMoid=%s' % parentMoid)
        logger.info('[UncontroledTerminalList] deviceName=%s' % deviceName)

        terminal_list, total_num = get_uncontroled_terminal(
            parentMoid, page, deviceName)
        response = {'success': 1}
        response['data'] = terminal_list
        response['total_num'] = total_num
        return Response(response)

    # 编辑
    def post(self, request):
        terminalID = request.POST.get('id')
        terminalType = request.POST.get('type')
        terminalE164 = request.POST.get('e164')
        terminalVersion = request.POST.get('version')

        if terminalID == None or terminalType == None or terminalE164 == None or terminalVersion == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[UncontroledTerminalList] terminalID:%s, terminalType:%s, terminalE164:%s, terminalVersion:%s' % (
            terminalID, terminalType, terminalE164, terminalVersion))

        result = save_uncontroled_terminal(
            terminalID, terminalType, terminalE164, terminalVersion)
        if result:
            return Response({"success": 1})
        else:
            return Response({"success": 0})


# 服务器设备重启
class RebootServer(APIView):
    def post(self, request, *args, **kwargs):
        # 密码参数验证
        superPwd = request.POST.get('superPwd')
        if superPwd == None or superPwd == '':
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        # 密码验证
        if admin_authenticate(superPwd) == False:
            response = {
                'success': 0, "error_code": error_code.SUPER_PWD_ERROR, 'message': '超管密码错误'}
            return Response(response)

        # 设备moid等参数验证
        deviceMoid = request.POST.get('deviceMoid')
        deviceType = request.POST.get('deviceType')
        if deviceMoid == None or deviceMoid == '' or deviceType == None or deviceType == '':
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[RebootServer] deviceMoid=%s' % deviceMoid)
        logger.info('[RebootServer] deviceType=%s' % deviceType)

        # 获取设备所在collector的moid
        collectorInfo = device.get_collector_info(deviceMoid, deviceType, 0)
        logger.info("[RebootServer] collector info: %s" % collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {
                'success': 0, "error_code": error_code.SERVER_ERROR, 'message': '服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        msg = {"eventid": "EV_REBOOT_CMD",   # 事件号，重启
               "devid": deviceMoid,          # 设备moid
               "devtype": deviceType,        # 设备类型
               "isterminal": 0               # 0 - 非终端，1 - 终端
               }

        # 发RMQ消息
        produce_msg(collectorMoid, msg)

        return Response({'success': 1})


# 服务器设备关机
class ShutdownServer(APIView):
    def post(self, request, *args, **kwargs):
        # 密码参数验证
        superPwd = request.POST.get('superPwd')
        if superPwd == None or superPwd == '':
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        # 密码验证
        if admin_authenticate(superPwd) == False:
            response = {
                'success': 0, "error_code": error_code.SUPER_PWD_ERROR, 'message': '超管密码错误'}
            return Response(response)

        # 设备moid等参数验证
        deviceMoid = request.POST.get('deviceMoid')
        deviceType = request.POST.get('deviceType')
        if deviceMoid == None or deviceMoid == '' or deviceType == None or deviceType == '':
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[ShutdownServer] deviceMoid=%s' % deviceMoid)
        logger.info('[ShutdownServer] deviceType=%s' % deviceType)

        # 获取设备所在collector的moid
        collectorInfo = device.get_collector_info(deviceMoid, deviceType, 0)
        logger.info("[ShutdownServer] collector info: %s" % collectorInfo)

        # 获取collector的moid失败，直接返回错误
        if collectorInfo['success'] == 0:
            response = {
                'success': 0, "error_code": error_code.SERVER_ERROR, 'message': '服务器错误'}
            return Response(response)

        collectorMoid = collectorInfo['dev_moid']

        msg = {"eventid": "EV_SHUTDOWN_CMD",  # 事件号，关机
               "devid": deviceMoid,            # 设备moid
               "devtype": deviceType,          # 设备类型
               "isterminal": 0                 # 0 - 非终端，1 - 终端
               }

        # 发RMQ消息
        produce_msg(collectorMoid, msg)

        return Response({'success': 1})


# 终端设备重启
class RebootTerminal(APIView):
    def post(self, request, *args, **kwargs):
        '''
        post: {
            superPwd: 'xxx',
            'devices': [
                {
                    'devicesMoid': '',
                    'devicesType: ''
                }
            ]
        }
        '''
        # 密码参数验证
        superPwd = request.data.get('superPwd')
        if superPwd == None or admin_authenticate(superPwd) == False:
            response = {
                'success': 0, "error_code": error_code.SUPER_PWD_ERROR, 'message': '超管密码错误'}
            return Response(response)

        # 设备moid等参数验证
        error = False
        try:
            for device_info in request.data.get('devices', []):
                deviceMoid = device_info.get('deviceMoid')
                deviceType = device_info.get('deviceType')
                if deviceMoid and deviceType:
                    # 获取设备所在collector的moid
                    collectorInfo = device.get_collector_info(
                        deviceMoid, deviceType, 1)
                    # 获取collector的moid失败，直接返回错误
                    if collectorInfo['success']:
                        collectorMoid = collectorInfo['dev_moid']

                        msg = {"eventid": "EV_CONFIG_RESTART_CMD",   # 事件号，重启终端
                               "devid": deviceMoid,            # 设备moid
                               "devtype": deviceType,          # 设备类型
                               "isterminal": 1                 # 0 - 非终端，1 - 终端
                               }

                        # 发RMQ消息
                        produce_msg(collectorMoid, msg)
                    else:
                        error = True
                else:
                    error = True
        except Exception as e:
            logger.error(e)
            error = True
        finally:
            if error:
                return Response({'success': 0, "error_code": error_code.SERVER_ERROR, 'message': '服务器错误'})
            else:
                return Response({'success': 1})


# 配置终端注册地址
class ConfigTerminalRegAddr(APIView):
    def post(self, request, *args, **kwargs):
        user = getattr(request, 'sso_user', None)
        if user is not None:
            userMoid = user['data']['moid']
        else:
            response = {'success': 0, 'message': '未登陆用户'}
            return Response(response)

        logger.info('[ConfigTerminalRegAddr] userMoid=%s' % userMoid)

        data = request.data
        deviceConfig = data['deviceConfig']
        if deviceConfig == None or deviceConfig == '':
          response = {'success': 0, "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
          return Response(response)

        logger.info('[ConfigTerminalRegAddr] deviceConfig=%s' % deviceConfig)  

        for i in data['data']:
          deviceMoid = i['moid']
          deviceTypes = i['type_ter']

          if deviceMoid == None or deviceMoid == '' or deviceTypes == None or len(deviceTypes) == 0:
            response = {'success': 0, "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

          logger.info('[ConfigTerminalNetwork] deviceMoid=%s' % deviceMoid)
          logger.info('[ConfigTerminalNetwork] deviceTypes=%s' % deviceTypes)

          for deviceType in deviceTypes:
            # 获取设备所在collector的moid
            collectorInfo = device.get_collector_info(deviceMoid, deviceType, 1)
            
            # 获取collector的moid失败，直接返回错误
            if collectorInfo['success'] == 0:
                response = {'success': 0, "error_code": error_code.SERVER_ERROR, 'message': '服务器错误'}
                return Response(response)
            
            logger.info("[ConfigTerminalRegAddr] collector info: %s" % collectorInfo)

            collectorMoid = collectorInfo['dev_moid']

            msg = {"eventid": "EV_CONFIG_REG_ADDR_CMD",   # 事件号，配置终端注册地址
                    "devid": deviceMoid,                  # 设备moid
                    "user_moid": userMoid,                # 用户moid
                    "devtype": deviceType,                # 设备类型
                    "cfg": deviceConfig,                  # 终端注册地址
                    "isterminal": 1
                  }

            # 发RMQ消息
            produce_msg(collectorMoid, msg)

        return Response({'success': 1})


# 配置终端网络参数
class ConfigTerminalNetwork(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        user = getattr(request, 'sso_user', None)
        if user is not None:
            userMoid = user['data']['moid']
        else:
            response = {'success': 0, 'message': '未登陆用户'}
            return Response(response)

        logger.info('[ConfigTerminalNetwork] userMoid=%s' % userMoid)

        # 网络配置参数验证
        pktLossResend = data['pktLostResend']
        audioFirst = data['audioFirst']
        fec = data['fec']
        decodePayloadAuto = data['decodePayloadAuto']

        if pktLossResend == None or audioFirst == None or fec == None or decodePayloadAuto == None:
            response = {'success': 0, "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[ConfigTerminalNetwork] pktLossResend=%s' % pktLossResend)
        logger.info('[ConfigTerminalNetwork] audioFirst=%s' % audioFirst)
        logger.info('[ConfigTerminalNetwork] fec=%s' % fec)
        logger.info('[ConfigTerminalNetwork] decodePayloadAuto=%s' % decodePayloadAuto)

        for i in data['data']:
            deviceMoid = i['moid']
            deviceTypes = i['type_ter']

            if deviceMoid == None or deviceMoid == '' or deviceTypes == None or len(deviceTypes) == 0:
                response = {'success': 0, "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
                return Response(response)

            logger.info('[ConfigTerminalNetwork] deviceMoid=%s' % deviceMoid)
            logger.info('[ConfigTerminalNetwork] deviceTypes=%s' % deviceTypes)

            for deviceType in deviceTypes:
                # 获取设备所在collector的moid
                collectorInfo = device.get_collector_info(deviceMoid, deviceType, 1)
                logger.info("[ConfigTerminalNetwork] collector info: %s" % collectorInfo)

                # 获取collector的moid失败，直接返回错误
                if collectorInfo['success'] == 0:
                    response = {'success': 0, "error_code": error_code.SERVER_ERROR, 'message': '服务器错误'}
                    return Response(response)

                collectorMoid = collectorInfo['dev_moid']

                msg = {
                    "eventid": "EV_CONFIG_NETWORK_CMD",            # 事件号，重启终端
                    "devid": deviceMoid,                           # 设备moid
                    "user_moid": userMoid,                         # 用户moid
                    "devtype": deviceType,                         # 设备类型
                    "isterminal": 1,
                    "cfg":
                    {
                        "pkt_loss_resend": pktLossResend,          # 开启/关闭丢包重传
                        "audio_first": audioFirst,                 # 开启/关闭音频优先
                        "fec": fec,                                # 开启/关闭FEC
                        "decode_payload_auto": decodePayloadAuto   # 开启/关闭强解、载荷自适应
                    }
                }

                # 发RMQ消息
                produce_msg(collectorMoid, msg)

        return Response({'success': 1})


# 配置终端视频格式
class ConfigTerminalVideoFormat(APIView):
    def post(self, request, *args, **kwargs):
        user = getattr(request, 'sso_user', None)
        if user is not None:
            userMoid = user['data']['moid']
        else:
            response = {'success': 0, 'message': '未登陆用户'}
            return Response(response)

        logger.info('[ConfigTerminalVideoFormat] userMoid=%s' % userMoid)
        
        data = request.data

        # 设备moid等参数验证
        deviceMoid = data['data'][0]['moid']
        deviceTypes = data['data'][0]['type_ter']
        deviceConfig = data['deviceConfig']

        if deviceMoid == None or deviceMoid == '' or deviceTypes == None or len(deviceTypes) == 0 or deviceConfig == None or deviceConfig == '':
            response = {'success': 0, "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[ConfigTerminalVideoFormat] deviceMoid=%s' % deviceMoid)
        logger.info('[ConfigTerminalVideoFormat] deviceTypes=%s' % deviceTypes)
        logger.info('[ConfigTerminalVideoFormat] deviceConfig=%s' % deviceConfig)

        for deviceType in deviceTypes:
          # 获取设备所在collector的moid
          collectorInfo = device.get_collector_info(deviceMoid, deviceType, 1)
          logger.info("[ConfigTerminalVideoFormat] collector info: %s" % collectorInfo)

          # 获取collector的moid失败，直接返回错误
          if collectorInfo['success'] == 0:
              response = {'success': 0, "error_code": error_code.SERVER_ERROR, 'message': '服务器错误'}
              return Response(response)

          collectorMoid = collectorInfo['dev_moid']

          msg = {"eventid": "EV_CONFIG_1ST_VIDEO_FORMAT_CMD",   # 事件号, 配置终端视频格式
                  "devid": deviceMoid,                          # 设备moid
                  "user_moid": userMoid,                        # 用户moid
                  "devtype": deviceType,                        # 设备类型
                  "cfg": deviceConfig,                          # 终端视频格式
                  "isterminal": 1
                }

          # 发RMQ消息
          produce_msg(collectorMoid, msg)

        return Response({'success': 1})


# 在线服务器名称、类型、网卡信息（作为抓包参数显示使用）
class OnlineServerList(APIView):
    def get(self, request, *args, **kwargs):

        parentMoid = request.GET.get('parentMoid')

        if parentMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {
                    'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[OnlineServerList] parentMoid=%s' % parentMoid)

        response = {'success': 1}
        response['data'] = device.get_online_server_list(parentMoid)
        return Response(response)


# 在线终端名称、类型、网卡信息（作为抓包参数显示使用）
class OnlineTerminalList(APIView):
    def get(self, request, *args, **kwargs):

        parentMoid = request.GET.get('parentMoid')

        if parentMoid == None:
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        if parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {
                    'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
                return Response(response)

        logger.info('[OnlineTerminalList] parentMoid=%s' % parentMoid)

        response = {'success': 1}
        response['data'] = device.get_online_terminal_list(parentMoid)
        return Response(response)


class LogicalServerList(APIView):
    def get(self, request, *args, **kwargs):
        pServerMoid = request.GET.get('pServerMoid')

        if pServerMoid == None or pServerMoid == '':
            response = {'success': 0,
                        "error_code": error_code.INPUT_ERROR, 'message': '参数错误'}
            return Response(response)

        logger.info('[LogicalServerList] pServerMoid=%s' % pServerMoid)

        server_list = device.get_logical_server_list(pServerMoid)
        for value in server_list:
            if value.get('type','') == 'pas':
                server_list.append({'moid':'','type':'callmanager','name':'callmanager'})
                server_list.append({'moid':'','type':'h323n','name':'h323n'})
                server_list.append({'moid':'','type':'h323nadp','name':'h323nadp'})
                server_list.append({'moid':'','type':'h323s','name':'h323s'})
                server_list.append({'moid':'','type':'h323sadp','name':'h323sadp'})
                server_list.append({'moid':'','type':'mpcadp','name':'mpcadp'})
                server_list.append({'moid':'','type':'ngi','name':'ngi'})
                server_list.append({'moid':'','type':'sipagent','name':'sipagent'})
                server_list.append({'moid':'','type':'sipproxy','name':'sipproxy'})
                server_list.append({'moid':'','type':'webrtcagent','name':'webrtcagent'})
                server_list.append({'moid':'','type':'protocol','name':'protocol'})

        server_list.append({'moid':'','type':'guard','name':'guard'})
        server_list.append({'moid':'','type':'monitor','name':'monitor'})
        server_list.append({'moid':'','type':'haproxy','name':'haproxy'})
        server_list.append({'moid':'','type':'nginx','name':'nginx'})
        server_list.append({'moid':'','type':'system','name':'system'})
        server_list.append({'moid':'','type':'docker','name':'docker'})

        response = {'success': 1}
        response['data'] = server_list
        return Response(response)