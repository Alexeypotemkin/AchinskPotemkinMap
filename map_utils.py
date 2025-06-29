from typing import Tuple, Dict, List
import math


def calculate_spn(toponym: Dict) -> Tuple[str, str]:
    """Вычисляет размеры объекта в градусной мере"""
    envelope = toponym['boundedBy']['Envelope']
    lower = list(map(float, envelope['lowerCorner'].split()))
    upper = list(map(float, envelope['upperCorner'].split()))

    delta_lon = str(abs(upper[0] - lower[0]))
    delta_lat = str(abs(upper[1] - lower[1]))

    return delta_lon, delta_lat


def get_map_params_for_two_points(point1: List[float], point2: List[float], apikey: str) -> Dict:
    """Формирует параметры карты для отображения двух точек"""
    # Вычисляем среднюю точку для центра карты
    center_lon = (point1[0] + point2[0]) / 2
    center_lat = (point1[1] + point2[1]) / 2

    # Вычисляем охват карты
    delta_lon = abs(point1[0] - point2[0]) * 1.5
    delta_lat = abs(point1[1] - point2[1]) * 1.5

    # Минимальный размер
    delta_lon = max(delta_lon, 0.005)
    delta_lat = max(delta_lat, 0.005)

    return {
        "ll": f"{center_lon},{center_lat}",
        "spn": f"{delta_lon},{delta_lat}",
        "l": "map",
        "pt": f"{point1[0]},{point1[1]},pm2rdl~{point2[0]},{point2[1]},pm2gnl",
        "apikey": apikey
    }


def calculate_distance(point1: List[float], point2: List[float]) -> float:
    """Вычисляет расстояние между двумя точками в метрах (упрощённая формула)"""
    lon1, lat1 = point1
    lon2, lat2 = point2

    # Коэффициенты для перевода в метры
    dx = (lon2 - lon1) * 111000 * math.cos(math.radians(lat1))
    dy = (lat2 - lat1) * 111000

    return math.sqrt(dx * dx + dy * dy)