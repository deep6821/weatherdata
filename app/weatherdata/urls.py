from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('get_weather_data', views.get_weather_data, name='get_weather_data'),
    path('get_list_of_weather_data', views.get_list_of_weather_data, name='get_list_of_weather_data'),
    path('get_min_max_weatherdata', views.get_min_max_weatherdata, name='get_min_max_weatherdata'),

]
