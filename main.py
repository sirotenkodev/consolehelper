import re
import jinja2
from settings import Settings
from weather_parser import WeatherRequest

settings = None
weatherRequest = WeatherRequest()

def get_settings_instance():
    global settings
    if not isinstance(settings, Settings):
        settings = Settings()
    return settings

def contains_any(text, words):
    return any(word in text for word in words)

def help_parser():
    print("""
        Привет!
        Я могу подсказать тебе погоду
        Только спроси: Какая погода в городе Х?
    """)


def normalize_city_name(city):
    if not city:
        return None

    city = city.strip().lower()
    normalization = {
        "омске": "Омск",
        "москве": "Москва",
        "петербурге": "Санкт-Петербург",
        "питере": "Санкт-Петербург",
        "санкт-петербурге": "Санкт-Петербург",
        "екатеринбурге": "Екатеринбург",
        "новосибирске": "Новосибирск"
    }

    if city in normalization:
        return normalization[city]

    if city.endswith("е") and len(city) > 3:
        return city[:-1].capitalize()

    return city.capitalize()


def extract_city_from_query(text):
    lower_text = text.lower()
    patterns = [
        r'(?:в|во)\s+(?:городе|город|г\.?)(?:\s+)?([а-яёa-zA-Z\-]+)',
        r'(?:в|во)\s+([а-яёa-zA-Z\-]+)',
        r'\b(?:городе|город|г\.?\s*)\s+([а-яёa-zA-Z\-]+)\b'
    ]
    temporal_words = {"сейчас", "сегодня", "завтра"}

    for pattern in patterns:
        match = re.search(pattern, lower_text)
        if match:
            city = normalize_city_name(match.group(1))
            if city and city.lower() in temporal_words:
                return None
            return city

    known_cities = [
        "москва",
        "омск",
        "омске",
        "москве",
        "санкт-петербург",
        "петербург",
        "екатеринбург",
        "новосибирск"
    ]
    for known in known_cities:
        if known in lower_text:
            return normalize_city_name(known)

    return None


def is_day_request(query):
    return any(word in query for word in ["сегодня", "завтра"])


def get_target_city(query):
    city = extract_city_from_query(query)
    if city:
        return city

    ls = get_settings_instance().get_settings()
    if ls.get("city"):
        return ls["city"]

    return "Москва"


def weather_for_city(city):
    ls = get_settings_instance().get_settings()
    weather = weatherRequest.get_weather(ls["baseurl"], city, ls["appid"])
    print_weather(weather)


def weather_parser(query):
    print("Парсим погоду из:", query)
    city = get_target_city(query)
    weather_for_city(city)


def query_parser(query):
    query = query.lower()
    if "привет" in query or "hello" in query:
        help_parser()

    if "погода" in query or "weather" in query:
        weather_parser(query)


def print_weather(weather):
    print(f"Погода в городе {weather['name']}")
    print(f"Ощущается как {weather['main']['feels_like']}")
    print(f"Описание: {weather['weather'][0]['description']}")


test_queries = [
    "Привет!",
    "Погода сейчас",
    "Погода сегодня",
    "Погода завтра",
    "Погода в Омск",
    "Погода в Москва",
    "Погода в городе Омск",
    "Погода в Омске"
]

if __name__ == "__main__":
    settings = Settings()
    for query in test_queries:
        query_parser(query)
