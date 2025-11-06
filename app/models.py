from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    fam = Column(String, nullable=False)
    name = Column(String, nullable=False)
    otc = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    passes = relationship("Pass", back_populates="user")


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)

    passes = relationship("Pass", back_populates="coords")


class Pass(Base):
    __tablename__ = "passes"

    id = Column(Integer, primary_key=True)
    beauty_title = Column(String, nullable=True)
    title = Column(String, nullable=False)
    other_titles = Column(String, nullable=True)
    connect = Column(String, nullable=True)
    add_time = Column(DateTime, nullable=False)
    status = Column(String, default="new")  # статус модерации

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coords_id = Column(Integer, ForeignKey("coords.id"), nullable=False)

    level_winter = Column(String, nullable=True)
    level_summer = Column(String, nullable=True)
    level_autumn = Column(String, nullable=True)
    level_spring = Column(String, nullable=True)

    user = relationship("User", back_populates="passes")
    coords = relationship("Coords", back_populates="passes")
    images = relationship("Image", back_populates="pass_obj")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    pass_id = Column(Integer, ForeignKey("passes.id"), nullable=False)
    data = Column(Text, nullable=False)  # base64
    title = Column(String, nullable=True)

    pass_obj = relationship("Pass", back_populates="images")
