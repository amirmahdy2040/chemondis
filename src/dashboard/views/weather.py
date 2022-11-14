from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from dashboard.serializer import WeatherSerilizer, CitySerilizer
from weather.services.weather import OpenWeather
from app.exception_handler import unpredicted_exception_handler
from dashboard.broadcast import broadcast


class WeatherAPIView(GenericAPIView):

    @swagger_auto_schema(methods=['post'], request_body=CitySerilizer)
    @action(detail=False, methods=['post'])
    @unpredicted_exception_handler("DEBUG")
    def post(self, request, *args, **kwargs):
        """
        This method checks weather for a given city
        input   -- city
        """
        serializer = CitySerilizer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            ow = OpenWeather()
            dt = ow.call(data['city'])
            broadcast(data['city'], dt)
            return Response({"message": "OK", "data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
