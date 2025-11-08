from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict


class UserSchema(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: Optional[str] = None


class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int


class LevelSchema(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class ImageSchema(BaseModel):
    data: str  # Base64
    title: Optional[str] = None


class PassCreateSchema(BaseModel):
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: str
    user: UserSchema
    coords: CoordsSchema
    level: Optional[LevelSchema] = LevelSchema()
    images: Optional[List[ImageSchema]] = []


class PassUpdateSchema(BaseModel):
    beauty_title: Optional[str] = None
    title: Optional[str] = None
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: Optional[str] = None
    coords: Optional[CoordsSchema] = None
    level: Optional[LevelSchema] = None
    images: Optional[List[ImageSchema]] = None


class PassResponseSchema(BaseModel):
    id: int
    beauty_title: Optional[str]
    title: str
    other_titles: Optional[str]
    connect: Optional[str]
    add_time: str
    status: str
    user_id: int
    coords_id: int
    level_winter: Optional[str]
    level_summer: Optional[str]
    level_autumn: Optional[str]
    level_spring: Optional[str]


class PatchResponseSchema(BaseModel):
    state: int
    message: str
