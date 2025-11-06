# app/init_db.py
from .models import Base
from .repository import engine

def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
    print("Все таблицы успешно созданы!")

if __name__ == "__main__":
    create_tables()
