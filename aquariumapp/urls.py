
from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('dashbord', dashbord, name='dashbord'),
    path('get_real_time_sensor_data/', get_real_time_sensor_data, name='get_real_time_sensor_data'),
    path('receive_data_from_arduino/', receive_data_from_arduino, name='receive_data_from_arduino'),
    path('metrics/', MetricListView.as_view(), name='metric-list'),
    path('chemical-tests/', ChemicalTestView.as_view(), name='chemical-test-list'),
    path('alert-settings/', AlertSettingView.as_view(), name='alert-setting-list'),
     path('send/' , send),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
]
