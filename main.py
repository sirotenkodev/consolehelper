import re
import jinja2
from settings import Settings
from weather_parser import WeatherRequest

settings = {}
weatherRequest = WeatherRequest()

def contains_any(text, words):
    return any(word in text for word in words)

def help_parser():
    print("""
        Привет!
        Я могу подсказать тебе погоду
        Только спроси: Какая погода в городе Х?
    """)

def extract_word_from_query(text):
    match = re.search(r'[вВ]\s+(?:город\s+)?([а-яА-ЯёЁa-zA-Z\-]+)', text)
    if match:
        return match.group(1)
    return None

def weather_from_city(query):
    extract_word = extract_word_from_query(query)
    ls = settings.get_settings()
    weather = weatherRequest.get_weather(ls["baseurl"], extract_word, ls["appid"])
    print_weather(weather)

def weather_from_savecity(query):
    ls = settings.get_settings()
    if len(ls["city"]) > 0:
        city = ls["city"]
    else:
        city = "Москва"
    weather = weatherRequest.get_weather(ls["baseurl"], city, ls["appid"])
    print_weather(weather)

def weather_parser(query):
    print("Парсим погоду из:", query)
    if " в " in query or " in " in query:
        weather_from_city(query)
    else:
        weather_from_savecity(query)


def query_parser(query  ):
    query = query.lower()
    if "погода" in query or "weather" in query:
        weather_parser(query)

    if "привет" in query or "hello in query" in query:
        help_parser()

def print_weather(weather):
    print(f"Погода в городе {weather["name"]}")
    print(f"Ощущается как {weather["main"]["feels_like"]}")
    print(f"Описание: {weather["weather"][0]["description"]}")

test_queries = [
    "Привет!",
    "Погода сейчас",
    "Погода завтра",
    "Погода в Омск",
    "Погода в Москва"
]

if __name__ == "__main__":
    settings = Settings()
    for query in test_queries:
        query_parser(query)
