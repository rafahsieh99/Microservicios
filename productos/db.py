import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="productos_db",
        user="postgres",  
        password="123456"  
    )
    return conn
