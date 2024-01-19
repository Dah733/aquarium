from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pH = models.FloatField()
    kH = models.FloatField()
    nitrites = models.FloatField()

class Metric(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    water_temperature = models.FloatField()
    air_temperature = models.FloatField()
    water_filter_flow = models.FloatField()
    pH = models.FloatField()
    water_turbidity = models.FloatField()
    light_intensity = models.FloatField()

    def __str__(self):
        return f'Metric at {self.timestamp}'
    
class ChemicalTest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    test_name = models.CharField(max_length=255)

class AlertSetting(models.Model):
    parameter = models.CharField(max_length=255)
    threshold = models.FloatField()