import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, User, Pass, Coords, Image
from datetime import datetime

# Параметры подключения к БД из переменных окружения
DB_HOST = os.getenv("FSTR_DB_HOST", "localhost")
DB_PORT = os.getenv("FSTR_DB_PORT", "5432")
DB_USER = os.getenv("FSTR_DB_LOGIN", "postgres")
DB_PASS = os.getenv("FSTR_DB_PASS", "postgres")
DB_NAME = os.getenv("FSTR_DB_NAME", "pereval_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class PassRepository:
    def __init__(self, media_root: str):
        self.db: Session = SessionLocal()
        self.media_root = media_root

    def create_pass(self, data: dict):
        try:
            # Работа с пользователем
            user_data = data["user"]
            user = self.db.query(User).filter_by(email=user_data["email"]).first()
            if not user:
                user = User(
                    email=user_data["email"],
                    fam=user_data["fam"],
                    name=user_data["name"],
                    otc=user_data.get("otc"),
                    phone=user_data.get("phone"),
                )
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)

            # Работа с координатами
            coords_data = data["coords"]
            coords = Coords(
                latitude=float(coords_data["latitude"]),
                longitude=float(coords_data["longitude"]),
                height=int(coords_data["height"]),
            )
            self.db.add(coords)
            self.db.commit()
            self.db.refresh(coords)

            # Создание перевала
            pass_obj = Pass(
                beauty_title=data.get("beauty_title"),
                title=data["title"],
                other_titles=data.get("other_titles"),
                connect=data.get("connect"),
                add_time=datetime.fromisoformat(data["add_time"]),
                status="new",
                user_id=user.id,
                coords_id=coords.id,
                level_winter=data["level"].get("winter"),
                level_summer=data["level"].get("summer"),
                level_autumn=data["level"].get("autumn"),
                level_spring=data["level"].get("spring"),
            )
            self.db.add(pass_obj)
            self.db.commit()
            self.db.refresh(pass_obj)

            # Работа с изображениями
            for img in data.get("images", []):
                image_obj = Image(
                    pass_id=pass_obj.id,
                    data=img["data"],
                    title=img.get("title")
                )
                self.db.add(image_obj)
            self.db.commit()

            return pass_obj.id

        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_pass_by_id(self, pass_id: int):
        try:
            pass_obj = self.db.query(Pass).filter_by(id=pass_id).first()
            if not pass_obj:
                return None
            result = {
                "id": pass_obj.id,
                "beauty_title": pass_obj.beauty_title,
                "title": pass_obj.title,
                "other_titles": pass_obj.other_titles,
                "connect": pass_obj.connect,
                "add_time": pass_obj.add_time.isoformat(),
                "status": pass_obj.status,
                "user_id": pass_obj.user_id,
                "coords_id": pass_obj.coords_id,
                "level_winter": pass_obj.level_winter,
                "level_summer": pass_obj.level_summer,
                "level_autumn": pass_obj.level_autumn,
                "level_spring": pass_obj.level_spring
            }
            return result
        finally:
            self.db.close()

    def update_pass(self, pass_id: int, data: dict):
        try:
            pass_obj = self.db.query(Pass).filter_by(id=pass_id).first()
            if not pass_obj:
                return 0, "Перевал не найден"
            if pass_obj.status != "new":
                return 0, "Редактировать можно только записи со статусом 'new'"

            # Обновляем поля перевала, кроме данных пользователя
            pass_obj.beauty_title = data.get("beauty_title", pass_obj.beauty_title)
            pass_obj.title = data.get("title", pass_obj.title)
            pass_obj.other_titles = data.get("other_titles", pass_obj.other_titles)
            pass_obj.connect = data.get("connect", pass_obj.connect)
            if "add_time" in data:
                pass_obj.add_time = datetime.fromisoformat(data["add_time"])
            levels = data.get("level", {})
            pass_obj.level_winter = levels.get("winter", pass_obj.level_winter)
            pass_obj.level_summer = levels.get("summer", pass_obj.level_summer)
            pass_obj.level_autumn = levels.get("autumn", pass_obj.level_autumn)
            pass_obj.level_spring = levels.get("spring", pass_obj.level_spring)

            # Координаты
            if "coords" in data:
                coords_data = data["coords"]
                coords_obj = self.db.query(Coords).filter_by(id=pass_obj.coords_id).first()
                if coords_obj:
                    coords_obj.latitude = float(coords_data.get("latitude", coords_obj.latitude))
                    coords_obj.longitude = float(coords_data.get("longitude", coords_obj.longitude))
                    coords_obj.height = int(coords_data.get("height", coords_obj.height))

            self.db.commit()
            return 1, "Запись успешно обновлена"
        except Exception as e:
            self.db.rollback()
            return 0, str(e)
        finally:
            self.db.close()

    def get_passes_by_user_email(self, email: str):
        try:
            user = self.db.query(User).filter_by(email=email).first()
            if not user:
                return []

            passes = self.db.query(Pass).filter_by(user_id=user.id).all()
            result_list = []
            for p in passes:
                result_list.append({
                    "id": p.id,
                    "beauty_title": p.beauty_title,
                    "title": p.title,
                    "other_titles": p.other_titles,
                    "connect": p.connect,
                    "add_time": p.add_time.isoformat(),
                    "status": p.status,
                    "user_id": p.user_id,
                    "coords_id": p.coords_id,
                    "level_winter": p.level_winter,
                    "level_summer": p.level_summer,
                    "level_autumn": p.level_autumn,
                    "level_spring": p.level_spring
                })
            return result_list
        finally:
            self.db.close()
