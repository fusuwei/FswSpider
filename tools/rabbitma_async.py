from tools import log
import pika


class MyRabbitPublisher:

    def __init__(self, consumer, host, user, password, queue_name="", callback_worker=None, prefetch_count=1):
        self.consumer = consumer
        self.logger = log(__name__)
        self.host = host
        self.user = user
        self.password = password
        self._connection = None
        self._channel = None
        self._closing = False
        self._stopping = False
        self._consumer_tag = None
        self.QUEUE = queue_name
        self.callbackworker = callback_worker
        self.prefetch_count = prefetch_count

    @classmethod
    def connect(cls, host, user, password, queue_name="test", callback_worker=None, prefetch_count=1):
        """
        连接rabbitmq
        :return:
        """
        consumer = pika.SelectConnection(pika.ConnectionParameters(host=host,
                                                                   credentials=pika.PlainCredentials(user, password)),
                                         cls.on_connection_open, stop_ioloop_on_close=False)

        return cls(consumer, host, user, password, queue_name="fish_test", callback_worker=None, prefetch_count=1)

    def con(self):
        return pika.SelectConnection(pika.ConnectionParameters(host=self.host,
                                                        credentials=pika.PlainCredentials(self.user, self.password)),
                              self.on_connection_open, stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):  # 打开连接时调用的方法
        """
        连接到rabbit回调函数
        :param unused_connection:
        :return:
        """
        self.logger.info('连接打开！')
        self.add_on_connection_close_callback()
        self.start_publishing()

    def add_on_connection_close_callback(self):
        """
        当rabbit连接到发布者是意外关闭时回调函数
        :return:
        """
        self.logger("添加连接关闭回调函数！")
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """
        当连接到RabbitMQ，pika调用此方法意外关闭，会重启RabbitMQ连接
        :param connection:
        :param reply_code:
        :param reply_text:
        :return:
        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.logger.warning('连接已关闭，5秒钟后重新打开: (%s) %s'%(reply_code, reply_text))
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        """重启rabbit连接"""
        self._connection.ioloop.stop()
        if not self._closing:
            self._connection = self.con()
            self._connection.ioloop.start()

    def start_publishing(self):
        """发送给RabbitMQ的一条消息"""
        self.logger.info('发送给RabbitMQ的一条消息')
        self.enable_delivery_confirmations()
        self.schedule_next_message()