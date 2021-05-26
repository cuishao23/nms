import time
import logging
import functools
import pika
import json
from django.conf import settings
from nms_server.dao.redis.device import set_device_user_moid

logger = logging.getLogger('nms.'+__name__)

def produce(exchange, routing_key, queue, msg):
    try:
        # 建立一个实例
        connection = pika.BlockingConnection(
            parameters=pika.URLParameters(settings.AMQP_URL)
        )
        # 声明一个管道，在管道里发消息
        channel = connection.channel()

        # 在管道里声明queue
        channel.queue_declare(queue=queue, durable=True)

        # 发送消息
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=json.dumps(msg),
                              properties=pika.BasicProperties(delivery_mode=2))

        connection.close()  # 队列关闭
    except Exception as e:
        logger.error(e)


def produce_msg(collectorMoid, msg):
    logger.info("produce_msg: collector moid=%s, msg=%s" % (collectorMoid, msg))
    queue = 'nms.webserver.q:' + collectorMoid
    routing_key = 'nms.webserver.k:' + collectorMoid
    # 集群环境，终端上报文件进度消息，user_moid字段可能为空，固此处保存设备和user_moid的对应关系
    
    if (msg.get('eventid','') == 'EV_PACKETCAPTURE_START_REQ') or (msg.get('eventid','')  == 'EV_PACKETCAPTURE_STOP_REQ') or (msg.get('eventid','')  == 'EV_GETLOG_REQ'):
        set_device_user_moid(msg['devid'],msg['devtype'],msg['user_moid'])

    produce('nms.webserver.ex', routing_key, queue, msg)
    logger.info("Rmq message send success")
