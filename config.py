import streamlit as st

def get_database_url():
    DB_USER = st.secrets["DB_USER"]
    DB_PASS = st.secrets["DB_PASS"]
    DB_NAME = st.secrets["DB_NAME"]
    CLOUD_SQL_CONNECTION_NAME = st.secrets["CLOUD_SQL_CONNECTION_NAME"]

    return f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/10.54.48.3/{CLOUD_SQL_CONNECTION_NAME}'

