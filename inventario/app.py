from flask import Flask, request, jsonify
import requests
from db import get_db_connection
from validaciones import validar_producto
from autenticacion import generar_token, verificar_token  # Importa el manejador de autenticación
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  # Cambia esto por una clave más segura

# Decorador para proteger las rutas
def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'mensaje': 'Token es necesario'}), 403
        
        user = verificar_token(token)
        if not user:
            return jsonify({'mensaje': 'Token inválido'}), 403
        
        return f(user, *args, **kwargs)
    return decorated

# Ruta para generar un token
@app.route('/generar_token', methods=['GET'])
def generar_token_route():
    token = generar_token('usuario_prueba')  # Cambia esto por la información real del usuario
    return jsonify({'token': token}), 200

# Ruta para agregar inventario
@app.route('/inventario', methods=['POST'])
@token_requerido  # Protege la ruta con autenticación
def agregar_inventario(usuario):
    data = request.get_json()
    producto_id = int(data.get('producto_id'))
    cantidad = int(data.get('cantidad'))

    # Validar que el producto existe llamando al microservicio de productos
    if not validar_producto(producto_id):
        return jsonify({'mensaje': 'Producto no encontrado'}), 404

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventario (producto_id, cantidad) VALUES (%s, %s) RETURNING id",
        (producto_id, cantidad)
    )
    inventario_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Inventario agregado', 'id': inventario_id}), 201

# Ruta para obtener el inventario
@app.route('/inventario', methods=['GET'])
@token_requerido  # Protege la ruta con autenticación
def obtener_inventario(usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario")
    inventarios = cursor.fetchall()
    cursor.close()
    conn.close()

    # Formatear los resultados
    inventario_list = [{'id': inv[0], 'producto_id': inv[1], 'cantidad': inv[2]} for inv in inventarios]
    return jsonify(inventario_list)

# Ruta para obtener un inventario por ID
@app.route('/inventario/<int:id>', methods=['GET'])
@token_requerido  # Protege la ruta con autenticación
def obtener_inventario_por_id(usuario, id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario WHERE id = %s", (id,))
    inventario = cursor.fetchone()
    cursor.close()
    conn.close()

    if inventario:
        return jsonify({'id': inventario[0], 'producto_id': inventario[1], 'cantidad': inventario[2]})
    else:
        return jsonify({'mensaje': 'Inventario no encontrado'}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Asegúrate de que el puerto sea diferente al de productos
