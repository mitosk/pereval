from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    fam = Column(String, nullable=False)
    name = Column(String, nullable=False)
    otc = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    passes = relationship("Pass", back_populates="user")


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)

    passes = relationship("Pass", back_populates="coords")


class Pass(Base):
    __tablename__ = "pereval_added"

    id = Column(Integer, primary_key=True, autoincrement=True)
    beauty_title = Column(String)
    title = Column(String, nullable=False)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="new")  # статус модерации

    user_id = Column(Integer, ForeignKey("users.id"))
    coords_id = Column(Integer, ForeignKey("coords.id"))

    level_winter = Column(String)
    level_summer = Column(String)
    level_autumn = Column(String)
    level_spring = Column(String)

    user = relationship("User", back_populates="passes")
    coords = relationship("Coords", back_populates="passes")
    images = relationship("Image", back_populates="pass_obj")


class Image(Base):
    __tablename__ = "pereval_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pass_id = Column(Integer, ForeignKey("pereval_added.id"))
    data = Column(String, nullable=False)
    title = Column(String)

    pass_obj = relationship("Pass", back_populates="images")
