from time import sleep
from dotenv import dotenv_values
import ssl
import pika

config = dotenv_values(".env")  

# SSL Context for TLS configuration of Amazon MQ for RabbitMQ
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

rabbitmq_user = config["USERNAME"]
rabbitmq_password = config["PASSWORD"]
rabbitmq_broker_id = config["BROKER"]
region = config["REGION"]
port = config["PORT"]

url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:{port}"
parameters = pika.URLParameters(url)
parameters.ssl_options = pika.SSLOptions(context=ssl_context)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue='test')
channel.basic_publish(exchange='', routing_key='test',
                      body=b'Test message.')
temp = 0

try:
    while True:
        temp += 1
        sleep(5)
        channel.basic_publish(exchange='', routing_key='test',
                        body=f'{temp}')
except KeyboardInterrupt: 
     print('Interrupted')
finally:
    connection.close()
