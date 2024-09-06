import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = meticulous-empathy
DB_HOST = "autorack.proxy.rlwy.net"
DB_PORT = "5432"

def get_database_url():
    return f'postgresql+asyncpg://{DB_HOST}:{DB_PORT}/{DB_NAME}'


