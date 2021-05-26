import logging
import requests
import json
from django.conf import settings
from nms_server.utils.sso import get_account_token

DEVICE_URL = 'http://{ip}:{port}/apiCore/bmc/device'
DEVICE_LIMIT_URL = 'http://{ip}:{port}/apiCore/bmc/deviceLimit'
BMC_CFG_URL = 'http://{ip}:{port}/apiCore/bmc/sysCfg'

logger = logging.getLogger("nms." + __name__)


# platform_type: 网管新增均为自建&租赁
def add_device_type(mainModel, terminalType, deviceTag, platformType=2):
    try:
        logger.info("[add_device_type] mainModel :%s" % mainModel)
        logger.info("[add_device_type] terminalType :%s" % terminalType)
        logger.info("[add_device_type] deviceTag :%s" % deviceTag)

        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = DEVICE_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[add_device_type] url :%s" % url)

        Params  = {'account_token': account_token}
        Headers = {'Content-Type':"application/json"}
        Data = {"name": mainModel,
                "data": [
                {
                    "terminalType": terminalType,
                    "deviceTag": deviceTag,
                    "platformType": platformType
                }]
              }

        result = requests.post(url, params=Params,headers=Headers, data=json.dumps(Data), timeout=settings.REQUESTS_TIMEOUT)
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[add_device_type] result :%s" % resultData)

            if resultData.get('success') == 1:
                logger.error('[add_device_type] success!')
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[add_device_type] status_code :%s" % result.status_code)
            return False
            
    except Exception as e:
        logger.error('[add_device_type] error : %s' % e)
        return False

def edit_device_type(mainModel,subTypeList):
    try:
        logger.info("[edit_device_type] mainModel :%s" % mainModel)
        logger.info("[edit_device_type] subTypeList :%s" % subTypeList)

        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = DEVICE_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[edit_device_type] url :%s" % url)

        Params  = {'account_token': account_token}
        Headers = {'Content-Type':"application/json"}
        Data = {"name": mainModel,
                "data": subTypeList
               }

        result = requests.put(url, params=Params,headers=Headers, data=json.dumps(Data, timeout=settings.REQUESTS_TIMEOUT))
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[edit_device_type] result :%s" % resultData)

            if resultData.get('success') == 1:
                logger.error('[edit_device_type] success!')
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[edit_device_type] status_code :%s" % result.status_code)
            return False

    except Exception as e:
        logger.error('[edit_device_type] error : %s' % e)
        return False

def delete_device_type(mainModel):
    try:
        logger.info("[delete_device_type] mainModel :%s" % mainModel)

        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = DEVICE_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[delete_device_type] url :%s" % url)

        Params  = {'account_token': account_token,'name':mainModel}
        Headers = {'Content-Type':"application/json"}

        result = requests.delete(url, params=Params, headers=Headers, timeout=settings.REQUESTS_TIMEOUT)
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[delete_device_type] result :%s" % resultData)
            
            if resultData.get('success') == 1:
                logger.error('[delete_device_type] success!')
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[delete_device_type] status_code :%s" % result.status_code)
            return False

    except Exception as e:
        logger.error('[delete_device_type] error : %s' % e)
        return False

def edit_device_type_limit(moid,e164,version,sn,ip,startIp,endIp,terminalType,mainType,subType,limitType):
    try:

        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = DEVICE_LIMIT_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[add_device_type_limit] url :%s" % url)

        Params  = {'account_token':account_token}
        Headers = {'Content-Type':"application/json"}
        Data = {"moid": moid,
                "e164": e164,
                "version": version,
                "sn": sn,
                "ip": ip,
                "startIp": startIp,
                "endIp": endIp,
                "terminalType": terminalType,
                "mainType": mainType,
                "subType": subType,
                "limitType": limitType
               }
        result = requests.put(url, params=Params,headers=Headers,data=json.dumps(Data), timeout=settings.REQUESTS_TIMEOUT)
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[edit_device_type_limit] result :%s" % resultData)

            if resultData.get('success') == 1:
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[edit_device_type_limit] status_code :%s" % result.status_code)
            return False

    except Exception as e:
        logger.error('[edit_device_type_limit] error! %s' % e)
        return False

def add_device_type_limit(moid,e164,version,sn,ip,startIp,endIp,terminalType,mainType,subType,limitType):
    try:
        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = DEVICE_LIMIT_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[add_device_type_limit] url :%s" % url)

        Params  = {'account_token':account_token}
        Headers = {'Content-Type':"application/json"}
        Data = {"moid": moid,
                "e164": e164,
                "version": version,
                "sn": sn,
                "ip": ip,
                "startIp": startIp,
                "endIp": endIp,
                "terminalType": terminalType,
                "mainType": mainType,
                "subType": subType,
                "limitType": limitType
               }

        result = requests.post(url, params=Params,headers=Headers,data=json.dumps(Data), timeout=settings.REQUESTS_TIMEOUT)
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[add_device_type_limit] result :%s" % resultData)

            if resultData.get('success') == 1:
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[add_device_type_limit] status_code :%s" % result.status_code)
            return False

    except Exception as e:
        logger.error('[add_device_type_limit] error! %s' % e)
        return False

def delete_device_type_limit(moid):
    try:
        logger.info("[delete_device_type_limit] moid :%s" % moid)

        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = DEVICE_LIMIT_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[delete_device_type_limit] url :%s" % url)

        Params  = {'account_token':account_token,'moid':moid}
        Headers = {'Content-Type':"application/json"}

        result = requests.delete(url, params=Params,headers=Headers, timeout=settings.REQUESTS_TIMEOUT)
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[delete_device_type_limit] result :%s" % resultData)

            if resultData.get('success') == 1:
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[delete_device_type_limit] status_code :%s" % result.status_code)
            return False

    except Exception as e:
        logger.error('[delete_device_type_limit] error! %s' % e)
        return False

def set_device_type_limit_cfg(cfgValue):
    try:
        logger.info("[set_device_type_limit_cfg] cfgValue :%s" % cfgValue)
        
        account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
        url = BMC_CFG_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        logger.info("[set_device_type_limit_cfg] url :%s" % url)

        Params  = {'account_token':account_token}
        Headers = {'Content-Type':"application/json"}
        Data = {'cfgKey':'limit.mode',
                'cfgValue':cfgValue,
                'description':''}

        result = requests.put(url, params=Params,headers=Headers,data=json.dumps(Data), timeout=settings.REQUESTS_TIMEOUT)
        if result.status_code == 200:
            resultData = result.json()
            logger.info("[set_device_type_limit_cfg] result :%s" % resultData)

            if resultData.get('success') == 1:
                return True
            else:
                logger.error(resultData)
                return False
        else:
            logger.error("[set_device_type_limit_cfg] status_code : %s" % result.status_code)
            return False
            
    except Exception as e:
        logger.error('[set_device_type_limit_cfg] error! %s' % e)
        return False