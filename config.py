import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "pencil-volume"
DB_HOST = "autorack.proxy.rlwy.net"
DB_PORT = "11629"

def get_database_url():
    return f'postgresql+asyncpg://{DB_HOST}:{DB_PORT}/{DB_NAME}'


