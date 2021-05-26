import logging
import threading

logger = logging.getLogger('nms.'+__name__)


class RMQConsumerThread(threading.Thread):

    def __init__(self, name, amqp_url, exchange, queue, routing_key, exchange_type):
        self.amqp_url = amqp_url
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.exchange_type = exchange_type
        super().__init__(name=name, daemon=True)

    # 重写run方法
    def run(self):
        from nms_server.rmq.consumer import ReconnectingConsumer
        while True:
            try:
                consumer = ReconnectingConsumer(
                    exchange=self.exchange,
                    queue=self.queue,
                    routing_key=self.routing_key,
                    exchange_type=self.exchange_type,
                    amqp_url=self.amqp_url,
                    handler=self.handler)
                consumer.run()
            except Exception as err:
                logger.error(err)

    def handler(self, message):
        from nms_server.rmq import msg_handler
        import json
        try:
            data = json.loads(message.decode('utf-8'))
            func = eval('msg_handler.'+data['eventid'].lower())
            if callable(func):
                func(data)
        except Exception as e:
            logger.error('[%s]: error:%s, msg:%s' %
                         (self._name, str(e), message))
