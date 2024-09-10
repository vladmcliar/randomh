import pandas as pd
import random
import asyncio
import logging
from datetime import datetime
import streamlit as st
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from config import get_database_url  # Импорт конфигурации подключения

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Имена для рандомайзера
names_list = ["Андрей", "Сергей", "Иван", "Вероника", "Катя", "Даня", "Маша", "Таня", "Влад", "Наташа", "Юлия"]

# Создание движка базы данных
try:
    engine = create_async_engine(
        get_database_url(), 
        echo=True, 
        pool_size=10,             # Максимальное количество соединений в пуле
        max_overflow=20,          # Дополнительные соединения сверх пула
        pool_timeout=30,          # Тайм-аут ожидания свободного соединения
        connect_args={"timeout": 60}  # Тайм-аут подключения
    )

    logger.info("Успешно создан движок базы данных.")
except Exception as e:
    logger.error(f"Ошибка при создании движка базы данных: {e}")
    st.error("Не удалось подключиться к базе данных.")

# Создание метаданных и таблицы
metadata = MetaData()
used_names_table = Table(
    'used_names', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('date', DateTime, default=datetime.utcnow)
)

async def create_tables():
    """Создает таблицы в базе данных, если они еще не существуют."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
            logger.info("Таблицы успешно созданы или уже существуют.")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        st.error("Не удалось создать таблицы в базе данных.")

# Функция для загрузки использованных имен из базы данных
async def load_used_names(session):
    """Загружает уже использованные имена из базы данных."""
    try:
        result = await session.execute(select(used_names_table))
        records = result.fetchall()
        logger.info("Успешно загружены использованные имена.")
        return pd.DataFrame(records, columns=["id", "Name", "Date"])
    except Exception as e:
        logger.error(f"Ошибка при загрузке использованных имен: {e}")
        st.error("Не удалось загрузить данные из базы данных.")
        return pd.DataFrame(columns=["id", "Name", "Date"])

# Функция для выбора случайного имени
async def get_random_name(session):
    """Выбирает случайное имя и сохраняет его в базе данных."""
    try:
        used_names_df = await load_used_names(session)
        available_names = [name for name in names_list if name not in used_names_df["Name"].values]

        if not available_names:
            st.warning("Все имена уже использованы. Очищаю базу данных и начинаю заново.")
            await session.execute(delete(used_names_table))
            await session.commit()
            logger.info("Таблица очищена, так как все имена уже использованы.")
            return None

        selected_name = random.choice(available_names)

        # Добавляем задержку и саспенс
        with st.spinner('Рожаю ведущего...'):
            for i in range(5, 0, -1):
                st.write(f"Назову через {i} секунд(ы)...")
                await asyncio.sleep(1)  # асинхронная задержка
        
        st.success(f"MN ведет {selected_name}")

        # Сохраняем имя и текущую дату в таблицу
        new_entry = {"name": selected_name, "date": datetime.now()}
        await session.execute(used_names_table.insert().values(new_entry))
        await session.commit()
        logger.info(f"Имя {selected_name} успешно добавлено в базу данных.")
        return selected_name

    except Exception as e:
        logger.error(f"Ошибка при выборе или сохранении имени: {e}")
        st.error("Произошла ошибка при обработке имени.")
        
async def get_leading_history(session):
    """Получает историю ведущих из базы данных."""
    try:
        result = await session.execute(
            select(used_names_table).order_by(used_names_table.c.date.desc())
        )
        records = result.fetchall()
        
        # Преобразование результатов в DataFrame
        df = pd.DataFrame(records, columns=result.keys())
        
        logger.info("Успешно загружена история ведущих.")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке истории ведущих: {e}")
        st.error("Не удалось загрузить историю ведущих.")
        return pd.DataFrame()



async def main():
    """Основная функция приложения Streamlit."""
    await create_tables()
    st.image("static/logo.png", use_column_width=False)
    st.title("Кто ведет MN?")
    st.write("Решит удача и немного кода:")

    # Создание сессии
    try:
        async with AsyncSession(engine) as session:
            if st.button("Получить имя"):
                await get_random_name(session)

            if st.button("Сбросить все"):
                st.button('Да я правда хочу стереть всю базу данных')
                st.button('Я передумал')
                if st.button('Да я правда хочу стереть всю базу данных'):
                
                    st.warning("Очищаю базу данных и начинаю заново.")
                    await session.execute(delete(used_names_table))
                    await session.commit()
                    logger.info("База данных очищена по запросу пользователя.")
                elif st.button('Я передумал'):
                    None

            if st.button("Показать историю ведущих"):
                history_df = await get_leading_history(session)
                if not history_df.empty:
                    st.write(history_df.loc[:, ['date', 'name']])
                else:
                    st.write("История ведущих пуста.")
                
    except Exception as e:
        logger.error(f"Ошибка в основной функции: {e}")
        st.error("Произошла ошибка при взаимодействии с базой данных.")


# Запуск основной функции
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске приложения: {e}")
        st.error("Приложение столкнулось с критической ошибкой и не может продолжить работу.")
