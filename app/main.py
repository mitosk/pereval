from fastapi import FastAPI, HTTPException
from .repository import PassRepository
from .schemas import PassCreateSchema
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


@app.get("/submitData/{pass_id}")
def get_pass(pass_id: int):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        pass_obj = repo.get_pass_by_id(pass_id)
        if not pass_obj:
            raise HTTPException(status_code=404, detail="Перевал не найден")
        return pass_obj
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при получении данных")


@app.patch("/submitData/{pass_id}")
def update_pass(pass_id: int, payload: PassCreateSchema):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        state, message = repo.update_pass(pass_id, payload.dict())
        return {"state": state, "message": message}
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении данных")


@app.get("/submitData/")
def get_passes_by_user(email: str):
    repo = PassRepository(media_root=MEDIA_ROOT)
    try:
        passes = repo.get_passes_by_user_email(email)
        return passes
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при получении данных")
