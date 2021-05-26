from django.shortcuts import render
import logging
import json
import threading
from dwebsocket.decorators import accept_websocket
import os
from nms_server.utils.myglobal import *
from nms_server.dao.diagnosis import add_capture_file, updata_capture_file
from nms_server.dao.redis.device import get_device_user_moid
from nms_server.rmq import RMQConsumerThread
from django.conf import settings

logger = logging.getLogger('nms.'+__name__)

# 存储连接websocket的用户

# 消费者创建标识
consumer_flag = True


@accept_websocket
def websocket_link(request):
    global consumer_flag
    # '连接websocket'
    # 获取连接
    if request.is_websocket:
        try:
            s = {}
            if consumer_flag:
                try:
                    logger.info('init nms_webserver_consumer: %s' %
                                os.getpid())
                    RMQConsumerThread(
                        name='nms_webserver_consumer_{}'.format(os.getpid()),
                        amqp_url=settings.AMQP_URL,
                        exchange='nms.webserver.ex',
                        queue='nms.webserver.q.{}'.format(os.getpid()),
                        routing_key='nms.webserver.k',
                        exchange_type='topic'
                    ).start()
                    consumer_flag = False
                except Exception as e:
                    logger.error(e)
            user = getattr(request, 'sso_user', None)
            user_moid = ''
            if user is not None: 
                user_moid = user['data']['moid']
            else:
                logger.error('sso_user in None')
                raise ValueError
            
            clients = get_clients()
            #  因为同一个账号打开多个页面连接信息是不同的
            if clients.get(user_moid) != None:
                # 连接信息  键 连接名  值：连接保存
                s[str(request.websocket)] = request.websocket
                # 已存在的连接信息继续增加
                clients[user_moid].update(s)
            else:
                #  连接信息  键 连接名  值：连接保存
                s[str(request.websocket)] = request.websocket
                # 新增 用户  连接信息
                clients[user_moid] = s

            set_clients(clients)
            logger.info('pid:%d ,client: %s',os.getpid(),clients)
            # 监听接收客户端发送的消息 或者 客户端断开连接
            for message in request.websocket:
                if not message:
                    break
                else:
                    client_msg_handler(user_moid,message)
        finally:
                logger.info('close client connect,user_moid:%s,request.websocket:%s',user_moid,str(request.websocket))
                # 通过用户名找到 连接信息 再通过 连接信息 k 找到 v (k就是连接信息)
                clients = get_clients()
                clients.get(user_moid).pop(str(request.websocket))
                if not clients.get(user_moid):
                    clients.pop(user_moid)
                set_clients(clients)
                logger.info('client: %s',clients)

# 客户端消息处理
def client_msg_handler(user_moid,msg):
    logger.info('[client_msg_handler] msg:%s' ,msg.decode('utf-8'))

    # test代码
    # import time
    # data = {
    #     'event':'ack',
    #     'text':'hello world'
    # }
    # for i in range(5):
    #     data['id'] = i
    #     send_msg_to_client(user_moid,data)
    #     time.sleep(1)
    pass

 # 发送消息
def websocketMsg(client, msg):
    # 因为一个账号会有多个页面打开 所以连接信息需要遍历
    for cli in client:
        try:
            b1 = json.dumps(msg).encode('utf-8')
            client[cli].send(b1)
        except Exception as e:
            logger.error(e)


'''
@description: 服务端发送消息
@user_moid {str}  用户moid
@msg {json}  消息
@return:        
'''
def send_msg_to_client(data):
    clients = get_clients()
    try:
        if data['user_moid'] == '':
            data['user_moid'] = get_device_user_moid(data['devid'],data['devtype'])

        user_moid = data['user_moid'] 
        if clients.get(user_moid) is not None:
            logger.info("send_msg_to_clinet: %s, %s" % (data, clients.get(user_moid)))
            if data['eventid'] == 'EV_PACKETCAPTURE_STOP_ACK':
                # 保存抓包文件到数据库
                file_name = data["url"].split("/")[-1]
                create_time = data['rpttime'].replace("/", "-").split(':',1)
                create_time = create_time[0] + " " + create_time[1]
                add_capture_file(data['user_moid'],
                                    data['devid'],
                                    file_name,
                                    data.get('size',0),
                                    create_time)

            if data['eventid'] == 'EV_PACKETCAPTURE_UPLOAD_PROGRESS_NTF':
                # 更新终端抓包文件信息
                file_name = data["url"].split("/")[-1]
                if 'size' in data:
                    updata_capture_file(data['user_moid'],
                                        data['devid'],
                                        file_name,
                                        data['size'])

            websocketMsg(clients[user_moid],data)
    except Exception as e:
        logger.error(e)