
from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('dashbord', dashbord, name='dashbord'),
    path('get_real_time_sensor_data/', get_real_time_sensor_data, name='get_real_time_sensor_data'),
    path('receive_data_from_arduino/', receive_data_from_arduino, name='receive_data_from_arduino'),
]
