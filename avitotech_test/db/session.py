from environs import Env
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

DB_NAME = env('DB_NAME')
DB_HOST = env('DB_HOST')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')

# Настройки для подключения к базе данных (подставьте свои значения)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Создаём движок и сессию
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    """Dependency for getting async session"""
    try:
        AsyncSession = async_session()
        yield AsyncSession
    finally:
        await AsyncSession.close()
