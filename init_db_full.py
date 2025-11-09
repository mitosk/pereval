# init_db_full.py
import os
from sqlalchemy import create_engine
from app.database import Base

# Настройки из переменных окружения
DB_USER = os.getenv("FSTR_DB_LOGIN", "pereval_user")
DB_PASS = os.getenv("FSTR_DB_PASS", "pereval_pass")
DB_HOST = os.getenv("FSTR_DB_HOST", "localhost")
DB_PORT = os.getenv("FSTR_DB_PORT", "5432")
DB_NAME = os.getenv("FSTR_DB_NAME", "pereval_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаём все таблицы
print("Создаём таблицы...")
Base.metadata.create_all(bind=engine)
print("Таблицы созданы!")
