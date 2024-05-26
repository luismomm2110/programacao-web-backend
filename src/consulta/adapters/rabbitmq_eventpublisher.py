import json

import pika


class RabbitMQEventPublisher:
    def __init__(self, connection_string):
        credentials = pika.PlainCredentials('user', 'password')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(connection_string, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='medical', durable=True)

    def publish(self, event):
        self.channel.basic_publish(
            exchange='',
            routing_key='medical',
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

    def close(self):
        self.connection.close()
