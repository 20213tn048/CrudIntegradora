import logging
import json
import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, String, BINARY

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuración de la base de datos
DB_USER = 'admin'
DB_PASSWORD = 'nhL5zPpY1I9w'
DB_NAME = 'sispe'
DB_HOST = 'integradora-lambda.czc42euyq8iq.us-east-1.rds.amazonaws.com'

# Cadena de conexión
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db_connection = create_engine(db_connection_str)

metadata = MetaData()

categories = Table('categories', metadata,
                   Column('category_id', BINARY(16), primary_key=True),
                   Column('name', String(45), nullable=False))

def lambda_handler(event, context):
    logger.info("Event: %s", event)
    method = event['httpMethod']

    if method == 'GET':
        return get_categories()
    elif method == 'POST':
        return create_category(event)
    elif method == 'PUT':
        return update_category(event)
    elif method == 'DELETE':
        return delete_category(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Método no soportado')
        }

def get_categories():
    logger.info("Fetching categories")
    conn = db_connection.connect()
    query = categories.select()
    result = conn.execute(query)
    category_list = [{column: value.hex() if isinstance(value, bytes) else value for column, value in row.items()} for row in result]
    conn.close()
    return {
        'statusCode': 200,
        'body': json.dumps(category_list)
    }

def create_category(event):
    logger.info("Creating category")
    data = json.loads(event['body'])
    conn = db_connection.connect()
    query = categories.insert().values(category_id=bytes.fromhex(data['category_id']), name=data['name'])
    result = conn.execute(query)
    conn.close()
    return {
        'statusCode': 201,
        'body': json.dumps({'category_id': data['category_id']})
    }

def update_category(event):
    logger.info("Updating category")
    data = json.loads(event['body'])
    conn = db_connection.connect()
    query = categories.update().where(categories.c.category_id == bytes.fromhex(data['category_id'])).values(name=data['name'])
    conn.execute(query)
    conn.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Categoría actualizada')
    }

def delete_category(event):
    logger.info("Deleting category")
    data = json.loads(event['body'])
    conn = db_connection.connect()
    query = categories.delete().where(categories.c.category_id == bytes.fromhex(data['category_id']))
    conn.execute(query)
    conn.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Categoría eliminada')
    }
