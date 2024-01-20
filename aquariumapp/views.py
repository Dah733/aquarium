from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData, FCMToken
import json
import requests
from django.views.generic import ListView
from .models import Metric, ChemicalTest, AlertSetting
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAEno-Ge8:APA91bH0_vKu85-LpVKscoPAQqFJ1PNJvOAHuMh8Qx7VDmJBVmExMV9jIpNoKQ3OYT81_t-15AlRLCNkEwvKIUDOwQI9MAOIpwUqDmFfKtDoSQBjGTp7kSWHigCdTdxHsN0X_vhRCQEN"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())


def send(request):
    registration_ids = FCMToken.objects.values_list('token', flat=True)
    if registration_ids:
        send_notification(list(registration_ids), 'Code Keen added a new video', 'Code Keen new video alert')
        return HttpResponse("sent")
    else:
        return HttpResponse("No registration IDs found")

def home(request):
    return render(request, 'index.html')

def dashbord(request):
    # Message(
    # notification=Notification(title="title", body="text", image="url"),
    # )
    # device = FCMDevice.objects.all().first()
    # print(device)
    # device.send_message(Message(data={...}))
    return render(request, 'dashbord.html')

def get_real_time_sensor_data(request):
    try:
        latest_data = SensorData.objects.latest('timestamp')
        data = {
            'pH': latest_data.pH,
            'kH': latest_data.kH,
            'nitrites': latest_data.nitrites,
        }
        return JsonResponse(data)
    except SensorData.DoesNotExist:
        return JsonResponse({'error': 'No data available'})

@csrf_exempt
def receive_data_from_arduino(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Assuming the data format from Arduino includes 'pH', 'kH', 'nitrites', etc.
            pH = data.get('pH')
            kH = data.get('kH')
            nitrites = data.get('nitrites')

            # Save the received data to the database
            SensorData.objects.create(pH=pH, kH=kH, nitrites=nitrites)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class MetricListView(ListView):
    model = Metric
    template_name = 'metric_list.html'

    def get_queryset(self):
        return Metric.objects.all().order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        metrics = self.get_queryset()
        colored_metrics = []

        timestamps = []
        temperatures = []
        ph_values = []

        for metric in metrics:
            colored_metric = {
                'timestamp': metric.timestamp,
                'water_temperature': metric.water_temperature,
                'air_temperature': metric.air_temperature,
                'water_filter_flow': metric.water_filter_flow,
                'pH': metric.pH,
                'water_turbidity': metric.water_turbidity,
                'light_intensity': metric.light_intensity,
                'intensity_color': get_intensity_color(metric.light_intensity),
            }
            colored_metrics.append(colored_metric)

            timestamps.append(metric.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            temperatures.append(metric.water_temperature)
            ph_values.append(metric.pH)

        context['colored_metrics'] = colored_metrics
        context['timestamps_json'] = json.dumps(timestamps)
        context['temperatures_json'] = json.dumps(temperatures)
        context['ph_values_json'] = json.dumps(ph_values)
        
        return context

def get_intensity_color(intensity):
    if intensity < 1000:
        return 'low-intensity-color'
    elif intensity < 2000:
        return 'medium-intensity-color'
    else:
        return 'high-intensity-color'

class ChemicalTestView(ListView):
    model = ChemicalTest
    template_name = 'chemical_test.html'

class AlertSettingView(ListView):
    model = AlertSetting
    template_name = 'alert_setting.html'


def showFirebaseJS(request):
    data=''

    return HttpResponse(data,content_type="text/javascript")

@csrf_exempt
def save_fcm_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')
            # Save or replace the token using the FCMToken model
            FCMToken.objects.update_or_create(token=token)

            return JsonResponse({'status': 'success', 'message': 'Token saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})