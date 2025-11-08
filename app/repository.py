import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, User, Pass, Coords, Image
from datetime import datetime

# Параметры подключения из переменных окружения
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
            # --- Пользователь ---
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

            # --- Координаты ---
            coords_data = data["coords"]
            coords = Coords(
                latitude=float(coords_data["latitude"]),
                longitude=float(coords_data["longitude"]),
                height=int(coords_data["height"]),
            )
            self.db.add(coords)
            self.db.commit()
            self.db.refresh(coords)

            # --- Перевал ---
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

            # --- Изображения ---
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
        return self.db.query(Pass).filter(Pass.id == pass_id).first()

    def update_pass(self, pass_id: int, data: dict):
        pass_obj = self.db.query(Pass).filter(Pass.id == pass_id).first()
        if not pass_obj:
            return 0, "Перевал не найден"
        if pass_obj.status != "new":
            return 0, "Запись нельзя редактировать — статус не new"

        pass_obj.beauty_title = data.get("beauty_title", pass_obj.beauty_title)
        pass_obj.title = data.get("title", pass_obj.title)
        pass_obj.other_titles = data.get("other_titles", pass_obj.other_titles)
        pass_obj.connect = data.get("connect", pass_obj.connect)
        pass_obj.add_time = datetime.fromisoformat(data["add_time"]) if "add_time" in data else pass_obj.add_time
        pass_obj.level_winter = data["level"].get("winter", pass_obj.level_winter)
        pass_obj.level_summer = data["level"].get("summer", pass_obj.level_summer)
        pass_obj.level_autumn = data["level"].get("autumn", pass_obj.level_autumn)
        pass_obj.level_spring = data["level"].get("spring", pass_obj.level_spring)

        if "images" in data:
            self.db.query(Image).filter(Image.pass_id == pass_id).delete()
            for img in data["images"]:
                image_obj = Image(
                    pass_id=pass_id,
                    data=img["data"],
                    title=img.get("title")
                )
                self.db.add(image_obj)

        self.db.commit()
        return 1, "Запись успешно обновлена"

    def get_passes_by_user_email(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return []
        return self.db.query(Pass).filter(Pass.user_id == user.id).all()
