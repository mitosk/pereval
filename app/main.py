from fastapi import FastAPI, HTTPException, Query
from fastapi import Depends
from sqlalchemy.orm import Session
from .repository import PassRepository
from .schemas import (
    PassCreateSchema,
    PassUpdateSchema,
    PassResponseSchema,
    PatchResponseSchema
)
from .config import MEDIA_ROOT

app = FastAPI()


@app.post("/submitData")
def submit_data(payload: PassCreateSchema):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        new_id = repo.create_pass(payload.dict())
        return {"status": 200, "message": None, "id": new_id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при обработке данных")


@app.get("/submitData/{pass_id}", response_model=PassResponseSchema)
def get_pass(pass_id: int):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        pass_obj = repo.get_pass_by_id(pass_id)
        if not pass_obj:
            raise HTTPException(status_code=404, detail="Перевал не найден")
        return pass_obj
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при обработке данных")


@app.patch("/submitData/{pass_id}", response_model=PatchResponseSchema)
def update_pass(pass_id: int, payload: PassUpdateSchema):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        success, message = repo.update_pass(pass_id, payload.dict(exclude_unset=True))
        return {"state": 1 if success else 0, "message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/submitData/", response_model=list[PassResponseSchema])
def get_passes_by_user(email: str = Query(..., alias="user__email")):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        passes = repo.get_passes_by_user_email(email)
        return passes
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при обработке данных")
