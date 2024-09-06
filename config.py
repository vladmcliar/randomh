import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]
DB_NAME = st.secrets["DB_NAME"]
CLOUD_SQL_CONNECTION_NAME = st.secrets["CLOUD_SQL_CONNECTION_NAME"]

def get_database_url():
    return f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@10.54.48.3/{DB_NAME}'
