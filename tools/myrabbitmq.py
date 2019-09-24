import pika
import setting


class RabbitMq:
    def __init__(self, name, connection, channel):
        self.name = name
        self.rabbitmq_host = setting.rabbitmq_host
        self.rabbitmq_pwd = setting.rabbitmq_pwd
        self.connection = connection
        self.channel = channel

    @classmethod
    def connect(cls, name):
        user_pwd = pika.PlainCredentials(setting.rabbitmq_user, setting.rabbitmq_pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=setting.rabbitmq_host, credentials=user_pwd))
        channel = connection.channel()
        channel.queue_declare(queue=name)
        return cls(name, connection, channel)

    def pulish(self, body, priority=0):
        self.channel.basic_publish(exchange='', routing_key=self.name, body=body,
                                   properties=pika.BasicProperties(delivery_mode=2, priority=priority))

if __name__ == '__main__':
    a = RabbitMq.connect("adad")
