import requests


class OpenWeather:

    def __init__(self) -> None:
        self.TOKEN = "TOKEN"
        self.URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}"

    def raw_call(self, city):
        request_url = self.URL.format(city, self.TOKEN)
        response = requests.get(request_url)
        return response
