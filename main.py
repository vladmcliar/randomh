import pandas as pd
import random
import time
from datetime import datetime
import streamlit as st
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.future import select

from config import get_database_url

# Имена для рандомайзера
names_list = ["Андрей", "Сергей", "Иван", "Вероника", "Катя", "Даня", "Маша", "Таня", "Влад", "Наташа"]

# Создание движка базы данных
engine = create_async_engine(get_database_url(), echo=True)

# Создание метаданных и таблицы
metadata = MetaData()
used_names_table = Table('used_names', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(50), nullable=False),
                         Column('date', DateTime, default=datetime.utcnow))

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

# Функция для загрузки использованных имен из базы данных
async def load_used_names(session):
    result = await session.execute(select(used_names_table))
    return pd.DataFrame(result.fetchall(), columns=["id", "Name", "Date"])

# Функция для выбора случайного имени
async def get_random_name(session):
    used_names_df = await load_used_names(session)
    available_names = [name for name in names_list if name not in used_names_df["Name"].values]

    if not available_names:
        st.warning("Все имена уже использованы. Очищаю базу данных и начинаю заново.")
        
        # Очистка таблицы
        await session.execute(used_names_table.delete())
        await session.commit()
        return None

    selected_name = random.choice(available_names)
    
    # Добавляем задержку и саспенс
    with st.spinner('Рожаю ведущего...'):
        for i in range(5, 0, -1):
            st.write(f"Назову через {i} секунд(ы)...")
            time.sleep(1)
    
    st.success(f"MN ведет {selected_name}")

    # Сохраняем имя и текущую дату в таблицу
    new_entry = {"name": selected_name, "date": datetime.now()}
    await session.execute(used_names_table.insert().values(new_entry))
    await session.commit()
    return selected_name

# Основная функция
async def main():
    await create_tables()
    st.image("static/logo.png", use_column_width=True)
    st.title("Кто ведет MN?")
    st.write("Решит удача и немного кода:")

    # Создание сессии
    async with AsyncSession(engine) as session:
        if st.button("Получить имя"):
            await get_random_name(session)

        if st.button("Сбросить все"):
            st.warning("Очищаю базу данных и начинаю заново.")
            await session.execute(used_names_table.delete())
            await session.commit()

# Запуск основной функции
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())