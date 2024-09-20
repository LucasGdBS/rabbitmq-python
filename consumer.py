import pika
from decouple import config
from rabbitmq import Rabbitmq

class RabbitmqConsumer(Rabbitmq):
	def __init__(self, callback) -> None:
		super().__init__()

		self.__queue = "data_queue"
		self.__callback = callback
		self.set_consume()
	
	def set_consume(self):
		self._Rabbitmq__channel.queue_declare(
			queue=self.__queue,
			durable=True
		)
		self._Rabbitmq__channel.basic_consume(
			queue=self.__queue,
			auto_ack=True,
			on_message_callback=self.__callback
		)

	def start(self):
		print(f'Listem RabbitMQ on Port: {self._Rabbitmq__port}')
		self._Rabbitmq__channel.start_consuming()

def minha_callback(ch, method, properties, body):
	print(f'Recebendo mensagem: {body}')

rabitmq_consumer = RabbitmqConsumer(minha_callback)
rabitmq_consumer.start()
