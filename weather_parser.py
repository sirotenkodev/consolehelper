import requests, json

class WeatherRequest:
    def get_weather(self, baseurl, city,appid):
        return requests.get(baseurl + "?q=" + city + "&appid=" + appid + "&units=metric").json()

