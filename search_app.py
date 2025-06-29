import sys
from io import BytesIO
import requests
from PIL import Image
from map_utils import get_map_params


def main():
    if len(sys.argv) < 2:
        print("Введите адрес для поиска")
        return

    # API ключи
    GEOCODER_API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
    STATIC_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    # Поиск адреса через геокодер
    toponym_to_find = " ".join(sys.argv[1:])
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": toponym_to_find,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print("Ошибка выполнения запроса к геокодеру:")
        print(response.url)
        print(f"HTTP статус: {response.status_code} ({response.reason})")
        return

    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except (KeyError, IndexError):
        print("Не удалось найти указанный адрес")
        return

    # Получаем параметры для карты
    map_params = get_map_params(toponym, STATIC_API_KEY)

    # Запрос карты
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    if not response:
        print("Ошибка выполнения запроса к StaticAPI:")
        print(response.url)
        print(f"HTTP статус: {response.status_code} ({response.reason})")
        return

    # Показываем карту
    try:
        Image.open(BytesIO(response.content)).show()
    except Exception as e:
        print(f"Ошибка при отображении карты: {e}")


if __name__ == "__main__":
    main()