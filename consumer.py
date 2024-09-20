import pika
from decouple import config

class RabbitmqConsumer:
	def __init__(self, callback) -> None:
		self.__host = config('HOST')
		self.__port = int(config('PORT'))
		self.__virtual_host = config('VIRTUAL_HOST')
		self.__username = config('RABBIT_USERNAME')
		self.__password = config('PASSWORD')
		self.__queue = "data_queue"
		self.__callback = callback
		self.__channel = self.__create_chanel()
	
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

		channel = pika.BlockingConnection(connection_parameters).channel()
		channel.queue_declare(
			queue=self.__queue,
			durable=True
		)
		channel.basic_consume(
			queue=self.__queue,
			auto_ack=True,
			on_message_callback=self.__callback
		)

		return channel

	def start(self):
		print(f'Listem RabbitMQ on Port: {self.__port}')
		self.__channel.start_consuming()

def minha_callback(ch, method, properties, body):
	print(f'Recebendo mensagem: {body}')

rabitmq_consumer = RabbitmqConsumer(minha_callback)
rabitmq_consumer.start()
