import requests
import json

# URL твоего API
url = "http://127.0.0.1:8000/submitData"

# Пример JSON для перевала
payload = {
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "соединяет долины",
    "add_time": "2021-09-22T13:18:13",
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
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "images": [
        {
            "data": "iVBORw0KGgoAAAANSUhEUgAAAAUA\
AAAFCAYAAACNbyblAAAAHElEQVQI12P4\
//8/w38GIAXDIBKE0DHxgljNBAAO\
9TXL0Y4OHwAAAABJRU5ErkJggg==",
            "title": "Седловина"
        }
    ]
}

# Отправка POST-запроса
response = requests.post(url, json=payload)

# Вывод результата
print("Статус:", response.status_code)
print("Ответ JSON:", response.json())