import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
CLOUD_SQL_CONNECTION_NAME = os.getenv('CLOUD_SQL_CONNECTION_NAME')

def get_database_url():
    return f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}'
