from typing import Dict
import pika
import json
from decouple import config
from rabbitmq import Rabbitmq

class RabbitmqPublisher(Rabbitmq):
    def __init__(self) -> None:
        super().__init__()

        self.__exchange = "data_exchange"
        self.__routing_key = ""

    
    def send_message(self, body:Dict):
        self._Rabbitmq__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

rabbitmq_publisher = RabbitmqPublisher()
rabbitmq_publisher.send_message({"message":"Hello World!"})