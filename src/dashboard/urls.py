from django.urls import path, include
from dashboard.views.index import index
from dashboard.views.weather import WeatherAPIView

urlpatterns = [
    path('', index, name='index'),
    path('api/weather/', WeatherAPIView.as_view(), name='WeatherAPIView'),
    path('i18n/', include('django.conf.urls.i18n')),
]
