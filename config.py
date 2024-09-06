import streamlit as st

def get_database_url():
    DB_USER = st.secrets["DB_USER"]
    DB_PASS = st.secrets["DB_PASS"]
    DB_NAME = st.secrets["DB_NAME"]
    CLOUD_SQL_CONNECTION_NAME = st.secrets["CLOUD_SQL_CONNECTION_NAME"]
    DB_HOST = "35.232.235.84"  # Укажите ваш хост
    return f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}'

