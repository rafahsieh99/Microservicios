# import pika

# def connect_rabbitmq():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='productos_queue', durable=True)  # Declara la cola
#     return connection, channel
