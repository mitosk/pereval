import requests

BASE_URL = "http://127.0.0.1:8000/submitData"

# --- 1. POST /submitData ---
post_payload = {
    "beauty_title": "пер.",
    "title": "Пхия",
    "other_titles": "Тестовый перевал",
    "connect": "соединяет долины рек...",
    "add_time": "2023-10-01T12:00:00",
    "user": {
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович",
        "phone": "+7 555 55 55"
    },
    "coords": {
        "latitude": 45.3842,
        "longitude": 7.1525,
        "height": 1200
    },
    "level": {
        "winter": "1A",
        "summer": "1A",
        "autumn": "1A",
        "spring": "1A"
    },
    "images": [
        {"data": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
         "title": "Седловина"}
    ]
}

response = requests.post(BASE_URL, json=post_payload)
print("=== 1. POST /submitData ===")
print("Статус:", response.status_code)
post_result = response.json()
print("Ответ JSON:", post_result)

new_id = post_result.get("id")

# --- 2. GET /submitData/{id} ---
response = requests.get(f"{BASE_URL}/{new_id}")
print("\n=== 2. GET /submitData/{id} ===")
print("Статус:", response.status_code)
print("Ответ JSON:", response.json())

# --- 3. PATCH /submitData/{id} ---
patch_payload = post_payload.copy()
patch_payload["title"] = "Пхия - обновлённый"
patch_payload["connect"] = "обновлённое соединение долин рек..."

response = requests.patch(f"{BASE_URL}/{new_id}", json=patch_payload)
print("\n=== 3. PATCH /submitData/{id} ===")
print("Статус:", response.status_code)
print("Ответ JSON:", response.json())

# --- 4. GET /submitData/?user__email=<email> ---
response = requests.get(f"{BASE_URL}/", params={"user__email": "qwerty@mail.ru"})
print("\n=== 4. GET /submitData/?user__email=<email> ===")
print("Статус:", response.status_code)
print("Ответ JSON:", response.json())
