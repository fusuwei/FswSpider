import json
import setting
from tools import log
import pika
logger = log(__name__)


class MyRabbitPublisher:

    def __init__(self, host, user, password, queue_name="", callback_worker=None, prefetch_count=1, priority=0):

        self.host = host
        self.user = user
        self.password = password
        self._connection = None
        self._channel = None
        self._closing = False
        self._stopping = False
        self._consumer_tag = None
        self.callbackworker = callback_worker
        self.prefetch_count = prefetch_count
        self.priority = priority

        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = None

        self.QUEUE = queue_name

    def connect(self, ):
        """
        连接rabbitmq
        :return:
        """
        logger.info('连接rabbitmq')
        user_pwd = pika.PlainCredentials(self.user, self.password)
        return pika.SelectConnection(pika.ConnectionParameters(host=self.host, credentials=user_pwd,),
                                     on_open_callback=self.on_connection_open,
                                     on_open_error_callback=self.on_connection_open_error,
                                     on_close_callback=self.on_connection_closed)

    def on_connection_open_error(self, _unused_connection, err):
        """发生错误导致与rabbitmq连接
        """
        logger.error('连接打开失败！: %s'% err)
        return

    def on_connection_closed(self, _unused_connection, reason):
        """当与rabbitmq的连接为意外关闭"""

        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            logger.warning('连接打开失败 %s',
                           reason)
            return

    def on_connection_open(self, unused_connection):  # 打开连接时调用的方法
        """
        连接到rabbit回调函数
        :param unused_connection:
        :return:
        """
        logger.info('连接打开！')
        self.open_channel()

    def open_channel(self):
        """
        打开通道
        """
        logger.info('打开通道')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """当通道打开时，pika会调用此方法。通道对象已传入。
        通道现在已打开，将声明要使用的交换。
        """
        logger.info('通道已打开')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(setting.EXCHANGE)

    def add_on_channel_close_callback(self):
        """如果rabbitmq意外地关闭了通道。将调用此方法
        """
        logger.info('添加通道关闭回调函数')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        """关闭连接关闭对象。"""
        logger.warning('通道%s 已经关闭: %s'% (channel, reason))
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self, exchange_name):
        """
        设置交换机
        :param str|unicode exchange_name: The name of the exchange to declare
        """
        logger.info('交换机的名字%s', exchange_name)
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=setting.EXCHANGE_TYPE,
            callback=self.setup_queue)

    def setup_queue(self, _unused_frame):
        """通过调用队列在rabbitmq上设置队列
        :param str|unicode queue_name: 要声明的队列的名称。
        """
        logger.info('声明 %s', self.QUEUE)
        self._channel.queue_declare(
            queue=self.QUEUE, callback=self.on_queue_declareok)

    def on_queue_declareok(self, _unused_frame):
        """绑定队列和路由密钥
        """
        logger.info('绑定 交换机%s 和 队列%s 和 路由密钥%s三者个关系！', setting.EXCHANGE, self.QUEUE, setting.ROUTING_KEY)
        self._channel.queue_bind(self.QUEUE, setting.EXCHANGE, routing_key=setting.ROUTING_KEY, callback=self.on_bindok)

    def on_bindok(self, _unused_frame):
        """绑定完成， 并开始发布消息"""
        logger.info('绑定完成！')
        self.start_publishing()

    def start_publishing(self):
        """此方法将启用交付确认并安排发送给RabbitMQ的一条消息
        """
        logger.info('发出与使用者相关的rpc命令')
        self.publish_message()

    def publish_message(self):
        """如果类没有停止，则向rabbitmq发布消息，
        """
        if self._channel is None or not self._channel.is_open:
            return
        properties = pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2,
            content_encoding='utf-8',
            priority=self.priority
            )
        for i in range(10):
            message = {'url': 'eqweqwew'}
            self._channel.basic_publish(setting.EXCHANGE, setting.ROUTING_KEY,
                                        json.dumps(message, ensure_ascii=True),
                                        properties)
            self._message_number += 1
            self._deliveries.append(self._message_number)
            logger.info('Published message # %i', self._message_number)
        self.stop()

    def run(self):
        if not self._stopping:
            self._connection = None
            self._deliveries = []
            self._acked = 0
            self._nacked = 0
            self._message_number = 0
            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
            except KeyboardInterrupt:
                self.stop()
                if (self._connection is not None and
                        not self._connection.is_closed):
                    self._connection.ioloop.start()

    def stop(self):
        """通过关闭通道和连接来停止
        """
        logger.info('Stopping')
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        """调用此命令通过发送rabbitmq关闭通道
        """
        if self._channel is not None:
            logger.info('Closing the channel')
            self._channel.close()

    def close_connection(self):
        """此方法关闭与rabbitmq的连接。"""
        if self._connection is not None:
            logger.info('Closing connection')
            self._connection.close()


def main():
    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    example = MyRabbitPublisher(
        "127.0.0.1", "fsw", "123456", "test"
    )
    a = example.connect()
    a.ioloop.start()



if __name__ == '__main__':
    main()