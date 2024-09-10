import streamlit as st

password = st.secrets["database"]["pass"]

def get_database_url():
    return f'postgresql+asyncpg://postgres:{password}@autorack.proxy.rlwy.net:20211/railway'



