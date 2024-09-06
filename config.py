import streamlit as st

def get_database_url():
    DB_USER = st.secrets["DB_USER"]
    DB_PASS = st.secrets["DB_PASS"]
    DB_NAME = st.secrets["DB_NAME"]
    DB_HOST = "10.54.48.3"  # Укажите ваш хост

    return f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{DB_NAME}&connect_timeout=30'

