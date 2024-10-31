import pika
import json

def callback(body):
    try:
        mensaje = json.loads(body)  # Decodificar el mensaje JSON
        print(f"Mensaje recibido: {mensaje}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el mensaje JSON: {e}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='productos_queue', durable=True)

channel.basic_consume(queue='productos_queue', on_message_callback=callback, auto_ack=True)

print('Esperando mensajes. Para salir presiona CTRL+C')
channel.start_consuming()


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='productos_queue', durable=True)
    channel.basic_consume(queue='productos_queue', on_message_callback=callback, auto_ack=True)
    print('Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consume()
