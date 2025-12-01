import psycopg2
from app.config import settings

def get_connection():
    connection = psycopg2.connect(
        host= settings.host,
        port= settings.port,
        user= settings.user,
        password= settings.password,
        dbname= settings.db_name,
        connect_timeout= 5
    )
    return connection
