from pydantic import BaseModel
from typing import Optional, List, Dict


class UserSchema(BaseModel):
    email: str
    fam: str
    name: str
    otc: Optional[str]
    phone: Optional[str]


class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int


class ImageSchema(BaseModel):
    data: str
    title: Optional[str]


class LevelSchema(BaseModel):
    winter: Optional[str]
    summer: Optional[str]
    autumn: Optional[str]
    spring: Optional[str]


class PassCreateSchema(BaseModel):
    beauty_title: Optional[str]
    title: str
    other_titles: Optional[str]
    connect: Optional[str]
    add_time: str  # ISO формат, например "2025-11-06T21:00:00"
    user: UserSchema
    coords: CoordsSchema
    level: LevelSchema
    images: Optional[List[ImageSchema]] = []
