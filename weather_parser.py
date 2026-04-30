import requests

class WeatherRequest:
    def get_weather(self, baseurl, city, appid):
        city = city or "Москва"
        if not appid:
            return self._mock_weather(city)

        try:
            response = requests.get(
                baseurl,
                params={"q": city, "appid": appid, "units": "metric"},
                timeout=5
            )
            data = response.json()
            if response.status_code != 200 or "name" not in data:
                return self._mock_weather(city)
            return data
        except Exception:
            return self._mock_weather(city)

    def _mock_weather(self, city):
        return {
            "name": city,
            "main": {"feels_like": 20},
            "weather": [{"description": "ясно"}]
        }

