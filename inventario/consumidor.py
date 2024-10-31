import pika
import json

def conectar_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='inventario_queue', durable=True)
    return channel

def callback(ch, method, properties, body):
    mensaje = json.loads(body)
    print(f"Mensaje recibido: {mensaje}")

if __name__ == '__main__':
    channel = conectar_rabbitmq()
    channel.basic_consume(queue='inventario_queue', on_message_callback=callback, auto_ack=True)
    print('Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()
