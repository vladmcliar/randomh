import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = 'postgres'
DB_PASS = 'jiztix-toXnu9-qosxut'
DB_NAME = 'postgres'
CLOUD_SQL_CONNECTION_NAME = 'nmrandom:us-central1:mnrandom'

def get_database_url():
    return f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@35.232.235.84/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}'
