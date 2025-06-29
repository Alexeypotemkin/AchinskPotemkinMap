import requests
from io import BytesIO
from PIL import Image
from map_utils import get_map_params


def search_organizations(address_ll: str, search_text: str):
    # API ключи
    SEARCH_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    STATIC_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    # Поиск организаций
    search_api_server = "https://search-maps.yandex.ru/v1/"

    search_params = {
        "apikey": SEARCH_API_KEY,
        "text": search_text,
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)

    if not response:
        print("Ошибка выполнения запроса к API поиска:")
        print(response.url)
        print(f"HTTP статус: {response.status_code} ({response.reason})")
        return

    try:
        json_response = response.json()
        organization = json_response["features"][0]
        org_point = organization["geometry"]["coordinates"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]

        print(f"Найдена организация: {organization['properties']['name']}")
        print(f"Адрес: {org_address}")

        # Получаем параметры для карты
        map_params = {
            "ll": address_ll,
            "spn": "0.05,0.05",
            "l": "map",
            "pt": f"{org_point[0]},{org_point[1]},pm2rdl",
            "apikey": STATIC_API_KEY
        }

        # Запрос карты
        map_api_server = "https://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса к StaticAPI:")
            print(response.url)
            print(f"HTTP статус: {response.status_code} ({response.reason})")
            return

        # Показываем карту
        Image.open(BytesIO(response.content)).show()

    except (KeyError, IndexError):
        print("Не удалось найти организации по запросу")


if __name__ == "__main__":
    search_organizations("37.588392,55.734036", "аптека")