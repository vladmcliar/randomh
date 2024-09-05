import pandas as pd
import random
import time
from datetime import datetime
import streamlit as st

# Имена для рандомайзера
names_list = ["Андрей", "Сергей", "Иван", "Вероника", "Катя", "Даня", "Маша", "Таня", "Влад", "Наташа"]

# Файл для сохранения результатов
filename = "used_names.csv"

# Загрузка уже использованных имен
def load_used_names():
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Date"])

# Функция для выбора случайного имени
def get_random_name(used_names_df):
    available_names = [name for name in names_list if name not in used_names_df["Name"].values]
    
    if not available_names:
        st.warning("Все имена уже использованы. Очищаю файл и начинаю заново.")
        used_names_df = pd.DataFrame(columns=["Name", "Date"])  # Очистка DataFrame
        used_names_df.to_csv(filename, index=False)
        return None

    selected_name = random.choice(available_names)
    
    # Добавляем задержку и саспенс
    with st.spinner('Выбираю имя...'):
        for i in range(5, 0, -1):
            st.write(f"Назову через {i} секунд(ы)...")
            time.sleep(1)
    
    st.success(f"Выпало имя: {selected_name}")

    # Сохраняем имя и текущую дату в файл
    used_names_df.loc[len(used_names_df)] = [selected_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    used_names_df.to_csv(filename, index=False)
    return selected_name

# Основная функция
def main():
    st.image("static/logo.png", use_column_width=True)
    st.title("Рандомайзер Имен")
    st.write("Случайный выбор имени из списка:")
    
    # Загрузка использованных имен
    used_names_df = load_used_names()
    
    if st.button("Получить имя"):
        get_random_name(used_names_df)

    if st.button("Сбросить все"):
        st.warning("Очищаю файл и начинаю заново.")
        used_names_df = pd.DataFrame(columns=["Name", "Date"])
        used_names_df.to_csv(filename, index=False)

# Запуск основной функции
if __name__ == "__main__":
    main()
