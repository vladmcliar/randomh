import streamlit as st
import streamlit.components.v1 as components

# Открываем HTML-файл
with open('random..html', 'r') as file:
    html_code = file.read()

# Отображаем HTML-код в приложении Streamlit
components.html(html_code, height=1000)
