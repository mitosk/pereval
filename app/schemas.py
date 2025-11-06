# app/schemas.py
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    email: str
    fam: str
    name: str
    otc: str
    phone: str

class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int

class LevelSchema(BaseModel):
    winter: Optional[str] = ""
    summer: Optional[str] = ""
    autumn: Optional[str] = ""
    spring: Optional[str] = ""

class ImageSchema(BaseModel):
    data: str
    title: str

class PassCreateSchema(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = ""
    connect: Optional[str] = ""
    add_time: datetime  # ✅ Pydantic сам конвертирует строку в datetime
    user: UserSchema
    coords: CoordsSchema
    level: LevelSchema
    images: List[ImageSchema]
