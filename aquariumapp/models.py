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
    TEST_STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
        ('Échec', 'Échec'),
    ]

    test_name = models.CharField(max_length=255)
    result = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TEST_STATUS_CHOICES, default='En attente')

    def __str__(self):
        return f'{self.test_name} Test Result at {self.timestamp}'
    
class AlertSetting(models.Model):
    parameter = models.CharField(max_length=255)
    threshold = models.FloatField()


class FCMToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.token
    
from django.db import models

class MetricSetting(models.Model):
    water_temperature = models.FloatField()
    air_temperature = models.FloatField()
    water_filter_flow = models.FloatField()
    pH = models.FloatField()
    water_turbidity = models.FloatField()
    light_intensity = models.FloatField()

    def __str__(self):
        return 'Paramètres métriques'