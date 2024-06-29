import json

import pika


class RabbitMQEventPublisher:
    def __init__(self, connection_string, queue_name):
        credentials = pika.PlainCredentials('user', 'password')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(connection_string, credentials=credentials))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def publish(self, event):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

    def close(self):
        self.connection.close()
