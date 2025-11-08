import requests
import json

BASE_URL = "http://127.0.0.1:8000/submitData"

# --- Данные для нового перевала ---
payload = {
    "beauty_title": "Красивый перевал",
    "title": "Перевал Тестовый",
    "other_titles": "Тестовый",
    "connect": "Маршрут 1",
    "add_time": "2025-11-06T21:00:00",
    "user": {
        "email": "qwerty@mail.ru",
        "fam": "Иванов",
        "name": "Иван",
        "otc": "Иванович",
        "phone": "+79991234567"
    },
    "coords": {
        "latitude": 60.0,
        "longitude": 30.0,
        "height": 200
    },
    "level": {
        "winter": "3A",
        "summer": "1B",
        "autumn": "2B",
        "spring": "1A"
    },
    "images": [
        {"data": "base64encodedstring", "title": "Вид с перевала"}
    ]
}

# --- POST /submitData ---
response = requests.post(BASE_URL, json=payload)
print("POST статус:", response.status_code)
print("Ответ JSON:", response.json())

# --- GET /submitData/<id> ---
pass_id = response.json().get("id")
if pass_id:
    response_get = requests.get(f"{BASE_URL}/{pass_id}")
    print("GET по ID статус:", response_get.status_code)
    print("GET по ID ответ:", response_get.json())

# --- PATCH /submitData/<id> ---
payload_update = payload.copy()
payload_update["title"] = "Перевал Тестовый Обновлённый"
response_patch = requests.patch(f"{BASE_URL}/{pass_id}", json=payload_update)
print("PATCH статус:", response_patch.status_code)
print("PATCH ответ:", response_patch.json())

# --- GET /submitData/?user__email=<email> ---
response_user = requests.get(f"{BASE_URL}/", params={"email": payload["user"]["email"]})
print("GET по email статус:", response_user.status_code)
print("GET по email ответ:", response_user.json())
