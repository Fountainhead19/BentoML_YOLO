import requests
import json
import base64

#Адрес Bento сервиса
BENTO_URL = "http://localhost:3000"


IMAGE_PATH = "chicken_test.jpg"

# Параметры (порог для вероятности)
parameters = {"conf": 0.3}

# Запрос для простого подсчета куриц
with open(IMAGE_PATH, "rb") as f:
    files = {"image": f}
    data = {"parameters": json.dumps(parameters)}

    print("Запрос на /count")
    count_response = requests.post(f"{BENTO_URL}/count", files=files, data=data)

    if count_response.ok:
        print("Кол-во куриц на фотке:", count_response.json())
    else:
        print("Error", count_response.status_code, count_response.text)

# Запрос кол-во куриц + боксы
with open(IMAGE_PATH, "rb") as f:
    files = {"image": f}
    data = {"parameters": json.dumps(parameters)}

    print("Запрос на /annotate")
    annotate_response = requests.post(f"{BENTO_URL}/annotate", files=files, data=data)

    if annotate_response.ok:
        result = annotate_response.json()
        print("Кол-во куриц на фотке:", result["count"])

        #Сохраняем фотку
        with open("annotated.jpg", "wb") as out_img:
            out_img.write(base64.b64decode(result["image_base64"]))
        print("Фотка готова в: annotated.jpg")

    else:
        print("Error", annotate_response.status_code, annotate_response.text)


