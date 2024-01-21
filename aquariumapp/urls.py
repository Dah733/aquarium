
from django.urls import path
from .views import *
urlpatterns = [
    path('', MetricListView.as_view(), name='home'),
    path('dashbord', dashbord, name='dashbord'),
    path('get_real_time_sensor_data/', get_real_time_sensor_data, name='get_real_time_sensor_data'),
    path('receive_data_from_arduino/', receive_data_from_arduino, name='receive_data_from_arduino'),
    path('metrics/', MetricListView.as_view(), name='metric-list'),
    path('alert-settings/', AlertSettingView.as_view(), name='alert-setting-list'),
     path('send/' , send),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"), path('save-fcm-token/', save_fcm_token, name='save_fcm_token'),
    path('chemical-tests/', chemical_tests, name='chemical-tests'),
    path('launch_chemical_test/', launch_chemical_test, name='launch_chemical_test'),
    path('metric-setting/', MetricSettingView.as_view(), name='metric_setting'),
     path('success/', success_view, name='success_view'),
]
