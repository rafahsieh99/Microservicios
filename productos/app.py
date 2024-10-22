from flask import Flask, request, jsonify
from db import get_db_connection
from autenticacion import verificar_token, token_requerido, generar_token  # Importar funciones de autenticación

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
# Ruta para iniciar sesión y generar un token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')  # Suponiendo que envías un nombre de usuario
    # Aquí puedes agregar lógica para verificar el usuario (por ejemplo, con una base de datos)
    
    # Generar el token
    token = generar_token(usuario)
    return jsonify({'token': token}), 200

# Ruta para crear un producto
@app.route('/productos', methods=['POST'])
@token_requerido  # Proteger la ruta
def crear_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    precio = int(data.get('precio'))  # Convertir precio a entero
    descripcion = data.get('descripcion')
    
    conn = get_db_connection()
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

# Ruta para obtener todos los productos
@app.route('/productos', methods=['GET'])
@token_requerido  # Proteger la ruta
def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertir los datos a un formato JSON
    return jsonify([{'id': producto[0], 'nombre': producto[1], 'precio': producto[2], 'descripcion': producto[3]} for producto in productos])

# Ruta para obtener un producto por ID
@app.route('/productos/<int:id>', methods=['GET'])
@token_requerido  # Proteger la ruta
def obtener_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if producto:
        return jsonify({'id': producto[0], 'nombre': producto[1], 'precio': producto[2], 'descripcion': producto[3]})
    else:
        return jsonify({'mensaje': 'Producto no encontrado'}), 404

# Ruta para actualizar un producto
@app.route('/productos/<int:id>', methods=['PUT'])
@token_requerido  # Proteger la ruta
def actualizar_producto(id):
    data = request.get_json()
    nombre = data.get('nombre')
    precio = int(data.get('precio'))  # Convertir precio a entero
    descripcion = data.get('descripcion')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = %s, precio = %s, descripcion = %s WHERE id = %s",
        (nombre, precio, descripcion, id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Producto actualizado'}), 200

# Ruta para eliminar un producto
@app.route('/productos/<int:id>', methods=['DELETE'])
@token_requerido  # Proteger la ruta
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensaje': 'Producto eliminado'}), 204

if __name__ == '__main__':
    app.run(port=5000, debug=True)
