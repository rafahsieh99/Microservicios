from flask import Flask, request, jsonify
from db import get_db_connection
from validaciones import validar_producto

app = Flask(__name__)

# Ruta para agregar inventario
@app.route('/inventario', methods=['POST'])
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