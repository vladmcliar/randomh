import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = "postgres"
DB_PASS = "hoWgrRiYylsODDTFQqjpqlEmZyAFrTea"
DB_NAME = "railway"
DB_HOST = "autorack.proxy.rlwy.net"
DB_PORT = "11629"

def get_database_url():
    return f'postgresql+asyncpg://{DB_HOST}:{DB_PORT}/{DB_NAME}'



