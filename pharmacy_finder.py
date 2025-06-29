import sys
import requests
from io import BytesIO
from PIL import Image
from typing import Dict, List, Optional
from map_utils import calculate_spn, get_map_params_for_two_points, calculate_distance

# API ключи
GEOCODER_API_KEY = "02932015-fa68-46f0-a730-e4a597aa51f0"
SEARCH_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
STATIC_API_KEY = "5029b410-09bd-4da8-87fa-27be4fb56096"


def geocode(address: str) -> Optional[Dict]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": address,
        "format": "json"
    }

    try:
        response = requests.get(
            "http://geocode-maps.yandex.ru/1.x/",
            params=params,
            headers=headers
        )
        response.raise_for_status()

        json_data = response.json()
        features = json_data["response"]["GeoObjectCollection"]["featureMember"]
        if not features:
            return None

        return features[0]["GeoObject"]
    except Exception as e:
        print(f"Ошибка геокодирования: {e}")
        return None


def find_nearest_pharmacy(coords: str) -> Optional[Dict]:
    """Поиск ближайшей аптеки"""
    search_url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": SEARCH_API_KEY,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": coords,
        "type": "biz",
        "results": 1
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()

        json_data = response.json()
        features = json_data.get("features", [])
        if not features:
            return None

        return features[0]
    except Exception as e:
        print(f"Ошибка поиска аптеки: {e}")
        return None


def create_snippet(pharmacy: Dict, distance: float) -> str:
    """Создаёт информационный сниппет об аптеке"""
    meta = pharmacy["properties"]["CompanyMetaData"]

    snippet = [
        f"Аптека: {meta.get('name', 'Название не указано')}",
        f"Адрес: {meta.get('address', 'Адрес не указан')}",
        f"Расстояние: {distance:.0f} метров"
    ]

    if "Hours" in meta:
        hours = meta["Hours"]["text"]
        snippet.append(f"Часы работы: {hours}")

    return "\n".join(snippet)


def main():
    if len(sys.argv) < 2:
        print("Использование: python pharmacy_finder.py 'адрес'")
        return

    address = " ".join(sys.argv[1:])

    # 1. Находим координаты исходного адреса
    location = geocode(address)
    if not location:
        print(f"Не удалось найти адрес: {address}")
        return

    location_coords = list(map(float, location["Point"]["pos"].split()))
    location_coords_str = f"{location_coords[0]},{location_coords[1]}"

    # 2. Ищем ближайшую аптеку
    pharmacy = find_nearest_pharmacy(location_coords_str)
    if not pharmacy:
        print("Не удалось найти ближайшую аптеку")
        return

    pharmacy_coords = pharmacy["geometry"]["coordinates"]
    distance = calculate_distance(location_coords, pharmacy_coords)

    # 3. Формируем информационный сниппет
    snippet = create_snippet(pharmacy, distance)
    print("\nИнформация об аптеке:")
    print(snippet)

    # 4. Получаем карту с двумя точками
    map_params = get_map_params_for_two_points(location_coords, pharmacy_coords, STATIC_API_KEY)
    map_url = "https://static-maps.yandex.ru/1.x/"

    try:
        response = requests.get(map_url, params=map_params)
        response.raise_for_status()

        # Показываем карту
        Image.open(BytesIO(response.content)).show()
    except Exception as e:
        print(f"Ошибка при загрузке карты: {e}")


if __name__ == "__main__":
    main()