import json
import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Sequence

# Configuración de la base de datos
DB_USER = 'admin'
DB_PASSWORD = 'sispe123'
DB_NAME = 'sispedb'
DB_HOST = '-----------------'#mando codigo de verificacion :(

# Cadena de conexión
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db_connection = create_engine(db_connection_str)

metadata = MetaData()

categoria = Table('categoria', metadata,
                  Column('id', Integer, Sequence('categoria_id_seq'), primary_key=True, autoincrement=True),
                  Column('nombre_categoria', String(60)))

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'GET':
        return get_categoria()
    elif method == 'POST':
        return create_categoria(event)
    elif method == 'PUT':
        return update_categoria(event)
    elif method == 'DELETE':
        return delete_categoria(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Método no soportado')
        }

def get_categoria():
    conn = db_connection.connect()
    query = categoria.select()
    result = conn.execute(query)
    categoria_list = [{column: value for column, value in row.items()} for row in result]
    conn.close()
    return {
        'statusCode': 200,
        'body': json.dumps(categoria_list)
    }

def create_categoria(event):
    data = json.loads(event['body'])
    conn = db_connection.connect()
    query = categoria.insert().values(nombre_categoria=data['nombre_categoria'])
    result = conn.execute(query)
    conn.close()
    return {
        'statusCode': 201,
        'body': json.dumps({'id': result.inserted_primary_key[0]})
    }

def update_categoria(event):
    data = json.loads(event['body'])
    conn = db_connection.connect()
    query = categoria.update().where(categoria.c.id == data['id']).values(nombre_categoria=data['nombre_categoria'])
    conn.execute(query)
    conn.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Categoría actualizada')
    }

def delete_categoria(event):
    data = json.loads(event['body'])
    conn = db_connection.connect()
    query = categoria.delete().where(categoria.c.id == data['id'])
    conn.execute(query)
    conn.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Categoría eliminada')
    }