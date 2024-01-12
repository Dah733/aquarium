from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
import json

def home(request):
    return render(request, 'index.html')

def dashbord(request):
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
