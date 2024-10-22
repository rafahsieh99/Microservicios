# validaciones.py
import requests

def validar_producto(producto_id):
    try:
        response = requests.get(f'http://127.0.0.1:5000/productos/{producto_id}')
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException as e:
        print(f'Error al conectar con el microservicio de productos: {e}')
        return False
