from flask import Flask, request, jsonify
from db import get_db_connection
import pybreaker
import pika
import json

app = Flask(__name__)

# Inicializar el circuito de ruptura
circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,         # Número máximo de fallas antes de abrir el circuito
    reset_timeout=30    # Tiempo en segundos para reiniciar el circuito
)

# Conexión a RabbitMQ
def conectar_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='productos_queue', durable=True)  # Asegúrate de declarar la cola
        return channel
    except pika.exceptions.AMQPConnectionError as e:
        print("Error de conexión a RabbitMQ:", e)
        raise

# Función para enviar un mensaje a RabbitMQ
def enviar_mensaje(mensaje):
    channel = conectar_rabbitmq()
    try:
        channel.basic_publish(
            exchange='',
            routing_key='productos_queue',
            body=mensaje,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Mensaje persistente
            )
        )
    finally:
        channel.close()  # Asegúrate de cerrar el canal siempre

# Ruta para crear un producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json(force=True)  # Forzar a interpretar el cuerpo como JSON
        nombre = data.get('nombre')
        precio = data.get('precio')
        descripcion = data.get('descripcion')

        # Verificar que todos los campos requeridos estén presentes
        if not nombre or not precio or not descripcion:
            return jsonify({'mensaje': 'Faltan campos requeridos'}), 400

        # Convertir precio a entero
        try:
            precio = int(precio)
        except ValueError:
            return jsonify({'mensaje': 'El precio debe ser un número entero'}), 400

        # Crear el producto en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, descripcion) VALUES (%s, %s, %s) RETURNING id",
            (nombre, precio, descripcion)
        )
        producto_id = cursor.fetchone()[0]  # Obtener el ID del nuevo producto
        conn.commit()
        cursor.close()
        conn.close()

        # Preparar el mensaje para RabbitMQ (si es necesario)
        mensaje = {
            'accion': 'crear',
            'id': producto_id,
            'nombre': nombre,
            'precio': precio,
            'descripcion': descripcion
        }

        enviar_mensaje(json.dumps(mensaje))  # Envía el mensaje a la cola como JSON
        return jsonify({'mensaje': 'Producto creado exitosamente', 'id': producto_id}), 201

    except Exception as e:
        return jsonify({'mensaje': 'Error al crear el producto', 'error': str(e)}), 503
    
# Ruta para obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        conn = circuit_breaker.call(get_db_connection)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify([{'id': producto[0], 'nombre': producto[1], 'precio': producto[2], 'descripcion': producto[3]} for producto in productos])
    except Exception as e:
        return jsonify({'mensaje': 'Error al obtener productos', 'error': str(e)}), 503

# Ruta para obtener un producto por ID
@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        conn = circuit_breaker.call(get_db_connection)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()

        if producto:
            return jsonify({'id': producto[0], 'nombre': producto[1], 'precio': producto[2], 'descripcion': producto[3]})
        else:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'mensaje': 'Error al obtener el producto', 'error': str(e)}), 503

# Ruta para actualizar un producto
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    nombre = data.get('nombre')
    precio = int(data.get('precio'))  # Convertir precio a entero
    descripcion = data.get('descripcion')

    # Crear conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Actualizar el producto en la base de datos
    cursor.execute(
        "UPDATE productos SET nombre = %s, precio = %s, descripcion = %s WHERE id = %s",
        (nombre, precio, descripcion, id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    mensaje = {
        'accion': 'actualizar',
        'id': id,
        'nombre': nombre,
        'precio': precio,
        'descripcion': descripcion
    }

    try:
        enviar_mensaje(json.dumps(mensaje))  # Envía el mensaje a la cola como JSON
        return jsonify({'mensaje': 'Producto actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al enviar el mensaje', 'error': str(e)}), 503
    
# Ruta para eliminar un producto por ID
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ejecutar la consulta para eliminar el producto
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        
        # Verificar si se eliminó algún producto
        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404
        
        conn.commit()
        cursor.close()
        conn.close()

        mensaje = {
            'accion': 'eliminar',
            'id': id
        }

        try:
            enviar_mensaje(json.dumps(mensaje))  # Envía el mensaje a la cola como JSON
            return jsonify({'mensaje': 'Producto eliminado exitosamente'}), 200
        except Exception as e:
            return jsonify({'mensaje': 'Error al enviar el mensaje', 'error': str(e)}), 503

    except Exception as e:
        return jsonify({'mensaje': 'Error al eliminar el producto', 'error': str(e)}), 503


if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Asegúrate de que el puerto sea diferente al de inventario
