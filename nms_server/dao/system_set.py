from nms_server.dao.mysql.system_set import *
from nms_server.dao.redis.system_set import *
from nms_server.dao.mysql.warning import WarningLevelForBaseInfo,WarningCode
from nms_server.dao.redis.domain import get_domain_info
from nms_server.utils import bmc
from django.db.models import Q
import logging
import uuid

logger = logging.getLogger("nms." + __name__)

def getPage( page ):
    if not page:
        page = 1
    else:
        page = int(page)

    start = (page - 1) * 10
    end = page * 10
    return start, end

# 所有域阈值获取接口
def get_resource_limit():
    limit = {}
    limit_obj = ResourceLimit.objects.values('s_pas', 's_callpair', 's_nms', 's_media_resource')
    if len(limit_obj):
        limit['s_pas'] = limit_obj[0]['s_pas']
        limit['s_callpair'] = limit_obj[0]['s_callpair']
        limit['s_nms'] = limit_obj[0]['s_nms']
        limit['s_media_resource'] = limit_obj[0]['s_media_resource']
    else:
        ResourceLimit.objects.create(s_pas=5000, s_callpair=400, s_nms=10000, s_media_resource=80)
        limit['s_pas'] = 5000
        limit['s_callpair'] = 400
        limit['s_nms'] = 10000
        limit['s_media_resource'] = 80
        set_global_server_limit(5000, 400, 10000, 80)
    logger.info('limit:%s' % limit)
    return limit

# 阈值修改接口
def set_resource_limit(limit_type, limit_data):
    
    logger.info('limit_type:%s' % limit_type)
    logger.info('limit_data:%s' % limit_data)

    try:
        limit_obj = ResourceLimit.objects.values('s_pas', 's_callpair', 's_nms', 's_media_resource')
        if limit_type == 'pas':
            ResourceLimit.objects.update(s_pas=limit_data)
            set_global_server_limit(limit_data, limit_obj[0]['s_callpair'], limit_obj[0]['s_nms'], limit_obj[0]['s_media_resource'])
        elif limit_type == 'callpair':
            ResourceLimit.objects.update(s_callpair=limit_data)
            set_global_server_limit(limit_obj[0]['s_pas'], limit_data, limit_obj[0]['s_nms'],
                                    limit_obj[0]['s_media_resource'])
        elif limit_type == 'nms':
            ResourceLimit.objects.update(s_nms=limit_data)
            set_global_server_limit(limit_obj[0]['s_pas'], limit_obj[0]['s_callpair'], limit_data,
                                    limit_obj[0]['s_media_resource'])
        elif limit_type == 'resource':
            ResourceLimit.objects.update(s_media_resource=limit_data)
            set_global_server_limit(limit_obj[0]['s_pas'], limit_obj[0]['s_callpair'], limit_obj[0]['s_nms'],
                                    limit_data)
    except Exception as e:
        logger.error(e)
        return False
    return True

# 服务域阈值获取接口
def get_server_limit(page, parentMoid):

    logger.info('parentMoid : %s' % parentMoid)

    # 获取查询页码
    start,end = getPage( page )
    
    server_limit_list = []
    server_limit_count = 0
    try:
        result = get_physical_server_limit(parentMoid, start, 10)
        server_limit_count = result['total_count']
        server_limit_list = result['p_servers']
    except Exception as e:
        logger.error(e)
        pass
    logger.info('server_limit_list:%s' % server_limit_list)
    return server_limit_list, server_limit_count

# 服务域阈值修改接口
def set_servers_limit(deviceMoid, cpu, memory, port, disk, diskwritespeed, rateofflow):

    logger.info('set_servers_limit')
    logger.info('cpu:%s, memory:%s, port:%s, disk:%s, diskwritespeed:%s, rateofflow:%s'%( cpu,memory,port,disk,diskwritespeed,rateofflow))
    # 更新mysql
    try:
        servers_limit_info = ServerResourceLimit.objects.get(device_moid=deviceMoid)
        servers_limit_info.cpu = cpu
        servers_limit_info.memory = memory
        servers_limit_info.port = port
        servers_limit_info.disk = disk
        servers_limit_info.diskwritespeed = diskwritespeed
        servers_limit_info.rateofflow = rateofflow
        servers_limit_info.save()
    except Exception as e:
        logger.error(e)
        ServerResourceLimit.objects.create(device_moid=deviceMoid, cpu=cpu, memory=memory, port=port, diskwritespeed=diskwritespeed, rateofflow=rateofflow)

    # 更新redis
    try:
        set_physical_server_limit(deviceMoid, cpu, disk, memory, port, diskwritespeed, rateofflow)
    except Exception as e:
        logger.error(e)
    
    return True


# 设备配置列表获取接口
def get_device_config(terminalType, terminalModel, page):
    
    logger.info('[get_device_config] terminalType:%s, terminalModel:%s, page:%s' % (terminalType, terminalModel, page))

    # 获取查询页码
    start,end = getPage( page )

    terminal_type_list = []
    total_num = 0
    if terminalModel == '':
        if terminalType == 'all':
            terminal_type_list = TerminalType.objects.all()[start:end]
            total_num = TerminalType.objects.all().count()
            
        else:
            terminal_type_list = TerminalType.objects.filter(terminal_type=terminalType)[start:end]
            total_num = TerminalType.objects.filter(terminal_type=terminalType).count()
            
    else:
        if terminalType == 'all':
            terminal_type_list = TerminalType.objects.filter(Q(name__icontains=terminalModel) | Q(product_name__icontains=terminalModel))[start:end]
            total_num = TerminalType.objects.filter(Q(name__icontains=terminalModel) | Q(product_name__icontains=terminalModel)).count()
            
        else:
            terminal_type_list = TerminalType.objects.filter(Q(name__icontains=terminalModel) | Q(product_name__icontains=terminalModel), terminal_type=terminalType)[start:end]
            total_num = TerminalType.objects.filter(Q(name__icontains=terminalModel) | Q(product_name__icontains=terminalModel), terminal_type=terminalType).count()

    device_config = []
    for value in terminal_type_list:
        if value.terminal_type == '0':
            device_config.append({'name': value.name, 'terminal_type': '软件',
                                  'device_tag': value.device_tag, 'product_name': value.product_name,
                                })
        elif value.terminal_type == '1':
            device_config.append({'name': value.name, 'terminal_type': '硬件',
                                  'device_tag': value.device_tag, 'product_name': value.product_name,
                                  })
        elif value.terminal_type == '2':
            device_config.append({'name': value.name, 'terminal_type': '外设',
                                  'device_tag': value.device_tag, 'product_name': value.product_name,
                                  })

    logger.info('device_config:%s' % device_config)
    logger.info('get_device_num:%s' % total_num)
    return device_config, total_num

def add_device_config(mainModel, terminalType, deviceTag, productName, platformType=2):
    try:
        # 子型号去重复
        TerminalTypeResult = TerminalType.objects.filter(product_name=productName)
        if len(TerminalTypeResult):
            return 1

        # 外设类型不需要上报bmc
        if terminalType == '2':
            # 添加子型号
            TerminalType.objects.update_or_create(name=mainModel,
                                                  terminal_type=terminalType,
                                                  device_tag=deviceTag,
                                                  product_name=productName)

            # 子型号添加到redis里面
            add_terminal_type(productName)
            return 0
        else:
            # 查询这个主型号下的子型号数量
            TerminalTypeResult = TerminalType.objects.filter(name=mainModel)

            # 如果只有一个子型号，则通知bmc添加这个主型号
            # 如果有多个子型号，则通知bmc更新这个主型号
            if len(TerminalTypeResult) == 0:
                logger.info("[add_device_config] add the main model from bmc: %s" % mainModel)

                result = bmc.add_device_type(mainModel, terminalType, deviceTag, platformType)
                if result:
                    TerminalType.objects.update_or_create(name=mainModel,
                                                          terminal_type=terminalType,
                                                          device_tag=deviceTag,
                                                          product_name=productName,
                                                          platform_type=platformType)

                    # 子型号添加到redis里面
                    add_terminal_type(productName)

                    return 0
                else:
                    return 2
            else:
                subTypeList = []

                # 先把数据库里面的型号都添加上
                for value in TerminalTypeResult:
                    subTypeList.append({'terminalType': value.terminal_type, 'deviceTag': value.device_tag, 'platformType': value.platform_type})

                # 再把新增加的这个也加上
                subTypeList.append({'terminalType': terminalType, 'deviceTag': deviceTag, 'platformType': platformType})

                logger.info("[add_device_config] edit the main model from bmc")
                logger.info("[add_device_config] main model : %s" % mainModel)
                logger.info("[add_device_config] sub type : %s" % subTypeList)

                result = bmc.edit_device_type(mainModel,subTypeList)
                if result:
                    TerminalType.objects.update_or_create(name=mainModel,
                                                          terminal_type=terminalType,
                                                          device_tag=deviceTag,
                                                          product_name=productName,
                                                          platform_type=platformType)
                    # 子型号添加到redis里面
                    add_terminal_type(productName)

                    return 0
                else:
                    return 2

    except Exception as e:
        logger.error(e)
        return 2


# 删除设备配置数据
def delete_device_config(mainModel, productName):
    try:
        # 判断该型号是否为外设
        obj = TerminalType.objects.get(name=mainModel, product_name=productName)

        if obj.terminal_type == '2':
            TerminalType.objects.get(name=mainModel, product_name=productName).delete()
            return True
        else:
            # 查询这个主型号下是否还有子型号
            TerminalTypeResult = TerminalType.objects.filter(name=mainModel)

            # 如果没有其他子型号了，则给通知bmc删除这个主型号
            # 否则通知bmc更新这个主型号
            if len(TerminalTypeResult) == 1:
                logger.info("[delete_device_config] delete the main model from bmc: %s" % mainModel)
                result = bmc.delete_device_type(mainModel)
                if result:
                    # 从网管数据库删除该子型号
                    TerminalType.objects.get(name=mainModel, product_name=productName).delete()

                    # 从redis删除该子型号
                    del_terminal_type(productName)
                    return True
                else:
                    return False
            else:
                subTypeList = []
                for value in TerminalTypeResult:
                    if value.product_name != productName:
                        subTypeList.append({'terminalType': value.terminal_type, 'deviceTag': value.device_tag, 'platformType': 2})

                logger.info("[delete_device_config] edit the main model from bmc")
                logger.info("[delete_device_config] main model : %s" % mainModel)
                logger.info("[delete_device_config] sub type : %s" % subTypeList)
                result = bmc.edit_device_type(mainModel,subTypeList)
                if result:
                    # 从网管数据库删除该子型号
                    TerminalType.objects.get(name=mainModel, product_name=productName).delete()

                    # 从redis删除该子型号
                    del_terminal_type(productName)
                    return True
                else:
                    return False

    except Exception as e:
        logger.error(e)
        return False



# 设备型号数据列表
def get_terminal_type_list():
    logger.info('[get_terminal_type_list] start...')
    result = TerminalType.objects.all()
    logger.info('[get_terminal_type_list] terminal type : %s' % result)
    data = []
    for value in result:
        data.append({'name': value.name,  # 主型号
                     'terminal_type': value.terminal_type,
                     'device_tag': value.device_tag, 
                     'product_name': value.product_name}) # 子型号
    return data

# 检测告警码
def get_warning_code(user_moid, domain_moid):
    sub_warning_code = []
    try:
        sub_warning_obj = SubWarningCode.objects.filter(user_id=user_moid, domain_moid=domain_moid)
        for value in sub_warning_obj:
            sub_warning_code.append({'code': value.sub_code})
    except Exception as e:
        logger.error(e)
        sub_warning_code.append({'code': ''})
        pass
    logger.info('sub_warning_code:%s' % sub_warning_code)
    return sub_warning_code

#设置告警码
def set_warning_code(user_moid, domain_moid, code):
    try:
        SubWarningCode.objects.filter(user_id=user_moid, domain_moid=domain_moid).delete()
        if len(code):
            for value in code:
                SubWarningCode.objects.create(user_id=user_moid, domain_moid=domain_moid, sub_code=value['code'])
    except Exception as e:
        logger.error(e)
        return False

    return True

# 获取告警信息列表
def get_warning_notify(domain_moid,user_moid,page):

    # 获取查询页码
    start,end = getPage( page )
    warning_notify_list = []
    try:
        result = WarningNotify.objects.filter(user_moid=user_moid, domain_moid=domain_moid)[start:end]
        total_num = WarningNotify.objects.filter(user_moid=user_moid, domain_moid=domain_moid).count()

        for value in result:
            warning_notify_list.append({'id': value.id, 'domain_moid': value.domain_moid, 'name': value.name,
                                        'warning': value.code_list, 'email': value.email, 'phone': value.phone, 'wechat': value.wechat})
    except Exception as e:
        logger.error(e)
        pass
    logger.info('warning_notify_list:%s' % warning_notify_list)
    logger.info('warning_notify_num:%s' % total_num)
    return warning_notify_list, total_num


# 新增告警信息列表
def set_warning_notify(name, email, phone, wechat, code_list, domain_moid, user_moid):
    try:
        notify = WarningNotify.objects.create(domain_moid=domain_moid, user_moid=user_moid, name=name,
                                     email=email, phone=phone, wechat=wechat, code_list=code_list)
        notify.save()
        id = notify.id
        add_warning_notify_info(domain_moid, email, phone, wechat, code_list, id)
    except Exception as e:
        logger.error(e)
        return False

    return True


# 删除告警信息列表
def delete_warning_notify(id):
    try:
        warning_notify_obj = WarningNotify.objects.get(id=id)
        domain_moid = warning_notify_obj.domain_moid
        id = warning_notify_obj.id
        del_warning_notify_info(domain_moid, id)
        warning_notify_obj.delete()
    except Exception as e:
        logger.error(e)
        return False

    return True

# 编辑告警信息列表
def edit_warning_notify(notifyID, phone, email, wechat, code_list):
    try:
        warning_notify_obj = WarningNotify.objects.get(id=notifyID)
        warning_notify_obj.phone = phone
        warning_notify_obj.email = email
        warning_notify_obj.wechat = wechat
        warning_notify_obj.code_list = code_list
        warning_notify_obj.save()
        domain_moid = warning_notify_obj.domain_moid
        id = warning_notify_obj.id
        set_warning_notify_info(domain_moid, email, phone, wechat, code_list, id)
    except Exception as e:
        logger.error(e)
        return False

    return True

# 编辑告警信息列表
def get_warning_level(user_moid, domain_moid):
    warning_level = {}
    try:
        warning_notify_obj = WarningLevelForBaseInfo.objects.get(user_moid=user_moid, domain_moid=domain_moid)
        warning_level['serverlevel'] = warning_notify_obj.server_level
        warning_level['terminallevel'] = warning_notify_obj.terminal_level
    except Exception as e:
        logger.error(e)
        WarningLevelForBaseInfo.objects.create(domain_moid=domain_moid, user_moid=user_moid, server_level="critical", terminal_level="critical")
        warning_level['serverlevel'] = "critical"
        warning_level['terminallevel'] = "critical"
        pass
    logger.info('warning_level:%s' % warning_level)
    return warning_level

def edit_warning_level(user_moid, domain_moid, warning_type, level):
    if warning_type == 'server':
        try:
            warning_notify_obj = WarningLevelForBaseInfo.objects.get(user_moid=user_moid, domain_moid=domain_moid)
            warning_notify_obj.server_level = level
            warning_notify_obj.save()
        except Exception as e:
            logger.error(e)
            return False
    elif warning_type == 'terminal':
        try:
            warning_notify_obj = WarningLevelForBaseInfo.objects.get(user_moid=user_moid, domain_moid=domain_moid)
            warning_notify_obj.terminal_level = level
            warning_notify_obj.save()
        except Exception as e:
            logger.error(e)
            return False
    else:
        return False

    return True

# 告警码接口
def get_warning_tree():
    response = []

    other = {'code': 4, 'name': '其它'}
    mcu_warning = {'code': 3, 'name': 'MCU告警'}
    server_warning = {'code': 2, 'name': '服务器设备告警'}
    terminal_warning = {'code': 1, 'name': '终端设备告警'}

    other_list = []
    mcu_warning_list = []
    server_warning_list = []
    terminal_warning_list = []

    warning_code_list = WarningCode.objects.all()
    for value in warning_code_list:
        if value.type == "MCU告警":
            mcu_warning_list.append({'name': value.name, 'level': value.level, 'code': value.code, 'type': 'mcu'})
        elif value.type == "其他":
            other_list.append({'name': value.name, 'level': value.level, 'code': value.code, 'type': 'other'})
        elif value.type == "服务器设备告警":
            server_warning_list.append({'name': value.name, 'level': value.level, 'code': value.code, 'type': 'server'})
        elif value.type == "终端设备告警":
            terminal_warning_list.append({'name': value.name, 'level': value.level, 'code': value.code, 'type': 'terminal'})

    other['children'] = other_list
    mcu_warning['children'] = mcu_warning_list
    server_warning['children'] = server_warning_list
    terminal_warning['children'] = terminal_warning_list

    response.append(other)
    response.append(mcu_warning)
    response.append(server_warning)
    response.append(terminal_warning)
    logger.info('warningcode:%s' % response)
    return response

# 暂停告警获取接口
def get_stopwarning_list(page):
    # 获取查询页码
    start,end = getPage(page)

    result = StopWarning.objects.all()[start:end]
    total_count = StopWarning.objects.all().count()
    result_all = StopWarning.objects.all()
    domain_list = []
    for value in result:
        domain_info = get_domain_info(value.moid)
        logger.info('domain moid:%s' % value.moid)
        logger.info('domain_info:%s' % domain_info)
        domain_list.append({'id': value.id, 'moid': value.moid,'name':domain_info['name']})

    list_all = []
    for value in result_all:
        list_all.append({'moid': value.moid})
    logger.info('stop warning domain moid list:%s' % domain_list)
    logger.info('stop warning domain count:%s' % total_count)
    return domain_list, total_count, list_all

# 暂停告警设置接口
def set_stopwarning_list(moidList):
    try:
        if len(moidList):
            StopWarning.objects.all().delete()
            for value in moidList:
                StopWarning.objects.create(moid=value)
        else:
            StopWarning.objects.all().delete()
        moid_list = [stop_warning.moid for stop_warning in StopWarning.objects.all()]
        init_warning_stop(moid_list)
    except Exception as e:
        logger.error(e)
        return False

    return True

# 获取终端权限配置列表
def get_device_type_limit(limitType, page):
    
    logger.info('[get_device_type_limit] limitType:%s, page:%s' % (limitType,  page))

    # 获取查询页码
    start,end = getPage( page )

    device_type_limit_list = []
    total_num = 0

    try:
        limit_list = TerminalTypeLimit.objects.filter(limit_type=limitType)[start:end]
        total_num = TerminalTypeLimit.objects.filter(limit_type=limitType).count()
        for value in limit_list:
            device_type_limit_list.append({'moid': value.moid,
                                           'e164': value.e164,
                                           'version': value.version,
                                           'sn': value.sn,
                                           'ip': value.start_ip + '-' + value.end_ip if value.ip == '' and (value.start_ip != '' or value.end_ip != '') else value.ip,
                                           'start_ip': value.start_ip,
                                           'end_ip': value.end_ip,
                                           'terminal_type': value.terminal_type,
                                           'main_type': value.main_type,
                                           'sub_type': value.sub_type,
                                           'limit_type': value.limit_type})
    except Exception as e:
        logger.error(e)
        pass
    logger.info('device_type_limit_list:%s' % device_type_limit_list)
    logger.info('get_device_num:%s' % total_num)
    return device_type_limit_list, total_num



# 编辑终端权限配置
def edit_device_type_limit(moid,e164,version,sn,ip,startIP,endIP,terminalType,mainType,subType,limitType):
    try:
        # 通知bmc更新
        result = bmc.edit_device_type_limit(moid,e164,version,sn,ip,startIP,endIP,terminalType,mainType,subType,limitType)

        # bmc更新成功了，再更新网管数据库
        if result:
            LimitResult = TerminalTypeLimit.objects.get(moid=moid)
            if LimitResult:
                LimitResult.e164 = e164
                LimitResult.version = version
                LimitResult.sn = sn
                LimitResult.ip = ip
                LimitResult.start_ip = startIP
                LimitResult.end_ip = endIP
                LimitResult.terminal_type = terminalType
                LimitResult.main_type = mainType
                LimitResult.sub_type = subType
                LimitResult.limit_type = limitType
                LimitResult.save()
                return True
            else:
                return False
        else:
            return False
        
    except Exception as e:
        logger.error(e)
        return False

# 添加终端权限配置
def add_device_type_limit(e164,version,sn,ip,startIP,endIP,terminalType,mainType,subType,limitType):
    try:
        # 随机生成一个moid,用来唯一标识这条数据
        moid = str(uuid.uuid1())
        
        # 通知bmc更新
        result = bmc.add_device_type_limit(moid,e164,version,sn,ip,startIP,endIP,terminalType,mainType,subType,limitType)
        
        # bmc更新成功了，再更新网管数据库
        if result:
            TerminalTypeLimit.objects.update_or_create(moid = moid,
                                                       e164 = e164,
                                                       version = version,
                                                       sn = sn,
                                                       ip = ip,
                                                       start_ip = startIP,
                                                       end_ip = endIP,
                                                       terminal_type =terminalType,
                                                       main_type = mainType,
                                                       sub_type = subType,
                                                       limit_type = limitType)
            return True
        else:
            return False

    except Exception as e:
        logger.error(e)
        return False

# 删除终端权限配置
def delete_device_type_limit(moid):
    try:
        # 通知bmc更新
        result = bmc.delete_device_type_limit(moid)

        # bmc更新成功了，再更新网管数据库
        if result:
            TerminalTypeLimit.objects.get(moid=moid).delete()
            return True
        else:
            return False

    except Exception as e:
        logger.error(e)
        return False

def get_device_type_limit_cfg():
    try:
        CfgResult = TerminalTypeLimitCfg.objects.values('value')
        if len(CfgResult):
            logger.info("the cfg value is : %s" % CfgResult[0]['value'])
            return CfgResult[0]['value']
        else:
            logger.info("create device type limit cfg")
            TerminalTypeLimitCfg.objects.create(value=0)
            return 0
    except Exception as e:
        logger.error(e)
        return 0

def set_device_type_limit_cfg(cfgValue):
    try:
        # 通知bmc更新
        result = bmc.set_device_type_limit_cfg(cfgValue)

        # bmc更新成功了，再更新网管数据库
        if result:
            CfgResult = TerminalTypeLimitCfg.objects.values('value')
            if len(CfgResult) == 1:
                TerminalTypeLimitCfg.objects.update(value=cfgValue)
                return True
            else:
                logger.error("there are more than one record")
                return False
        else:
            return False

    except Exception as e:
        logger.error(e)
        return False

