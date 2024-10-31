from flask import Flask, request, jsonify
from db import get_db_connection
import pybreaker

app = Flask(__name__)

# Inicializar el circuito de ruptura
circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,         # Número máximo de fallas antes de abrir el circuito
    reset_timeout=30    # Tiempo en segundos para reiniciar el circuito
)

# Ruta para crear un producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    precio = int(data.get('precio'))  # Convertir precio a entero
    descripcion = data.get('descripcion')
    
    try:
        conn = circuit_breaker.call(get_db_connection)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, descripcion) VALUES (%s, %s, %s) RETURNING id",
            (nombre, precio, descripcion)
        )
        producto_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Producto creado', 'id': producto_id}), 201
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

        # Convertir los datos a un formato JSON
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

    try:
        conn = circuit_breaker.call(get_db_connection)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = %s, precio = %s, descripcion = %s WHERE id = %s",
            (nombre, precio, descripcion, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Producto actualizado'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al actualizar el producto', 'error': str(e)}), 503

# Ruta para eliminar un producto
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = circuit_breaker.call(get_db_connection)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Producto eliminado'}), 204
    except Exception as e:
        return jsonify({'mensaje': 'Error al eliminar el producto', 'error': str(e)}), 503

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Asegúrate de que el puerto sea diferente al de inventario
