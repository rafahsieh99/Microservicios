import psycopg2
from config import username_productos_db, password_productos_db
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="inventario_db",
        user= username_productos_db,  
        password= password_productos_db  
    )
    return conn
