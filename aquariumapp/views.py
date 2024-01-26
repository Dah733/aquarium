from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MetricSetting, SensorData, FCMToken
import json
import requests
from django.views.generic import ListView
from .models import Metric, ChemicalTest, AlertSetting
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from django.views.generic.edit import FormView
from .forms import MetricSettingForm

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
            "image" : "https://www.thesprucepets.com/thmb/dcVNtKuCbjor2TWeoGLd1HlFIMM=/4608x2592/smart/filters:no_upscale()/reef-aquarium-504106122-5af89ebe3418c60038cd2123.jpg",
            "icon": "https://th.bing.com/th/id/OIP.4J46_yqs0mR04JD06RtbqAHaHa?rs=1&pid=ImgDetMain",
            
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
        water_filter_flow_values = []
        water_turbidity_values = []
        light_intensity_values = []

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
            water_filter_flow_values.append(metric.water_filter_flow)
            water_turbidity_values.append(metric.water_turbidity)
            light_intensity_values.append(metric.light_intensity)

        context['colored_metrics'] = colored_metrics
        context['timestamps_json'] = json.dumps(timestamps)
        context['temperatures_json'] = json.dumps(temperatures)
        context['ph_values_json'] = json.dumps(ph_values)
        context['water_filter_flow_values_json'] = json.dumps(water_filter_flow_values)
        context['water_turbidity_values_json'] = json.dumps(water_turbidity_values)
        context['light_intensity_values_json'] = json.dumps(light_intensity_values)

        return context

def get_intensity_color(intensity):
    if intensity < 1000:
        return 'low-intensity-color'
    elif intensity < 2000:
        return 'medium-intensity-color'
    else:
        return 'high-intensity-color'

def chemical_tests(request):
    tests = ChemicalTest.objects.all().order_by('-timestamp')
    return render(request, 'chemical_tests.html', {'tests': tests})

@csrf_exempt
def launch_chemical_test(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            test_name = data.get('testName')

            # Save the chemical test to the database with status 'En cours'
            chemical_test = ChemicalTest.objects.create(test_name=test_name, result=None, status='En cours')
            return JsonResponse({'status': 'success', 'test_id': chemical_test.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
class AlertSettingView(ListView):
    model = AlertSetting
    template_name = 'alert_setting.html'


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
          '        apiKey: "AIzaSyAZwYMKiwWzBmQSMc4v4hbF6rjcNCDBXVs",' \
         '        authDomain: "aquarium-16634.firebaseapp.com",' \
         '        databaseURL: "https://aquarium-16634.firebaseio.com",' \
         '        projectId: "aquarium-16634",' \
         '        storageBucket: "aquarium-16634.appspot.com",' \
         '        messagingSenderId: "79360301551",' \
         '        appId: "1:79360301551:web:5ed19cd2cbe4986cfefe1a",' \
         '        measurementId: "G-5DY4YQWMEB"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

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


class MetricSettingView(FormView):
    template_name = 'metric_setting.html'
    form_class = MetricSettingForm

    def form_valid(self, form):
        # Handle form submission, compare values, and send notifications
        cleaned_data = form.cleaned_data
        water_temperature = cleaned_data['water_temperature']
        air_temperature = cleaned_data['air_temperature']
        water_filter_flow = cleaned_data['water_filter_flow']
        pH = cleaned_data['pH']
        water_turbidity = cleaned_data['water_turbidity']
        light_intensity = cleaned_data['light_intensity']

        # Compare values with predefined thresholds
        check_threshold_and_notify('Water Temperature', water_temperature)
        check_threshold_and_notify('Air Temperature', air_temperature)
        check_threshold_and_notify('Water Filter Flow', water_filter_flow)
        check_threshold_and_notify('pH', pH)
        check_threshold_and_notify('Water Turbidity', water_turbidity)
        check_threshold_and_notify('Light Intensity', light_intensity)

        # Save the form data to the database
        MetricSetting.objects.create(
            water_temperature=water_temperature,
            air_temperature=air_temperature,
            water_filter_flow=water_filter_flow,
            pH=pH,
            water_turbidity=water_turbidity,
            light_intensity=light_intensity
        )

        # Redirect to the success page
        return redirect('success_view')
    
def check_threshold_and_notify(parameter, value):
    # Check if the value exceeds the threshold and send notification
    try:
        alert_setting = AlertSetting.objects.get(parameter=parameter)
        if value > alert_setting.threshold:
            # Send notification logic goes here
            # You can use FCM or any other method to send notifications
            pass
    except AlertSetting.DoesNotExist:
        pass

@csrf_exempt
def metric_setting(request):
    if request.method == 'POST':
        try:
            # Récupérez les données du formulaire
            water_temperature = request.POST.get('water_temperature')
            air_temperature = request.POST.get('air_temperature')
            water_filter_flow = request.POST.get('water_filter_flow')
            pH = request.POST.get('pH')
            water_turbidity = request.POST.get('water_turbidity')
            light_intensity = request.POST.get('light_intensity')

            # Enregistrez les paramètres dans la base de données
            MetricSetting.objects.create(
                water_temperature=water_temperature,
                air_temperature=air_temperature,
                water_filter_flow=water_filter_flow,
                pH=pH,
                water_turbidity=water_turbidity,
                light_intensity=light_intensity
            )

            return JsonResponse({'status': 'success', 'message': 'Paramètres enregistrés avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide'})

def success_view(request):
    return render(request, 'success.html')