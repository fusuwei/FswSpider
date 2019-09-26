import pika


# 异步消息消费类
class RabbitConsumerAsync(object):
    EXCHANGE = 'amq.direct'
    EXCHANGE_TYPE = 'direct'

    def __init__(self, host, user, password, queue_name="fish_test", callback_worker=None, prefetch_count=1):
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

    def connect(self):
        return pika.SelectConnection(pika.ConnectionParameters(host=self.host, credentials=pika.PlainCredentials(self.user, self.password)), self.on_connection_open,
                                     stop_ioloop_on_close=False)  # 需要传入打开连接时调用的方法

    def on_connection_open(self, unused_connection):  # 打开连接时调用的方法
        """
        连接到rabbit回调函数
        :param unused_connection:
        :return:
        """
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """
        当rabbit连接到发布者是意外关闭时回调函数
        :return:
        """
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
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        "重启rabbit连接"
        self._connection.ioloop.stop()
        if not self._closing:
            self._connection = self.connect()
            self._connection.ioloop.start()

    def open_channel(self):
        """
        此方法将通过发出通道。打开RPC命令。当RabbitMQ确认通道打开时通过发送信道。
        OpenOK RPC应答，on_channel_open方法将被调用。
        :return:
        """
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """
        当通道打开时，pika将调用此方法。channel对象被传入，因此我们可以使用它。
        由于通道现在已经打开，我们将声明要使用的交换。
        :param channel:
        :return:
        """
        self._channel = channel
        self._channel.basic_qos(prefetch_count=self.prefetch_count)
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        """
        这个方法告诉pika调用on_channel_closed方法如果 RabbitMQ意外地关闭通道。
        :return:
        """
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """
        当RabbitMQ意外关闭通道时，pika调用。
        如果您尝试做某事，通道通常是关闭的
        违反协议，例如重新声明交换或队列
        不同的参数。在这种情况下，我们将关闭连接
        关闭对象。
        :param channel:
        :param reply_code:
        :param reply_text:
        :return:
        """
        print(reply_text)
        self._connection.close()

    def setup_exchange(self, exchange_name):
        """
        通过调用队列在RabbitMQ上设置队列。声明RPC
命令。当它完成时，on_queue_declareok方法将执行
被pika调用。
        :param exchange_name:
        :return:
        """
        self._channel.exchange_declare(self.on_exchange_declareok, exchange_name, self.EXCHANGE_TYPE, durable=True)

    def on_exchange_declareok(self, unused_frame):
        """
        当RabbitMQ完成交换后，pika调用。声明RPC
命令。
        :param unused_frame:
        :return:
        """
        self.setup_queue()

    def setup_queue(self):
        """
        通过调用队列在RabbitMQ上设置队列。”声明RPC
命令。当它完成时，on_queue_declareok方法将执行
被pika调用。
        :return:
        """
        self._channel.queue_declare(self.on_queue_declareok, self.QUEUE, durable=True)

    def on_queue_declareok(self, method_frame):
        """
        方法在队列中调用。声明RPC调用setup_queue已经完成。在这个方法中，我们将绑定队列
        并通过发出Queue.Bind与路由密钥交换RPC的命令。当这个命令完成时，on_bindok方法将执行
        被pika调用。
        :param method_frame:
        :return:
        """
        self._channel.queue_bind(self.on_bindok, self.QUEUE, self.EXCHANGE, self.QUEUE)

    def on_bindok(self, unused_frame):
        """
        当pika接收Queue.BindOk时，它调用这个方法
RabbitMQ的回应。因为我们知道我们现在是建立和绑定，它是
是时候开始发布了。
        :param unused_frame:
        :return:
        """
        self.start_consuming()

    def start_consuming(self):
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message, self.QUEUE)

    def add_on_cancel_callback(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        self.callbackworker(body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        self.close_channel()

    def close_channel(self):
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()

    def close_connection(self):
        self._connection.close()

    def start_publishing(self):
        """此方法将启用交付确认并调度
        第一个发送到RabbitMQ的消息
        """
        self.enable_delivery_confirmations()
        self.schedule_next_message()

    def schedule_next_message(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds.
        """
        if self._stopping:
            return
        self._connection.add_timeout(60, self.publish_message)

    def enable_delivery_confirmations(self):
        """发送确认。选择要启用传递的RabbitMQ的RPC方法
            通道上的确认。关闭这个的唯一方法就是关闭
            创建一个新的通道。
            当从RabbitMQ确认消息时
            将通过传入Basic.Ack调用on_delivery_confirmation方法
            或基本。来自RabbitMQ的Nack方法，该方法将指示它的消息
            是确认还是拒绝。
        """

        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.
        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()

        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        self._deliveries.remove(method_frame.method.delivery_tag)


if __name__ == '__main__':
    # 消费回调函数
    def callback(body):
        print(" [x] Received %r" % body)


    consumer = RabbitConsumerAsync(host="127.0.0.1", user="fsw", password="123456", queue_name="test",
                                   callback_worker=callback, prefetch_count=1)
    consumer.run()