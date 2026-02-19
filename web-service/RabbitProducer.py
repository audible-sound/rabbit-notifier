import pika
import time
import json


class RabbitProducer:
    def __init__(
            self,
            host,
            port,
            username,
            password,
            max_retry=5,
            retry_delay=0.5):

        self._credentials = pika.PlainCredentials(
            username=username, password=password)
        self._parameters = pika.ConnectionParameters(
            host=host, port=port, credentials=self._credentials)
        self._max_retry = max_retry
        self._retry_delay = retry_delay
        self._connection = None
        self._channel = None

    def _connect(self):
        for _ in range(self._max_retry):
            try:
                print("Connecting to rabbitmq...")
                self._connection = pika.BlockingConnection(self._parameters)
                self._channel = self._connection.channel()
                break
            except Exception as e:
                print(f"Error connecting to rabbitmq: {e}")
                time.sleep(self._retry_delay)

        if self._connection is None:
            raise Exception("Failed to connect to rabbitmq.")

    def publish_message(self, queue_name, message):
        self._connect()
        try:
            self._channel.queue_declare(queue=queue_name, durable=True)
            properties = pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            )
            self._channel.basic_publish(
                exchange="", routing_key=queue_name, properties=properties, body=json.dumps(message))
        finally:
            self._channel.close()
            self._connection.close()
