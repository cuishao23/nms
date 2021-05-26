import logging
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from nms_server.dao import system_set
from nms_server.utils import error_code

logger = logging.getLogger('nms.'+__name__)

class ResourceLimit(APIView):
    def get(self, request, *args, **kwargs):
        response = {'success': 1}
        response['limits'] = system_set.get_resource_limit()
        return Response(response)
    def post(self, request):
        limit_type = request.data.get('type')
        data = request.data.get('value')

        if limit_type == None or data == None:
            response = {'success': 0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if limit_type != 'pas' and limit_type != 'callpair' and limit_type != 'nms' and limit_type != 'resource':
            response = {'success': 0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        logger.info('[DomainLimit] type = %s' % limit_type)
        logger.info('[DomainLimit] data = %s' % data)
        result = system_set.set_resource_limit(limit_type, data)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR, 'message':'阈值设置失败'})

class ServerLimit(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        parentMoid = request.GET.get('moid')
        if parentMoid == "all":
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['serviceDomainMoid']
            else:
                response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        logger.info('[ServerLimit] parentMoid:%s'%parentMoid)

        response = {'success': 1}
        response['servers'], response['TotalNum'] = system_set.get_server_limit(page, parentMoid)
        return Response(response)

    def post(self, request):
        deviceMoid = request.data.get('moid')
        cpu = request.data.get('cpu')
        memory = request.data.get('memory')
        port = request.data.get('port')
        disk = request.data.get('disk')
        diskwritespeed = request.data.get('diskwritespeed')
        rateofflow = request.data.get('rateofflow')
        result = system_set.set_servers_limit(deviceMoid, cpu, memory, port, disk, diskwritespeed, rateofflow)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"设置服务器阈值失败"})

class DeviceConfig(APIView):
    def get(self, request, *args, **kwargs):
        terminalType = request.GET.get('terminal_type')
        terminalModel = request.GET.get('terminal_model')
        page = request.GET.get('page')

        logger.info('terminal type = %s' % terminalType)
        logger.info('terminal model = %s' % terminalModel)
    
        response = {'success': 1}
        response['device'], response['TotalNum'] = system_set.get_device_config(terminalType, terminalModel, page)
        return Response(response)
        
    def post(self, request):
        mainModel = request.data.get('name')
        terminalType = request.data.get('terminal_type')
        deviceTag = request.data.get('device_tag')
        productName = request.data.get('product_name')

        if mainModel == None or terminalType == None or terminalType == None or productName == None:
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        logger.info('[DeviceConfig] name:%s' % mainModel)
        logger.info('[DeviceConfig] terminal_type:%s' % terminalType)
        logger.info('[DeviceConfig] device_tag:%s' % deviceTag)
        logger.info('[DeviceConfig] product_name:%s' % productName)
        
        result = system_set.add_device_config(mainModel, terminalType, deviceTag, productName)
        if result == 0:
            return Response({"success":1})
        elif result == 1:
            return Response({"success":0,"error_code":error_code.TERMINAL_TYPE_EXIST,"message":"子类型已存在"})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"添加终端设备类型失败"})


class DeleteDeviceConfig(APIView):
    def post(self, request):
        mainModel = request.data.get('name')
        productName = request.data.get('product_name')
        if mainModel == None or productName == None:
            return Response({"success":0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'})
        
        logger.info('[DeleteDeviceConfig] name:%s' % mainModel)
        logger.info('[DeleteDeviceConfig] product_name:%s' % productName)

        result = system_set.delete_device_config(mainModel, productName)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"删除终端设备类型失败"})

# 设备型号数据列表
class TerminalTypeList(APIView):
    def get(self, request, *args, **kwargs):
        type_list = system_set.get_terminal_type_list()
        logger.info('[TerminalTypeList] terminal type list : %s' % type_list)
        response = {'success': 1}
        response['data'] = type_list
        return Response(response)
        
# 告警码
class WarningTreeList(APIView):
    def get(self, request, *args, **kwargs):
        response = {'success': 1}
        response['warning_trees'] = system_set.get_warning_tree()
        return Response(response)

class SubWarningCode(APIView):
    def get(self, request, *args, **kwargs):
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            user_moid = user['data']['moid']
            domain_moid = user['data']['serviceDomainMoid']
        else:
            response = {'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
            return Response(response)
            #user_moid = ""
            #domain_moid = ""
        response = {'success': 1}
        response['subwarningcode'] = system_set.get_warning_code(user_moid, domain_moid)
        return Response(response)

    def post(self, request):
        code = request.data.get('warning_code')
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            user_moid = user['data']['moid']
            domain_moid = user['data']['serviceDomainMoid']
        else:
            #user_moid = ""
            #domain_moid = ""
            response = {'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
            return Response(response)
        result = system_set.set_warning_code(user_moid, domain_moid, code)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"设置订阅告警失败"})

class WarningNotify(APIView):
    # 获取告警通知列表
    def get(self, request, *args, **kwargs):
        user = getattr(request, 'sso_user', None)
        if user is not None:
            domain_moid = user['data']['serviceDomainMoid']
            user_moid = user['data']['moid']
        else:
            response = {'success': 0, "error_code": error_code.UN_LOGIN, 'message': '未登陆用户'}
            return Response(response)
            #user_moid = ""
            #domain_moid = ""
        page = request.GET.get('newPageNum')

        response = {'success': 1}
        response['warning_notify_list'], response['TotalNum'] = system_set.get_warning_notify(domain_moid,user_moid,page)
        return Response(response)

    # 新增告警告警通知
    def post(self, request):
        user = getattr(request, 'sso_user', None)
        if user is not None:
            domain_moid = user['data']['serviceDomainMoid']
            user_moid = user['data']['moid']
        else:
            #user_moid = ""
            #domain_moid = ""
            response = {'success': 0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
            return Response(response)

        email = request.data.get('email')
        phone = request.data.get('phone')
        wechat = request.data.get('wechat')
        code_list = request.data.get('code_list')
        name = request.data.get('name')

        logger.info('email:%s' % email)
        logger.info('phone:%s' % phone)
        logger.info('wechat:%s' % wechat)
        logger.info('warning:%s' % code_list)
        logger.info('domain moid:%s' % domain_moid)
        logger.info('user moid:%s' % user_moid)
        result = system_set.set_warning_notify(name, email, phone, wechat, code_list, domain_moid, user_moid)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"设置告警通知失败"})

# 删除告警通知
class DeleteWarningNotify(APIView):
    def post(self, request):
        warningNotifyID = request.data.get('id')
        if warningNotifyID == None:
            return Response({"success":0,"error_code":error_code.INPUT_ERROR,"message":"参数错误"})

        logger.info('[DeleteWarningNotify] warning notify id:%s' % warningNotifyID)
        result = system_set.delete_warning_notify(warningNotifyID)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"删除告警通知失败"})


# 编辑告警通知
class EditWarningNotify(APIView):
    def post(self, request):
        notifyID = request.data.get('id')
        phone = request.data.get('phone')
        email = request.data.get('email')
        wechat = request.data.get('wechat')
        code_list = request.data.get('code_list')
        logger.info('notifyID:%s' % notifyID)
        logger.info('email:%s' % email)
        logger.info('phone:%s' % phone)
        logger.info('wechat:%s' % wechat)
        logger.info('warning:%s' % code_list)
        result = system_set.edit_warning_notify(notifyID, phone, email, wechat, code_list)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"编辑告警通知失败"})

class WarningLevel(APIView):
    def get(self, request):
        user = getattr(request, 'sso_user', None)
        if user is not None: 
            user_moid = user['data']['moid']
            domain_moid = user['data']['serviceDomainMoid']
        else:
            response = {'success':0,"error_code":error_code.UN_LOGIN,'message':'未登陆用户'}
            return Response(response)

        warning_level = system_set.get_warning_level(user_moid, domain_moid)
        response = {'success': 1}
        response['level'] = warning_level
        return Response(response)

    def post(self, request):
        level = request.data.get('level')
        warning_type = request.data.get('type')

        if level == None or warning_type == None:
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        logger.info('warning_level:%s' % level)
        logger.info('warning_type:%s' % warning_type)

        user = getattr(request, 'sso_user', None)
        if user is not None:
            user_moid = user['data']['moid']
            domain_moid = user['data']['serviceDomainMoid']
            logger.info('user_moid:%s, domain_moid:%s' % (user_moid, domain_moid))
        else:
            response = {'success': 0, "error_code":error_code.UN_LOGIN,'message':'未登陆用户'}
            return Response(response)

        result = system_set.edit_warning_level(user_moid, domain_moid, warning_type, level)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"设置告警级别失败"})

class StopWarning(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        response = {'success': 1}
        response['stopWarnings'], response['TotalNum'], response['allWarnings'] = system_set.get_stopwarning_list(page)
        return Response(response)

    def post(self, request):
        moidList = request.data.get('moid')
        logger.info('stop warning domain moid list:%s' % moidList)

        result = system_set.set_stopwarning_list(moidList)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"设置暂停告警失败"})

class DeviceTypeLimit(APIView):
    def get(self, request, *args, **kwargs):
        limitType = request.GET.get('limitType')
        page = request.GET.get('newPageNum')

        if limitType == None or page == None:
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        if limitType == '' or page == '':
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        logger.info('limitType:%s, page:%s' % (limitType, page))

        response = {'success': 1}
        response['data'], response['total_num'] = system_set.get_device_type_limit(limitType,page)
        return Response(response)

    def post(self, request):
        moid = request.data.get('moid')
        e164 = request.data.get('e164')
        version = request.data.get('version')
        sn = request.data.get('sn')
        ip = request.data.get('ip')
        startIP = request.data.get('startIP')
        endIP = request.data.get('endIP')
        terminalType = request.data.get('terminalType')
        mainType = request.data.get('mainType')
        subType = request.data.get('subType')
        limitType = request.data.get('limitType')
        if moid == None or moid == '':
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        # 这些参数至少要有一个不为空
        if (e164 == None or e164 == '') and (version == None or version == '') and (sn == None or sn == '') and (ip == None or ip == '') and (startIP == None or startIP == '') and (endIP == None or endIP == '') and (mainType == None or mainType == '') and (subType == None or subType == '') and (terminalType == None or terminalType == ''):
           return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        # 设置了起始IP，就必须设置结束IP
        if startIP != None and startIP != '' and (endIP == None or endIP == ''):
           return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        # 设置了结束IP，就必须设置起始IP
        if endIP != None and endIP != '' and (startIP == None or startIP == ''):
           return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        logger.info('moid:%s' % moid)
        logger.info('e164:%s' % e164)
        logger.info('version:%s' % version)
        logger.info('sn:%s' % sn)
        logger.info('ip:%s' % ip)
        logger.info('startIP:%s' % startIP)
        logger.info('endIP:%s' % endIP)
        logger.info('terminalType:%s' % terminalType)
        logger.info('mainType:%s' % mainType)
        logger.info('subType:%s' % subType)

        result = system_set.edit_device_type_limit(moid,e164,version,sn,ip,startIP,endIP,terminalType,mainType,subType,limitType)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.SERVER_ERROR,"message":"登陆权限修改失败"})

class AddDeviceTypeLimit(APIView):
    def post(self, request):
        e164 = request.data.get('e164')
        version = request.data.get('version')
        sn = request.data.get('sn')
        ip = request.data.get('ip')
        startIP = request.data.get('startIP')
        endIP = request.data.get('endIP')
        terminalType = request.data.get('terminalType')
        mainType = request.data.get('mainType')
        subType = request.data.get('subType')
        limitType = request.data.get('limitType')

        if limitType == None or limitType == '':
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        # 这些参数至少要有一个不为空
        if (e164 == None or e164 == '') and (version == None or version == '') and (sn == None or sn == '') and (ip == None or ip == '') and (startIP == None or startIP == '') and (endIP == None or endIP == '') and (mainType == None or mainType == '') and (subType == None or subType == '') and (terminalType == None or terminalType == ''):
           return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        # 设置了起始IP，就必须设置结束IP
        if startIP != None and startIP != '' and (endIP == None or endIP == ''):
           return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        # 设置了结束IP，就必须设置起始IP
        if endIP != None and endIP != '' and (startIP == None or startIP == ''):
           return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        logger.info('limitType:%s' % limitType)
        logger.info('e164:%s' % e164)
        logger.info('version:%s' % version)
        logger.info('sn:%s' % sn)
        logger.info('ip:%s' % ip)
        logger.info('startIP:%s' % startIP)
        logger.info('endIP:%s' % endIP)
        logger.info('terminalType:%s' % terminalType)
        logger.info('mainType:%s' % mainType)
        logger.info('subType:%s' % subType)

        result = system_set.add_device_type_limit(e164,version,sn,ip,startIP,endIP,terminalType,mainType,subType,limitType)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.SERVER_ERROR,"message":"登陆权限添加失败"})

class DelDeviceTypeLimit(APIView):
    def post(self, request):
        moid = request.data.get('moid')
        if moid == None or moid == '':
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

        logger.info('moid:%s' % moid)

        result = system_set.delete_device_type_limit(moid)
        if result:
            return Response({"success":1})
        else:
            return Response({"success":0,"error_code":error_code.MYSQL_ERROR,"message":"登陆权限删除失败"})

class DeviceTypeLimitCfg(APIView):
    def get(self, request, *args, **kwargs):

        response = {'success': 1}
        response['data'] = system_set.get_device_type_limit_cfg()
        return Response(response) 

    def post(self, request):
        cfgValue = request.data.get('cfgValue')
        if cfgValue == '0' or cfgValue == '1' or cfgValue == '2':
            logger.info('cfgValue:%s' % cfgValue)
            result = system_set.set_device_type_limit_cfg(cfgValue)
            if result:
                return Response({"success": 1})
            else:
                return Response({"success": 0, "error_code": error_code.MYSQL_ERROR, "message": "登陆权限删除失败"})
        else:
            return Response({'success':0,"error_code":error_code.INPUT_ERROR,'message':'参数错误'})

