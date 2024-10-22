import jwt
import datetime
from flask import current_app, request, jsonify
from functools import wraps

def generar_token(usuario):
    """Genera un token JWT para el usuario dado."""
    token = jwt.encode({
        'user': usuario,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # El token es válido por 1 hora
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def verificar_token(token):
    """Verifica el token JWT y devuelve el usuario si es válido."""
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data['user']  # Aquí puedes retornar el ID de usuario o cualquier información que necesites
    except jwt.ExpiredSignatureError:
        return None  # Token ha expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def token_requerido(f):
    """Decorador que requiere un token JWT para acceder a la ruta."""
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get('Authorization')  # Obtiene el token del encabezado

        if not token:
            return jsonify({'mensaje': 'Token es necesario'}), 401
        
        # Elimina 'Bearer ' del token si está presente
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        
        usuario = verificar_token(token)  # Verifica el token

        if usuario is None:
            return jsonify({'mensaje': 'Token inválido'}), 401
        
        return f(*args, **kwargs)  # Llama a la función original si el token es válido
    return decorador
