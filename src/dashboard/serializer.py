from rest_framework import serializers


class WeatherSerilizer(serializers.Serializer):
    name = serializers.CharField()
    temperature_min = serializers.CharField()
    temperature_max = serializers.CharField()
    humidity = serializers.CharField()
    pressure = serializers.CharField()
    wind_speed = serializers.CharField()
    wind_direction = serializers.CharField()
    description = serializers.CharField()


class CitySerilizer(serializers.Serializer):
    city = serializers.RegexField(regex=r'^([a-zA-Z]*\ *[a-zA-Z]*)$', required=True)
