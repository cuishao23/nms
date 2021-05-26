import logging
from nms_server.ws.views import send_msg_to_client

logger = logging.getLogger('nms.'+__name__)
# 终端视频制式配置结果通知
def ev_config_1st_video_format_ntf(data):
    '''
    {
        "eventid": "EV_CONFIG_1ST_VIDEO_FORMAT_NTF",
        "devid": "xxxxxxxxxxxxxxxx",
        "user_moid" : "dddd",   //用户moid
        "devtype": "SKY windows",
        "result": 1 //1是成功，0是失败
    }
    '''
    logger.info('[ev_config_1st_video_format_ntf] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 终端注册地址配置结果通知
def ev_config_reg_addr_ntf(data):
    '''
    {    
        "eventid": "EV_CONFIG_REG_ADDR_NTF",
        "devid": "xxxxxxxxxxxxxxxx",
        "user_moid" : "dddd",   //用户moid
        "devtype": "SKY windows",
        "result": 0     //1是成功，0是失败
    }
    '''

    logger.info('[ev_config_reg_addr_ntf] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 终端网络配置结果通知
def ev_config_network_ntf(data):
    '''
    {
        "eventid": "EV_CONFIG_NETWORK_NTF", 
        "devid": "xxxxxxxxxxxxxxxx",
        "user_moid" : "dddd",   //用户moid
        "devtype": "SKY windows",
        "result": 1     //1是成功，0是失败
    }
    '''
    logger.info('[ev_config_network_ntf] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 获取日志列表成功响应
def ev_getlog_list_ack(data):
    '''
    {
        "eventid" : "EV_GETLOG_LIST_ACK",//消息类型
        "devid" : "xxxxx",               //终端的moid
        "user_moid" : "dddd",            //用户moid
        "file_list" : [
        {
           "name" : "log.txt",              //日志文件名
           "dir"  : "/opt/log/nms_adapter"  //日志文件路径
           "crtime" : "2020/1/17:10:58:41"  //文件创建时间
        },
        {
           "name" : "log1.txt",              //日志文件名
           "dir"  : "/opt/log/nms_adapter"   //日志文件路径
           "crtime" : "2020/1/17:10:58:41"   //文件创建时间
        }]
    }

    '''
    logger.info('[ev_getlog_list_ack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

def ev_getlog_ack(data):
    '''
    {
        "eventid" : "EV_GETLOG_ACK",   //消息类型
        "devid" : "xxxxx",             //设备的moid
        "user_moid" : "dddd",          //用户moid
        "url" : "http://xxxxx.xxxx"    //日志下载地址
    }
    '''
    logger.info('[ev_getlog_ack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 获取日志列表失败响应
def ev_getlog_nack(data):
    '''
    {
        "eventid" : "EV_GETLOG_NACK",   //消息类型
        "devid" : "xxxxx",              //终端的moid
        "user_moid" : "dddd",           //用户moid
        "reasoncode" : 1                //原因码，见REASONCODE定义
    }
    '''
    logger.info('[ev_getlog_nack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 日志文件上传进度通知
def ev_log_upload_progress_ntf(data):
    '''
    {
        'collectorid': 'a4bf01519af2', 
        'rpttime': '2020/5/12:19:46:35', 
        'user_moid': 'mooooooo-oooo-oooo-oooo-defaultadmin', 
        'rpttimestamp': 1589283995228, 
        'devid': '992ce364-62ad-11ea-8dad-a4bf01519af2', 
        'devtype': 'x86_server', 
        'progress': 100, 
        'eventid': 'EV_LOG_UPLOAD_PROGRESS_NTF', 
        'msgsrc': 'x86_server', 
        'url': 'http://127.0.0.1:8083/mnt/files/kdfs/1589283990.zip'
    }
    '''

    logger.info('[ev_log_upload_progress_ntf] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 开始抓包成功响应
def ev_packetcapture_start_ack(data):
    '''
    {
        "eventid" : “EV_PACKETCAPTURE_START_ACK”, //消息类型
        "user_moid" : "dddd"                      //用户moid
    }
    '''
    logger.info('[ev_packetcapture_start_ack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 开始抓包失败响应
def ev_packetcapture_start_nack(data):
    '''
    {
        "eventid" : "EV_PACKETCAPTURE_START_NACK",    //消息类型
        "user_moid" : "dddd",                         //用户moid
        "reasoncode" : 1                              //原因码，见REASONCODE定义
    }
    '''
    logger.info('[ev_packetcapture_start_nack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 停止抓包成功响应
def ev_packetcapture_stop_ack(data):
    '''
    {
        "eventid" : "EV_PACKETCAPTURE_STOP_ACK",    //消息类型
        "devid" : "xxxxx",                          //设备的moid
        "user_moid" : "dddd",                       //抓包账户的moid
        "url" : 抓包地址                            //抓包文件下载地址
        "ctime" : "2020/02/10 10:20:00",           //抓包文件创建时间，终端消息缺少字段，可取rpttime字段替换
        "size" : 20,                                //抓包文件大小，单位（B），终端消息缺少字段，补充到终端EV_PACKETCAPTURE_UPLOAD_PROGRESS_NTF消息
        "name" : "dump.pacp"                        //抓包文件名，
    }
    '''
    logger.info('[ev_packetcapture_stop_ack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 停止抓包失败响应
def ev_packetcapture_stop_nack(data):
    '''
    {
        "eventid" : "EV_PACKETCAPTURE_STOP_NACK",//消息类型
        "user_moid" : "dddd",                    //用户moid
        "reasoncode" : 1                         //原因码
    }
    '''
    logger.info('[ev_packetcapture_stop_nack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 抓包文件上传进度通知
def ev_packetcapture_upload_progress_ntf(data):
    '''
    {
        "eventid" : "EV_PACKETCAPTURE_UPLOAD_PROGRESS_NTF",//消息类型
        "devid" : "xxxxx",   //设备的moid
        "user_moid" : "dddd",//用户moid
        'url' : 'http://127.0.0.1:8083/mnt/files/kdfs/nms_tcpdump_1589448578.pcap', 
        "progress" : 80,     //上传进度百分比,
        "size":1200          //终端抓包消息有该字段            
        "reasoncode" :0      //上传失败，reasoncode为负
    }
    '''
    logger.info('[ev_packetcapture_upload_progress_ntf] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)


# 终端性能消息成功回复
def ev_pfminfo_msg(data):
    '''
    {
        "eventid": "EV_PFMINFO_MSG",
        "devid": "1111",
        "user_moid" : "dddd",//用户moid
        "devtype": "TrueLink",
        "rpttime": "2014/06/16:09:57:50",
        "collectorid": "12331",
        "pfm_info":
        {
            "cpu_userate": 12, // cpu使用百分比
            "mem_userate": 12, // 内存使用百分比
            "sip_addr": "192.168.1.1", // sip服务器信息
            "gk_addr": "", // GK服务器信息
            "master_chip_status": 0, // 主芯片状态，0-正常，1-异常
            "temperature_status": 0, // 温度状态，0-正常，1-异常
            "netcardinfo":
            {
                "sendkbps": 123,
                "recvkbps": 123,
                "netcardcount: 123, // 网卡个数
                "netcards":
                [{
                    "name": "eth0", // 网卡名称（比如eth0）
                    "netcardtype": 1, // 网卡类型
                    "sendkbps": 123, // 网卡出口量
                    "recvkbps": 123 // 网卡入口量
                }]
            },
            "video_resource_name":
            [{
                "video_index": "HDMI0", // 视频源名称
                "type": 1 // 视频源类型 0：主流 1：双流
            }],
            "loudspeakers":
            [{
                "name": "001", // 扬声器名称
                "status": 1 // 扬声器状态，0-正常，1-异常
            }],
            "microphones":
            [{
                "name": "xxxxx", // 麦克风名称
                "status": 1 // 麦克风状态，0-正常，1-异常
            }]
        }
    }

    '''
    logger.info('[ev_pfminfo_msg] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)


# 终端性能消息失败回复
def ev_pfminfo_nack(data):
    '''
    {
        "eventid" : "EV_PFMINFO_NACK",//消息类型
        "user_moid" : "dddd",         //用户moid
        "reasoncode" : 1              //原因码，见REASONCODE定义
    }

    '''
    logger.info('[ev_pfminfo_nack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 终端音量能量值请求回复
def ev_volume_ack(data):
    '''
    {
        "eventid": "EV_VOLUME_ACK",
        "devid": "1111",
        "user_moid" : "dddd",//用户moid
        "devtype": "TrueLink",
        "rpttime": "2014/06/16:09:57:50",
        "volume_info": // 音量信息
        {
            "input": 12, // 输入音量能量值大小---必须
            "output": 12 //输出音量能量值大小---必须
        }
    }

    '''
    logger.info('[ev_volume_ack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)

# 终端音视频信号请求回复
def ev_audio_video_status_ack(data):
    '''
    {
        "eventid": "EV_AUDIO_VIDEO_STATUS_ACK",
        "devid": "1111",
        "user_moid" : "dddd",//用户moid
        "devtype": "TrueLink",
        "rpttime": "2014/06/16:09:57:50",
        "audio_input_sign":
        [
            {
                "type": "DVI",
                "status": 1 // 1: 正常 0: 异常
            },
            {
                "type": "RCA",
                "status": 0
            }
        ],
        "audio_output_sign":
        [
            {
                "type": "HDMI",
                "status": 1
            },
            {
                "type": "SDI",
                "status": 0
            }
        ],
        "video_input_sign":
        [
            {
                "type": "VGA",
                "status": 1
            },
            {
                "type": "HDMI",
                "status": 0
            }
        ],
        "video_output_sign":
        [
            {
                "type": "HDMI",
                "status": 1
            },
            {
                "type": "SDI",
                "status": 0
            }
        ]
    }
    '''
    logger.info('[ev_audio_video_status_ack] data=%s' % data)

    # 以websocker通知前端
    send_msg_to_client(data)