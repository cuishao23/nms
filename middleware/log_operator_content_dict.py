import logging
from django.urls.resolvers import get_resolver
from nms_server.dao.mysql.opr_log import Log

logger = logging.getLogger("nms." + __name__)

url_type = [
    {
        'url': '/nms/logout/',
        'name': '退出',
        'level': 'normal',
        'type': 'logout',
    },
    {
        'url': '/nms/sus/addverinfo/',
        'name': '上传版本',
        'level': 'important',
        'type': 'sus',
    },
    {
        'url': '/nms/sus/editver/',
        'name': '编辑版本',
        'level': 'important',
        'type': 'sus',
    },
    {
        'url': '/nms/sus/deletever/',
        'name': '删除版本',
        'level': 'important',
        'type': 'sus',
    },
    {
        'url': '/nms/system_set/resourcelimit/',
        'name': '修改系统阈值',
        'level': 'important',
        'type': 'limitset',
    },
    {
        'url': '/nms/system_set/serverslimit/',
        'name': '修改服务器阈值',
        'level': 'important',
        'type': 'limitset',
    },
    {
        'url': '/nms/system_set/subwarningcode/',
        'name': '修改订阅告警项',
        'level': 'normal',
        'type': 'warningset',
    },
    {
        'url': '/nms/system_set/warningnotify/',
        'name': '添加告警通知',
        'level': 'normal',
        'type': 'warningset',
    },
    {
        'url': '/nms/system_set/editwarningnotify/',
        'name': '编辑告警通知',
        'level': 'normal',
        'type': 'warningset',
    },
    {
        'url': '/nms/system_set/delwarningnotify/',
        'name': '删除告警通知',
        'level': 'normal',
        'type': 'warningset',
    },
    {
        'url': '/nms/system_set/warninglevel/',
        'name': '修改告警级别',
        'level': 'important',
        'type': 'warningset',
    },
    {
        'url': '/nms/system_set/stopwarning/',
        'name': '设置暂停告警',
        'level': 'important',
        'type': 'warningset',
    },
    {
        'url': '/nms/system_set/deldeviceconfig/',
        'name': '删除终端设备类型',
        'level': 'important',
        'type': 'terminaltype',
    },
    {
        'url': '/nms/system_set/deviceconfig/',
        'name': '添加终端设备类型',
        'level': 'important',
        'type': 'terminaltype',
    },
    {
        'url': '/nms/system_set/devicetypelimit/',
        'name': '修改终端登录权限',
        'level': 'important',
        'type': 'terminallimit',
    },
    {
        'url': '/nms/system_set/adddevicetypelimit/',
        'name': '添加终端登录权限',
        'level': 'important',
        'type': 'terminallimit',
    },
    {
        'url': '/nms/system_set/deldevicetypelimit/',
        'name': '删除终端登录权限',
        'level': 'important',
        'type': 'terminallimit',
    },
    {
        'url': '/nms/system_set/devicetypelimitcfg/',
        'name': '终端登录权限配置',
        'level': 'important',
        'type': 'terminallimit',
    },
    {
        'url': '/nms/diagnosis/capturedevice/',
        'name': '修改抓包对象',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/addcapturedevice/',
        'name': '添加抓包对象',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/delcapturedevice/',
        'name': '删除抓包对象',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/startcapturedevice/',
        'name': '开始抓包',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/stopcapturedevice/',
        'name': '结束抓包',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/capturefile/',
        'name': '删除抓包文件',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/downloadcapturefile/',
        'name': '下载抓包文件',
        'level': 'normal',
        'type': 'capture',
    },
    {
        'url': '/nms/diagnosis/capturelog/',
        'name': '日志列表获取',
        'level': 'normal',
        'type': 'log',
    },
    {
        'url': '/nms/diagnosis/downloadcapturelog/',
        'name': '日志文件下载',
        'level': 'normal',
        'type': 'log',
    },
    {
        'url': '/nms/diagnosis/serverdiagnose/',
        'name': '服务器诊断',
        'level': 'normal',
        'type': 'diagnose',
    },
    {
        'url': '/nms/diagnosis/terminaldiagnose/',
        'name': '终端诊断',
        'level': 'normal',
        'type': 'diagnose',
    },
]

class VerifyUrlSaveContent(object):
    logger.info('VerifyUrlSaveContent')
    def __init__(self, request, response):
        self._request = request
        self._response = response

    def parse_detail(self, path):
        # 校验
        detail = {}
        if path is not None:
            user = getattr(self._request, 'sso_user', None)
            if user is not None:
                user_moid = user['data']['moid']
                user_name = user['data']['name']

                # 用户域管理员
                if user['data']['userDomainMoid'] != None:
                    domain_moid = user['data']['userDomainMoid']
                # 服务域管理员
                elif user['data']['serviceDomainMoid'] != None:
                    domain_moid = user['data']['serviceDomainMoid']

                logger.info('[VerifyUrlSaveContent] domain_moid : %s, user_moid : %s, user_name : %s' % (domain_moid,user_moid,user_name))
            else:
                logger.error('[VerifyUrlSaveContent] 未登陆用户')
                return None

            ip = self._request.META.get('HTTP_X_REAL_IP', " ")
            logger.info('[VerifyUrlSaveContent] user ip : %s' % ip)

            logger.info('[VerifyUrlSaveContent] path : %s' % path)

            # TODO 修改匹配, 提高效率
            for value in url_type:
                if value['url'] == path:
                    logger.info('[VerifyUrlSaveContent] match url : %s' % path)

                    detail['user_moid'] = user_moid
                    detail['user_name'] = user_name
                    detail['domain_moid'] = domain_moid
                    detail['level'] = value['level']
                    detail['type'] = value['type']
                    detail['description'] = value['name']
                    detail['ip'] = ip
                    return detail

        return None

    def run(self):
        if self._request.method == "GET":
            pass
        else:
            detail = self.parse_detail(self._request.path)
            if detail is not None:
                result = eval(self._response.content.decode('utf-8'))
                logger.info('result : %s' % result)
                if result.get("success",0) == 1:
                    detail['result'] = 'success'
                    detail['reason'] = ''
                else:
                    detail['result'] = 'fail'
                    detail['reason'] = result.get("message","")
                    
                logger.info("log_detail : %s" % detail)
                return detail