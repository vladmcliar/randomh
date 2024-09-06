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

class Database:
    def __init__(self, db_url):
        try:
            self.engine = create_async_engine(
                db_url,
                echo=True,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                connect_args={"timeout": 60}
            )
            self.metadata = MetaData()
            self.used_names_table = Table(
                'used_names', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(50), nullable=False),
                Column('date', DateTime, default=datetime.utcnow)
            )
            logger.info("Успешно создан движок базы данных.")
        except Exception as e:
            logger.error(f"Ошибка при создании движка базы данных: {e}")
            st.error("Не удалось подключиться к базе данных.")

    async def create_tables(self):
        """Создает таблицы в базе данных, если они еще не существуют."""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(self.metadata.create_all)
                logger.info("Таблицы успешно созданы или уже существуют.")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц: {e}")
            st.error("Не удалось создать таблицы в базе данных.")

    async def get_session(self):
        """Создает асинхронную сессию для работы с базой данных."""
        return AsyncSession(self.engine)

class NameManager:
    def __init__(self, db):
        self.db = db
        self.names_list = ["Андрей", "Сергей", "Иван", "Вероника", "Катя", "Даня", "Маша", "Таня", "Влад", "Наташа"]

    async def load_used_names(self, session):
        """Загружает уже использованные имена из базы данных."""
        try:
            result = await session.execute(select(self.db.used_names_table))
            records = result.fetchall()
            logger.info("Успешно загружены использованные имена.")
            return pd.DataFrame(records, columns=["id", "Name", "Date"])
        except Exception as e:
            logger.error(f"Ошибка при загрузке использованных имен: {e}")
            st.error("Не удалось загрузить данные из базы данных.")
            return pd.DataFrame(columns=["id", "Name", "Date"])

    async def get_random_name(self, session):
        """Выбирает случайное имя и сохраняет его в базе данных."""
        try:
            used_names_df = await self.load_used_names(session)
            available_names = [name for name in self.names_list if name not in used_names_df["Name"].values]

            if not available_names:
                st.warning("Все имена уже использованы. Очищаю базу данных и начинаю заново.")
                await session.execute(delete(self.db.used_names_table))
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
            await session.execute(self.db.used_names_table.insert().values(new_entry))
            await session.commit()
            logger.info(f"Имя {selected_name} успешно добавлено в базу данных.")
            return selected_name

        except Exception as e:
            logger.error(f"Ошибка при выборе или сохранении имени: {e}")
            st.error("Произошла ошибка при обработке имени.")

    async def get_history(self, session):
        """Получает историю использованных имен."""
        try:
            result = await session.execute(select(self.db.used_names_table))
            records = result.fetchall()
            history_df = pd.DataFrame(records, columns=["id", "Name", "Date"])
            logger.info("История имен успешно загружена.")
            return history_df
        except Exception as e:
            logger.error(f"Ошибка при получении истории имен: {e}")
            st.error("Не удалось загрузить историю имен.")
            return pd.DataFrame(columns=["id", "Name", "Date"])

# Основная функция
async def main():
    """Основная функция приложения Streamlit."""
    db = Database(get_database_url())
    await db.create_tables()
    
    name_manager = NameManager(db)
    
    st.title("Кто ведет MN?")
    st.write("Решит удача и немного кода:")

    # Создание сессии
    try:
        async with db.get_session() as session:
            if st.button("Получить имя"):
                await name_manager.get_random_name(session)

            if st.button("Сбросить все"):
                st.warning("Очищаю базу данных и начинаю заново.")
                await session.execute(delete(db.used_names_table))
                await session.commit()
                logger.info("База данных очищена по запросу пользователя.")

            if st.button("Показать историю"):
                history_df = await name_manager.get_history(session)
                st.write(history_df)
                
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
