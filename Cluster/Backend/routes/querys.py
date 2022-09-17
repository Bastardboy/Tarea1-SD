from psycopg2 import connect

def init_db():
    conn = connect(
        dbname='tarea1',
        user='postgres',
        password='postgres',
        host='postgres'
    )
    return conn