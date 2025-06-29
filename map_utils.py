from typing import Tuple


def calculate_spn(toponym: dict) -> Tuple[str, str]:
    """Вычисляет размеры объекта в градусной мере для параметра spn"""
    envelope = toponym['boundedBy']['Envelope']
    lower_corner = envelope['lowerCorner'].split()
    upper_corner = envelope['upperCorner'].split()

    delta_lon = str(abs(float(upper_corner[0]) - float(lower_corner[0])))
    delta_lat = str(abs(float(upper_corner[1]) - float(lower_corner[1])))

    return delta_lon, delta_lat


def get_map_params(toponym: dict, apikey: str) -> dict:
    """Формирует параметры для запроса к StaticAPI"""
    delta_lon, delta_lat = calculate_spn(toponym)
    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_latitude = toponym_coordinates.split()

    return {
        "ll": ",".join([toponym_longitude, toponym_latitude]),
        "spn": ",".join([delta_lon, delta_lat]),
        "l": "map",
        "pt": f"{toponym_longitude},{toponym_latitude},pm2rdl",
        "apikey": apikey
    }