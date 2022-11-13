from django.urls import path
from dashboard.views.index import index
from dashboard.views.weather import WeatherAPIView

urlpatterns = [
    path('', index, name='index'),
    path('api/weather/', WeatherAPIView.as_view(), name='WeatherAPIView'),
]
