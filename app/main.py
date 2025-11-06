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
    except Exception as e:
        # выводим текст ошибки в лог, чтобы проще было отлаживать
        print("Ошибка при обработке данных:", e)
        raise HTTPException(status_code=500, detail="Ошибка при обработке данных")
