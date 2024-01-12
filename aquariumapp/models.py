from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pH = models.FloatField()
    kH = models.FloatField()
    nitrites = models.FloatField()
