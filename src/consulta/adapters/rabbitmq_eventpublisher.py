import pika


class RabbitMQEventPublisher:
    def __init__(self, connection_string):
        self.connection = pika.BlockingConnection(pika.URLParameters(connection_string))
        self.channel = self.connection.channel()

    def publish(self, event):
        self.channel.basic_publish(exchange='', routing_key='events', body=event)

    def close(self):
        self.connection.close()