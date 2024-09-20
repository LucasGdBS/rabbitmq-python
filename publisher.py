from typing import Dict
import pika
import json
from decouple import config

class RabbitmqPublisher:
    def __init__(self) -> None:
        self.__host = config('HOST')
        self.__port = int(config('PORT'))
        self.__virtual_host = config('VIRTUAL_HOST')
        self.__username = config('RABBIT_USERNAME')
        self.__password = config('PASSWORD')
        self.__channel = self.__create_chanel()

        self.__exchange = "data_exchange"
        self.__routing_key = ""
    
    def __create_chanel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            virtual_host=self.__virtual_host,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password,
            ),
        )

        return pika.BlockingConnection(connection_parameters).channel()
    
    def send_message(self, body:Dict):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

rabbitmq_publisher = RabbitmqPublisher()
rabbitmq_publisher.send_message({"message":"Hello World!"})