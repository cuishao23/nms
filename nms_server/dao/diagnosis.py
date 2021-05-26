import logging
import os
from nms_server.dao.mysql.diagnosis import CaptureDevice,CaptureFile
from nms_server.dao.redis.device import get_physical_server_info, get_terminal_detail_info
from nms_server.utils.date_conversion import get_time
from nms_server.utils.redis import distributed_lock, distributed_unlock
from nms_server.settings import KDFS, REQUESTS_TIMEOUT
import requests
import random
from django.core.cache import cache

logger = logging.getLogger("nms." + __name__)

def getPage(page):
    if not page:
        page = 1
    else:
        page = int(page)

    start = (page - 1) * 5
    end = page * 5
    return start, end

def get_capture_device(userMoid):

    result = CaptureDevice.objects.filter(user_moid=userMoid)
    total_num = CaptureDevice.objects.filter(user_moid=userMoid).count()

    device_list = []
    if len(result):
        for value in result:
            device_list.append({'id': value.id, 
                                'user_moid': value.user_moid, 
                                'device_moid': value.device_moid, 
                                'device_category': value.device_category,
                                'device_name': value.device_name,
                                'device_type': value.device_type, 
                                'netcard': value.netcard})
    return device_list, total_num


def edit_capture_device(deviceID, deviceType, netcard):
    try:
        capture_device_obj = CaptureDevice.objects.get(id=deviceID)
        capture_device_obj.device_type = deviceType
        capture_device_obj.netcard = netcard
        capture_device_obj.save()
    except Exception as e:
        logger.error(e)
        return False

    return True

def add_capture_device(userMoid, deviceCategory, deviceMoid, deviceType, netcard):
   
    deviceName = ''
    deviceIP = ''

    if deviceCategory == 'server':
        deviceInfo = get_physical_server_info(deviceMoid)
        logger.info('deviceInfo : %s' % deviceInfo)

        deviceName = deviceInfo.get('name','')
        deviceIP = deviceInfo.get('ip','')

    elif deviceCategory == 'terminal':
        # 返回的是一个列表，因为终端可能有多个类型
        deviceList = get_terminal_detail_info(deviceMoid) 
        logger.info('deviceList : %s' % deviceList)

        for value in deviceList:
            if deviceType == value.get('type_ver',''):
                deviceName = value.get('name','')
                deviceIP = value.get('ip','')

    try:
        result = CaptureDevice.objects.filter(user_moid=userMoid,device_moid=deviceMoid)

        # 不能为同一个设备，重复添加抓包对象
        if len(result) == 0:
            CaptureDevice.objects.update_or_create(user_moid=userMoid,
                                                   device_moid=deviceMoid,
                                                   device_name=deviceName, 
                                                   device_ip=deviceIP, 
                                                   device_category=deviceCategory, 
                                                   device_type=deviceType, 
                                                   netcard=netcard)
        else:
            logger.error("[add_capture_device] Capture device repeated")
            return 2

    except Exception as e:
        logger.error(e)
        return 1
        
    return 0

def del_capture_device(deviceID):
    try:
        CaptureDevice.objects.filter(id=deviceID).delete()
    except Exception as e:
        logger.error(e)
        return False

    return True

def get_capture_file(userMoid,page):
    
    start,end = getPage(page)
    logger.info('start : %s, end : %s' %(start,end))

    result = CaptureFile.objects.filter(user_moid=userMoid).order_by("-create_time")[start:end]
    total_num = CaptureFile.objects.filter(user_moid=userMoid).count()

    capture_file_list = []
    if len(result):
        for value in result:
            capture_file_list.append({'id': value.id, 
                                      'user_moid': value.user_moid, 
                                      'device_moid': value.device_moid, 
                                      'device_name': value.device_name,
                                      'file_name': value.file_name,
                                      'file_size': value.file_size, 
                                      'create_time': get_time(value.create_time)})
    return capture_file_list, total_num

def del_capture_file(fileID):
    try:
        captureFile = CaptureFile.objects.get(id=fileID)
        

        ip = KDFS['HOST']
        port = KDFS['PORT']

        logger.info('[del_capture_file] kdfs ip = %s' % ip)
        logger.info('[del_capture_file] kdfs port = %s' % port)
        logger.info('[del_capture_file] file name = %s' % captureFile.file_name)

        delete_url = "http://"+ip+":"+port+"/api/inner/kdfs/v1"
        
        logger.info('[del_capture_file] delete_url=%s' % delete_url)

        headers = {
            'path': os.path.join(captureFile.device_moid,captureFile.file_name),
            'type': 'file',
            'home': 'platformLog'
        }
        
        result = requests.delete(delete_url, headers=headers, timeout=REQUESTS_TIMEOUT)
        json_data = result.json()
        logger.info('[del_capture_file] result=%s' % json_data)

        # 文件服务器上的文件删除后，再删除本地数据库的数据
        if json_data.get("success","0") == "1" or json_data.get("errorcode") == "-101":
            CaptureFile.objects.get(id=fileID).delete()

    except Exception as e:
        logger.error(e)
        return False

    return True


def add_capture_file(userMoid, deviceMoid, fileName, size, createTime):
    logger.info("[add_capture_file] userMoid : %s"%userMoid)
    logger.info("[add_capture_file] deviceMoid : %s"%deviceMoid)
    logger.info("[add_capture_file] fileName : %s"%fileName)
    logger.info("[add_capture_file] size : %s"%size)
    logger.info("[add_capture_file] createTime : %s"%createTime)

    try:
        lock_name = 'capture_lock:' + userMoid
        if distributed_lock(lock_name):
            try:
                captureDeviceObj = CaptureFile.objects.filter(file_name=fileName, device_moid=deviceMoid, user_moid=userMoid)
                logger.info("captureDeviceObj count=%s"%captureDeviceObj.count())
                if (captureDeviceObj.count() == 0):
                    captureDevice = CaptureDevice.objects.get(user_moid=userMoid,device_moid=deviceMoid)
                    capturefile = CaptureFile(
                        user_moid=userMoid,
                        device_moid=deviceMoid,
                        device_name=captureDevice.device_name,
                        file_name=fileName,
                        file_size=size,
                        create_time=createTime
                    )
                    capturefile.save()
                    logger.info("[add_capture_file] success")
            except Exception as e:
                logger.error("[add_capture_file] %s" % e)
            finally:
                distributed_unlock(lock_name)
        else:
            logger.info("[add_capture_file] lock error")

    except Exception as e:
        logger.error("[add_capture_file] failed, reason : %s" % e)


def updata_capture_file(userMoid, deviceMoid, fileName, size):

    logger.info("[updata_capture_file] userMoid : %s"%userMoid)
    logger.info("[updata_capture_file] deviceMoid : %s"%deviceMoid)
    logger.info("[updata_capture_file] fileName : %s"%fileName)
    logger.info("[updata_capture_file] size : %s"%size)

    try:
        captureDevice = CaptureFile.objects.get(user_moid=userMoid, device_moid=deviceMoid, file_name=fileName)

        if captureDevice.file_size == 0:
            captureDevice.file_size = size
            captureDevice.save()
            logger.info("[updata_capture_file] success")
    except Exception as e:
        logger.error("[updata_capture_file] failed, reason : %s"%e)