import pika
import json

def conectar_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='inventario_queue', durable=True)
    return channel

def enviar_mensaje_a_rabbitmq(mensaje):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='inventario_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='inventario_queue',
        body=json.dumps(mensaje),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Hacer que el mensaje sea persistente
        )
    )
    connection.close()
